Vision - MODULARITY 3.0
=======================

The branch demonstrates an alternatively of modularity without:
1. Filtering out of nonmodular packages
2. Fail-Safe
3. Hot-fix-repositories

They will be replaced by another mechanisms supported from rpm-4.14 - `Provides`, `Requires`,
`Conflicts`, and `Rich-deps`.

Benefits
--------

1. Modular packages will work together with nonmodular packages without any additional
metadata (modules.yaml)
2. RPM, libsolv, zypper will support out modules without any problems.
3. The proposal keeps modules.yaml as a part of design to provide additional information about
content in distribution (`dnf module list` or other commands in `DNF` unchanged).
4. Unify a modular build system with non-modular
5. Improve modularity on customer side by
 - compact packages are well known to customers
 - no problems with untransparent modular filtering across all repositories
 - no problem with Fail-Safe mechanism with same level of safety
6. Improved flexibility for packagers

Compatibility
-------------
The proposal is 100% compatible with dnf-4/yum-4. Only some internal workflow in DNF could be
simplify or removed.
No changes will be required on a customer side.

Requirements
------------

The proposal requires changes in buld-system (mostly `Modular Build System`). Also it requires
a support of maintainers to adjust specs.

Problem - Prevent upgrade of non-modular package to modular
-----------------------------------------------------------

Modular package will use a name with surfix that will represent stream or name of stream.

`Name: %{base_name}%{?mod_version}`

To ensure that only one provider is installed on the system a conflict is required:

`Conflicts: %{base_name}`

To keep compatibility it is required to add original provides:

```
Provides: %{base_name}%{?_isa} = %{version}-%{release}
Provides: %{base_name} = %{version}-%{release}
```

Problem - Modular package must require modular package from required module
----------------------------------------------------------------------------

In repository in ``repository_with_yaml`` perl and perl-DBI packages are available (modular and not
modular)

When I install modular perl-DBI I expect that modular perl is used as a dependency. The behaviour
is obtained by using additional provides and rich dependencies. Each modular package could
have provides that say I am a modular package, I am from a `module`, `module:stream` and
`module:stream:context`. See example `test-perl.spec`.
```
Provides: module(I_am_from_module)
Provides: module(%{?mod_name})
Provides: module(%{?mod_name}:%{?mod_stream})
Provides: module(%{?mod_name}:%{?mod_stream}:%{?mod_context})
```
Provides are suited to be used for requires, that could specify what functionality it requires but
but maintainer could set if the require must be a modular, or from which `module`, `module:stream`,
or `module:stream:context`.  

Examples how requires could be constructed:
___________________________________________

```
Requires: (test-perl = 5.24 with module(name:stream))
```
or with provided additional macro
```
Requires: test-perl%{?module_require_1} = 5.24
```
or for subpackages

```
Requires: test-perl%{?mod_version} = 5.24
```

Non modular package that depends on nonmodular component will use

```
Requires: (test-perl = 5.24 without module(name:stream))
```

Problem - unwanted obsoletes of modular package
-----------------------------------------------

In Fedora 32/RHEL8 modular packages are protected from obsoletes and from higher version by removing
all other packages from distribution with the same name or with the same provide as a name of
modular package.

The proposed vision protects modular packages without any requirement for filtering, because modular
packages will use a different package names, therefore obsoletes of non-modular packages will be not
applicable to modular one.

Notes
-----

`mod_version` - string that represents module name, stream and in case of multicontect stream also
context. `mod_version` is used as a surfix for package names and it will be provided during build
of modular packages.

`module_require_1` - string that reflects modular requires.

`module(I_am_from_module)` - provide that in the examples mark packages that they are modular.

`module(%{?mod_name})` - provide with a module `name`

`module(%{?mod_name}:%{?mod_stream})` provide with a module `name:stream`

`module(%{?mod_name}:%{?mod_stream}:%{?mod_context})` - provide with a module `name:stream:context`

To build rpms from example specs use for modular build rpmbuild with additional defines:
```
rpmbuild -ba --define='mod_version <-<surfix>>' --define='mod_name <value>' --define='mod_stream <value>' --define='mod_context <value>' rpm.spec
```

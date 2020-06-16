Vision - MODULARITY 3.0
=======================

The branch demonstrates an alternatively of modularity without:
1. Filtering out of non-modular packages
2. Fail-Safe
 - Store yamls when module-stream is enabled
 - Prevent installing of modular package without information in yaml
3. Hot-fix-repositories
4. Calculation of applicability of modular errata

They will be replaced by another mechanisms supported from rpm-4.14 - `Provides`, `Requires`,
`Conflicts`, and `Rich-deps`.

Benefits
--------

1. Modular packages will work together with non-modular packages without any additional
metadata (modules.yaml)
2. RPM, libsolv, zypper will support out modules without any problems.
3. The proposal keeps modules.yaml as a part of design to provide additional information about
content in distribution (`dnf module list` or other commands in `DNF` unchanged).
4. Unify a modular build system with non-modular
5. Improve modularity on customer side by
 - compact packages are well known to customers
 - no problems with nontransparent modular filtering across all repositories
 - no problems with Fail-Safe mechanism with same level of safety
 - no problems with calculation of errata applicability
6. Improved flexibility for packagers
7. Same SPEC/build system for modular and non-modular builds

Compatibility
-------------
The proposal is 100% compatible with dnf-4/yum-4 (Fedora 27+). Only some internal workflow in DNF
could be simplify or removed:
 - modular filtering
 - modular solver
 - applicability of modular errata

No changes will be required on a customer side.

Requirements
------------

 - changes in buld-system (mostly `Modular Build System`)
 - changes in specs => support of maintainers
 - rpm-4.14 (Fedora 27+, RHEL8)

New elements in SPECs - OPTIONAL
--------------------------------

1. Create compat packages by adding an optional suffix
```
# move name of the package to a variable
%global base_name test-perl-DBI
Name: %{base_name}%{?mod_version}
```
Packages in modules could also be without suffix, but then they will be not protected from other
obsoletes or they can be easily mixed with packages from other sources. The decision will be on
maintainers.

2. Create conflict with other provides
It is required when provides cannot be installed in parallel
```
Conflicts: %{base_name}
```

3. Additional provides
Mark a package that it is from a module, from module name and so on. It allows other packages to
require specific providers non-modular or modular, or from certain module name, stream or context.
Macros (%{?mod_name}) will be specified during builds.
```
# Mark a package that it is from a module
Provides: module(I_am_from_module)

# Mark a package that it is from the mod_stream
Provides: module(%{?mod_name})

# Mark a package that it is from the mod_stream:mod_stream
Provides: module(%{?mod_name}:%{?mod_stream})

# Mark a package that it is from the mod_stream:mod_stream:mod_context
Provides: module(%{?mod_name}:%{?mod_stream}:%{?mod_context})
```

4. Targeted requires
Packages could directly requires modular or non modular version of providers. It uses Rich deps with
combination with additional modular provides.

To require  `test-perl=5.24` from non-modular provider:
```
Requires: (test-perl = 5.24 without module(I_am_from_module))
```

To require `test-perl=5.24` from modular provider:
```
Requires: (test-perl = 5.24 with module(I_am_from_module))
```

To require `test-perl=5.24` from module `perl`:
```
Requires: (test-perl = 5.24 with module(perl))
```

To require `test-perl=5.24` from module `perl`, and stream `5.24`:
```
Requires: (test-perl = 5.24 with module(perl:5.24))
```

To require `test-perl=5.24` from module `perl`, stream `5.24`, and context `A`:
```
Requires: (test-perl = 5.24 with module(perl:5.24:A))
```

For subpackages it wii be possible to use:

```
Requires: test-perl%{?mod_version} = 5.24
```

It is also possible to use dynamic requires like:
```
Requires: test-perl%{?module_require_1} = 5.24
```

Example data
------------

3 repositories are provided to demonstrate the vision in following directories:
 - obsoletes
   - demonstration of obsolete of perl package is not applicable to modular packages without
   modular filtering
   - repository is without modular yaml
 - repository
   - demonstrates self protection of modular packages without modular filtering
   - repository is without modular yaml
 - repository_with_yaml
   - repository is with modular yaml
   - demonstrates compatibility with dnf-4

All SPECs used for generation of test RPMs are provided in the project.

Problem - Prevent upgrade of non-modular package to modular
-----------------------------------------------------------

Modular package will use a name with suffix that will represent stream or name of stream.

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

Provides are suited to be used for requires, that could specify what functionality it requires but
but maintainer could set if the require must be a modular, or from which `module`, `module:stream`,
or `module:stream:context`.  

Problem - unwanted obsoletes of modular package
-----------------------------------------------

In Fedora 32/RHEL8 modular packages are protected from obsoletes and from higher version by removing
all other packages from distribution with the same name or with the same provide as a name of
modular package.

The proposed vision protects modular packages without any requirement for filtering, because modular
packages will use a different package names, therefore obsoletes of non-modular packages will be not
applicable to modular one.

Problem - false positive modular advisories
-------------------------------------------

With compat packages the calculation will not require any special code for generation or calculation
of errata in comparison to RHEL-7/Fedora22

Notes
-----

`mod_version` - string that represents module name, stream and in case of multicontect stream also
context. `mod_version` is used as a suffix for package names and it will be provided during build
of modular packages.

`module_require_1` - string that reflects modular requires.

`module(I_am_from_module)` - provide that in the examples mark packages that they are modular.

`module(%{?mod_name})` - provide with a module `name`

`module(%{?mod_name}:%{?mod_stream})` provide with a module `name:stream`

`module(%{?mod_name}:%{?mod_stream}:%{?mod_context})` - provide with a module `name:stream:context`

To build rpms from example specs use for modular build rpmbuild with additional defines:
```
rpmbuild -ba --define='mod_version <-<suffix>>' --define='mod_name <value>' --define='mod_stream <value>' --define='mod_context <value>' rpm.spec
```

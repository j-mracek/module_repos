%global base_name test-perl-DBI

%{?mod_version:%bcond_without modules}

Name: %{base_name}%{?mod_version}
Version: 1
Release: 1
Summary: testpkg Package
Group: System Environment/Base
License: LGPLv2.1+
BuildArch: x86_64
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Conflicts: %{base_name}

%if %{with modules}
Provides: %{base_name}%{?_isa} = %{version}-%{release}
Provides: %{base_name} = %{version}-%{release}
Provides: module(name:stream)
Requires: (test-perl = 5.24 with module(name:stream))
%else
Requires: (test-perl = 5.24 without module(name:stream))
%endif


%description

This is a perl-DBI test package

%build

%install

%files


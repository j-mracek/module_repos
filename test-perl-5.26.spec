%global base_name test-perl

%{?mod_version:%bcond_without modules}

Name: %{base_name}%{?mod_version}
Version: 5.26
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
Provides: module(I_am_from_module)
Provides: module(%{?mod_name})
Provides: module(%{?mod_name}:%{?mod_stream})
Provides: module(%{?mod_name}:%{?mod_stream}:%{?mod_context})
%endif


%description

This is a perl-DBI test package

%build

%install

%files


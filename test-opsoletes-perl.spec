Name: test-obsoletes-perl
Version: 1.11
Release: 1
Summary: testpkg Package
Group: System Environment/Base
License: LGPLv2.1+
BuildArch: x86_64
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Obsoletes: test-perl < 6

%description

This is a perl obsoleter test package

%build

%install

%files


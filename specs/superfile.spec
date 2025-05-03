%global debug_package %{nil}
%global binary_name spf

Name:    superfile
Version: 1.2.1
Release: 1%{?dist}
Summary: Pretty fancy and modern terminal file manager

License: MIT
URL:     https://github.com/yorukot/superfile
Source:  %{url}/releases/download/v%{version}/%{name}-linux-v%{version}-amd64.tar.gz
Source1: https://raw.githubusercontent.com/yorukot/superfile/v%{version}/README.md
Source2: https://raw.githubusercontent.com/yorukot/superfile/v%{version}/LICENSE

%description
%{summary}

%prep
%autosetup -c
cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} LICENSE

%build

%install
install -p -D dist/%{name}-linux-v%{version}-amd64/%{binary_name} %{buildroot}%{_bindir}/%{binary_name}

%files
%doc CONFIGURATION.md
%license LICENSE
%{_bindir}/%{binary_name}

%changelog
%autochangelog

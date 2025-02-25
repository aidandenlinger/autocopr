%global debug_package %{nil}

Name:    volta
Version: 2.0.2
Release: 1%{?dist}
Summary: JS Toolchains as Code

License: BSD 2-CLAUSE
# https://github.com/volta-cli/volta/releases/download/v2.0.1/volta-2.0.1-linux.tar.gz
URL:     https://github.com/volta-cli/volta
Source:  %{url}/releases/download/v%{version}/%{name}-%{version}-linux.tar.gz
Source1: https://raw.githubusercontent.com/volta-cli/volta/v%{version}/README.md
Source2: https://raw.githubusercontent.com/volta-cli/volta/v%{version}/LICENSE

%description
%{summary}

%prep
%autosetup -c
cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} LICENSE

%build

%install
install -p -D %{name} %{buildroot}%{_bindir}/%{name}
install -p -D %{name} %{buildroot}%{_bindir}/%{name}-migrate
install -p -D %{name} %{buildroot}%{_bindir}/%{name}-shim

%files
%doc CONFIGURATION.md
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-migrate
%{_bindir}/%{name}-shim

%changelog
%autochangelog

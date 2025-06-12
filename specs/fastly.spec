%global debug_package %{nil}

Name:    fastly
Version: 11.3.0
Release: 1%{?dist}
Summary: Build, deploy and configure Fastly services from your terminal

License: MIT
URL:     https://github.com/fastly/cli
#https://github.com/fastly/cli/releases/download/v11.2.0/fastly_v11.2.0_linux-amd64.tar.gz
Source:  %{url}/releases/download/v%{version}/fastly_v%{version}_linux-amd64.tar.gz
Source1: https://raw.githubusercontent.com/fastly/cli/v%{version}/README.md
Source2: https://raw.githubusercontent.com/fastly/cli/v%{version}/LICENSE

%description
%{summary}

%prep
%autosetup -c
cp %{SOURCE1} README.md
cp %{SOURCE2} LICENSE

%install
install -v -p -D %{name} %{buildroot}%{_bindir}/%{name}

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}

%changelog
%autochangelog

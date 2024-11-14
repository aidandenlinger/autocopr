%global debug_package %{nil}

Name:    lazyjj
Version: 0.4.2
Release: 1%{?dist}
Summary: TUI for Jujutsu/jj

License: Apache-2.0
URL: https://github.com/Cretezy/lazyjj
Source: %{url}/releases/download/v%{version}/%{name}_%{version}_Linux_x86_64.tar.gz
Source1: https://raw.githubusercontent.com/Cretezy/lazyjj/v%{version}/README.md
Source2: https://raw.githubusercontent.com/Cretezy/lazyjj/v%{version}/LICENSE

%description
%{summary}

%prep
%autosetup -c
cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} LICENSE

%build

%install
install -p -D %{name} %{buildroot}%{_bindir}/%{name}

%files
%doc CONFIGURATION.md
%license LICENSE
%{_bindir}/%{name}

%changelog
%autochangelog

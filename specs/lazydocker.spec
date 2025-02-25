%global debug_package %{nil}

Name:    lazydocker
Version: 0.24.1
Release: 1%{?dist}
Summary: The lazier way to manage everything docker

License: MIT
URL: https://github.com/jesseduffield/lazydocker
Source: %{url}/releases/download/v%{version}/%{name}_%{version}_Linux_x86_64.tar.gz
Source1: https://raw.githubusercontent.com/jesseduffield/lazydocker/v%{version}/README.md
Source2: https://raw.githubusercontent.com/jesseduffield/lazydocker/v%{version}/LICENSE

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

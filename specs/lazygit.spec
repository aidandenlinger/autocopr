%global debug_package %{nil}

Name:    lazygit
Version: 0.46.0
Release: 1%{?dist}
Summary: simple terminal UI for git commands

License: MIT
URL: https://github.com/jesseduffield/lazygit
Source: %{url}/releases/download/v%{version}/%{name}_%{version}_Linux_x86_64.tar.gz
Source1: https://raw.githubusercontent.com/jesseduffield/lazygit/v%{version}/README.md
Source2: https://raw.githubusercontent.com/jesseduffield/lazygit/v%{version}/LICENSE

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

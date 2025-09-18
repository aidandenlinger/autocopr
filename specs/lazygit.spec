# Taken from RelativeSure's repo, thank you!
# https://github.com/RelativeSure/autocopr/blob/54ebe5d5ed94d14aad2bc021507b370d508cc622/specs/lazygit.spec
%global debug_package %{nil}

Name:    lazygit
Version: 0.55.1
Release: 1%{?dist}
Summary: simple terminal UI for git commands

License: MIT
URL: https://github.com/jesseduffield/lazygit
Source: %{url}/releases/download/v%{version}/%{name}_%{version}_Linux_x86_64.tar.gz

%description
%{summary}

%prep
%autosetup -c

%build

%install
install -p -D %{name} %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
%license LICENSE

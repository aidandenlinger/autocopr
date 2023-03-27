%global debug_package %{nil}

Name:       zellij
Version: 0.35.2
Release: 1%{?dist}
Summary:    A terminal workspace with batteries included.

License:    MIT
URL:        https://github.com/zellij-org/zellij
Source:     %{url}/releases/download/v%{version}/%{name}-%{_arch}-unknown-linux-musl.tar.gz

%description
Zellij is a workspace aimed at developers, ops-oriented people and anyone who loves the terminal. At its core, it is a terminal multiplexer (similar to tmux and screen), but this is merely its infrastructure layer. Zellij includes a layout system, and a plugin system allowing one to create plugins in any language that compiles to WebAssembly.

%prep
# This source file doesn't have a high level directory, so create one
%autosetup -c

%build

%install
mkdir -p %{buildroot}%{_bindir}
install %{name} %{buildroot}%{_bindir}

%files
%{_bindir}/%{name}

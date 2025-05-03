%global debug_package %{nil}

Name:    topgrade
Version: 16.0.3
Release: 1%{?dist}
Summary: Upgrade all the things

License: GPL-3.0
# https://github.com/topgrade-rs/topgrade/releases/download/v16.0.1/topgrade-v16.0.1-x86_64-unknown-linux-musl.tar.gz
URL:     https://github.com/topgrade-rs/topgrade
Source:  %{url}/releases/download/v%{version}/%{name}-v%{version}-x86_64-unknown-linux-musl.tar.gz
Source1: https://raw.githubusercontent.com/topgrade-rs/topgrade/v%{version}/README.md
Source2: https://raw.githubusercontent.com/topgrade-rs/topgrade/v%{version}/LICENSE

%description
Keeping your system up to date usually involves invoking multiple package managers.
This results in big, non-portable shell one-liners saved in your shell.
To remedy this, Topgrade detects which tools you use and runs the appropriate commands to update them.

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

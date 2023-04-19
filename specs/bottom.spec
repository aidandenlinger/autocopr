%global debug_package %{nil}

Name: bottom
Version: 0.8.0
Release: 1%{?dist}
Summary: Yet another cross-platform graphical process/system monitor.

License: MIT
URL: https://github.com/ClementTsang/bottom
Source: %{url}/releases/download/%{version}/%{name}_x86_64-unknown-linux-gnu.tar.gz

%description
A customizable cross-platform graphical process/system monitor for the terminal. Supports Linux, macOS, and Windows. Inspired by gtop, gotop, and htop. 

%prep
%autosetup -c

%build

%install
install -v -p -D btm %{buildroot}%{_bindir}/btm

# Shell completion
install -v -p -D -m 0644 completion/btm.bash %{buildroot}%{_datadir}/bash-completion/completions/btm
install -v -p -D -m 0644 completion/btm.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/btm.fish
install -v -p -D -m 0644 completion/_btm %{buildroot}%{_datadir}/zsh/site-functions/_btm

%files
%{_bindir}/btm
%{_datadir}/bash-completion/completions/btm
%{_datadir}/fish/vendor_completions.d/btm.fish
%{_datadir}/zsh/site-functions/_btm


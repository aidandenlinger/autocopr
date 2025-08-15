%global debug_package %{nil}
%global binary_name btm

Name: bottom
Version: 0.11.1
Release: 1%{?dist}
Summary: Yet another cross-platform graphical process/system monitor

License: MIT
URL: https://github.com/ClementTsang/bottom
Source: %{url}/releases/download/%{version}/%{name}_x86_64-unknown-linux-gnu.tar.gz
Source1: %{url}/releases/download/%{version}/manpage.tar.gz
Source2: https://raw.githubusercontent.com/ClementTsang/bottom/%{version}/LICENSE

%description
A customizable cross-platform graphical process/system monitor for the terminal.
Supports Linux, macOS, and Windows. Inspired by gtop, gotop, and htop.

%prep
%autosetup -c
# Dump the manpage in this folder without deleting our binary
%__rpmuncompress -x %{SOURCE1}
cp %{SOURCE2} .

%build

%install
install -v -p -D %{binary_name} %{buildroot}%{_bindir}/%{binary_name}

# Shell completion
install -pvD -m 0644 completion/%{binary_name}.bash %{buildroot}%{bash_completions_dir}/%{binary_name}
install -pvD -m 0644 completion/%{binary_name}.fish %{buildroot}%{fish_completions_dir}/%{binary_name}.fish
install -pvD -m 0644 completion/_%{binary_name} %{buildroot}%{zsh_completions_dir}/_%{binary_name}

# Manpage
install -v -p -D -m 0644 %{binary_name}.1.gz %{buildroot}%{_mandir}/man1/%{binary_name}.1.gz

%files
%{_bindir}/%{binary_name}
%{bash_completions_dir}/%{binary_name}
%{fish_completions_dir}/%{binary_name}.fish
%{zsh_completions_dir}/_%{binary_name}
%{_mandir}/man1/%{binary_name}.1.gz
%license LICENSE

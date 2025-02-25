%global debug_package %{nil}

Name:    fish
Version: 4.0b1
Release: 1%{?dist}
Summary: The user-friendly command line shell.

License: MIT
Source:  https://github.com/fish-shell/fish-shell/releases/download/%{version}/fish-static-linux-x86_64.tar.xz
Source1: https://raw.githubusercontent.com/fish-shell/fish-shell/%{version}/README.rst
Source2: https://raw.githubusercontent.com/fish-shell/fish-shell/%{version}/COPYING

%description
Fish is a smart and user-friendly command line shell for Linux, macOS, and the rest
of the family. Fish includes features like syntax highlighting, autosuggestions,
and tab completions that just work, with nothing to learn or configure.

%prep
%autosetup -c
cp %{SOURCE1} README.md
cp %{SOURCE2} LICENSE

%install
install -v -p -D %{name} %{buildroot}%{_bindir}/%{name}
install -v -p -D %{name}_indent %{buildroot}%{_bindir}/%{name}_indent
install -v -p -D %{name}_key_reader %{buildroot}%{_bindir}/%{name}_key_reader

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}_indent
%{_bindir}/%{name}_key_reader

%changelog
%autochangelog

%global debug_package %{nil}

Name:    fish
Version: 4.0.2
Release: 1%{?dist}
Summary: The user-friendly command line shell.

License: MIT
URL:     https://github.com/fish-shell/fish-shell
Source:  %{url}/releases/download/%{version}/fish-%{version}.tar.xz
Source1: https://raw.githubusercontent.com/fish-shell/fish-shell/%{version}/README.rst
Source2: https://raw.githubusercontent.com/fish-shell/fish-shell/%{version}/COPYING

BuildRequires: cmake >= 3.19
BuildRequires: cargo >= 1.40
BuildRequires: rust >= 1.40
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: ncurses-devel
BuildRequires: pcre2-devel

%description
Fish is a smart and user-friendly command line shell for Linux, macOS, and the rest
of the family. Fish includes features like syntax highlighting, autosuggestions,
and tab completions that just work, with nothing to learn or configure.


%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} README.md
cp %{SOURCE2} LICENSE

%build
%cmake
%cmake_build

%install
%cmake_install

# Move config.fish from /usr/etc/fish/ to /etc/fish/ in the buildroot
if [ -f %{buildroot}/usr/etc/fish/config.fish ]; then
    mkdir -p %{buildroot}%{_sysconfdir}/fish
    mv %{buildroot}/usr/etc/fish/config.fish %{buildroot}%{_sysconfdir}/fish/config.fish
fi

%files
# Documentation
%doc %{_docdir}/fish
%doc CONTRIBUTING.rst README.rst
%license LICENSE
# Executable files
%attr(0755,root,root) %{_bindir}/fish
%attr(0755,root,root) %{_bindir}/fish_indent
%attr(0755,root,root) %{_bindir}/fish_key_reader
# Config files and folders
%dir %{_sysconfdir}/fish/
%config(noreplace) %{_sysconfdir}/fish/config.fish
%{_datadir}/applications/fish.desktop
%{_datadir}/fish/
%{_mandir}/man1/fish*.1*
%{_datadir}/pixmaps/fish.png
%{_datadir}/pkgconfig/fish.pc

%post
# Add fish to the list of allowed shells in /etc/shells
if ! grep %{_bindir}/fish %{_sysconfdir}/shells >/dev/null; then
    echo %{_bindir}/fish >>%{_sysconfdir}/shells
fi

%postun
# Remove fish from the list of allowed shells in /etc/shells
if [ "$1" = 0 ]; then
    grep -v %{_bindir}/fish %{_sysconfdir}/shells >%{_sysconfdir}/fish.tmp
    mv %{_sysconfdir}/fish.tmp %{_sysconfdir}/shells
fi

%changelog
%autochangelog

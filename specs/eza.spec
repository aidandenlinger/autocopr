%global debug_package %{nil}

Name:       eza
Version: 0.13.0
Release: 1%{?dist}
Summary:    A modern, maintained replacement for ls

License:    MIT
URL:        https://github.com/eza-community/eza
Source:     %{url}/releases/download/v%{version}/%{name}_x86_64-unknown-linux-gnu.tar.gz
Source1:    https://raw.githubusercontent.com/eza-community/eza/v%{version}/completions/bash/eza
Source2:    https://raw.githubusercontent.com/eza-community/eza/v%{version}/completions/fish/eza.fish
Source3:    https://raw.githubusercontent.com/eza-community/eza/v%{version}/completions/zsh/_eza

%description
eza is a modern, maintained replacement for the venerable file-listing command-line program ls that ships with Unix and Linux operating systems, giving it more features and better defaults. It uses colours to distinguish file types and metadata.

%prep
# This source file doesn't have a high level directory, so create one
%autosetup -c
cp %{SOURCE1} eza.bash
cp %{SOURCE2} .
cp %{SOURCE3} .

%build

%install
install -p -D %{name} %{buildroot}%{_bindir}/%{name}

# Shell completion
# Inspired by alacritty's spec build
install -v -p -D -m 0644 %{name}.bash %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -v -p -D -m 0644 %{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish
install -v -p -D -m 0644 _%{name} %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

%files
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}

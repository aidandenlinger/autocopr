%global debug_package %{nil}

Name:    chezmoi
Version: 2.54.0
Release: 1%{?dist}
Summary: Manage your dotfiles across multiple diverse machines, securely.

# https://github.com/twpayne/chezmoi/releases/download/v2.54.0/chezmoi_2.54.0_linux-musl_amd64.tar.gz
License: MIT
URL: https://github.com/twpayne/chezmoi
Source: %{url}/releases/download/v%{version}/%{name}_%{version}_linux-musl_amd64.tar.gz
Source1: https://raw.githubusercontent.com/twpayne/chezmoi/v%{version}/README.md
Source2: https://raw.githubusercontent.com/twpayne/chezmoi/v%{version}/LICENSE

%description
Manage your dotfiles across multiple diverse machines, securely.

%prep
%autosetup -c
cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} LICENSE

%build

%install
ls -la
install -p -D %{name} %{buildroot}%{_bindir}/%{name}
ls -la completions
install -pvD -m 0644 completions/%{name}-completion.bash %{buildroot}%{bash_completions_dir}/%{name}.bash
install -pvD -m 0644 completions/%{name}.zsh %{buildroot}%{zsh_completions_dir}/%{name}.zsh
install -pvD -m 0644 completions/%{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish

%files
%doc CONFIGURATION.md
%license LICENSE
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}.bash
%{zsh_completions_dir}/%{name}.zsh
%{fish_completions_dir}/%{name}.fish

%changelog
%autochangelog

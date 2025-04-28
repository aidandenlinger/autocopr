%global debug_package %{nil}

Name: starship
Version: 1.23.0
Release: 1%{?dist}
Summary: The minimal, blazing-fast, and infinitely customizable prompt for any shell

License: ISC
URL: https://github.com/starship/starship
Source: %{url}/releases/download/v%{version}/%{name}-x86_64-unknown-linux-gnu.tar.gz
# No man page yet (https://github.com/starship/starship/issues/2926), so including the config README
Source1: https://raw.githubusercontent.com/starship/starship/v%{version}/docs/config/README.md
Source2: https://raw.githubusercontent.com/starship/starship/v%{version}/LICENSE

%description
The minimal, blazing-fast, and infinitely customizable prompt for any shell!

- Fast: it's fast – really really fast! 🚀
- Customizable: configure every aspect of your prompt.
- Universal: works on any shell, on any operating system.
- Intelligent: shows relevant information at a glance.
- Feature rich: support for all your favorite tools.
- Easy: quick to install – start using it in minutes.

%prep
%autosetup -c
# Copy config README here
cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} .

%build
./%{name} completions bash > %{name}.bash
./%{name} completions zsh > _%{name}
# Fish has built in completions: https://github.com/fish-shell/fish-shell/blob/master/share/completions/starship.fish

%install
install -p -D %{name} %{buildroot}%{_bindir}/%{name}

# Shell completions (Fish has built-in completions, see above)
install -pvD -m 0644 %{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
install -pvD -m 0644 _%{name} %{buildroot}%{zsh_completions_dir}/_%{name}

%files
%doc CONFIGURATION.md
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}
%{zsh_completions_dir}/_%{name}
%license LICENSE

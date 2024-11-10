%global debug_package %{nil}

Name:    atuin
Version: 18.3.0
Release: 1%{?dist}
Summary: ✨ Magical shell history

License:    MIT
# https://github.com/atuinsh/atuin/releases/download/v18.3.0/atuin-x86_64-unknown-linux-musl.tar.gz
URL:        https://github.com/atuinsh/atuin
Source:     %{url}/releases/download/v%{version}/%{name}-x86_64-unknown-linux-musl.tar.gz
Source1:    https://raw.githubusercontent.com/atuinsh/atuin/v%{version}/README.md
#Source2:    https://raw.githubusercontent.com/jdx/mise/v%{version}/completions/mise.bash
#Source3:    https://raw.githubusercontent.com/jdx/mise/v%{version}/completions/mise.fish

%description
Atuin replaces your existing shell history with a SQLite database, and records additional context for your commands. Additionally, it provides optional and fully encrypted synchronisation of your history between machines, via an Atuin server.

%prep
%autosetup -n atuin

cp %{SOURCE1} CONFIGURATION.md
#cp %{SOURCE2} .
#cp %{SOURCE3} .

%build

%install
# Ensure the source binary is in the expected location
install -p -D %{name} %{buildroot}%{_bindir}/%{name}

# Shell completions
#install -pvD -m 0644 %{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
#install -pvD -m 0644 %{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish

%files
%doc CONFIGURATION.md
%{_bindir}/%{name}
#%{bash_completions_dir}/%{name}
#%{fish_completions_dir}/%{name}.fish
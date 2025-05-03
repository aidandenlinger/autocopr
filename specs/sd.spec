%global debug_package %{nil}

Name:    sd
Version: 1.0.0
Release: 2%{?dist}
Summary: Intuitive find & replace CLI (sed alternative)

License: MIT
URL: https://github.com/chmln/sd
Source: %{url}/releases/download/v%{version}/%{name}-v%{version}-x86_64-unknown-linux-gnu.tar.gz

%description
%{summary}

%prep
%autosetup -n %{name}-v%{version}-x86_64-unknown-linux-gnu

%build
# Compress the manpage
gzip %{name}.1

%install
install -p -D %{name} %{buildroot}%{_bindir}/%{name}

# Shell completions
install -pvD -m 0644 completions/%{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
install -pvD -m 0644 completions/_%{name} %{buildroot}%{zsh_completions_dir}/_%{name}
install -pvD -m 0644 completions/%{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish

# Man page
install -pvD -m 0644 %{name}.1.gz %{buildroot}%{_mandir}/man1/%{name}.1.gz

%files
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}
%{zsh_completions_dir}/_%{name}
%{fish_completions_dir}/%{name}.fish
%{_mandir}/man1/%{name}.1.gz
%license LICENSE

%changelog
%autochangelog

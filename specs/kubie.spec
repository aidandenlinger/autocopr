%global debug_package %{nil}

Name:    kubie
Version: 0.24.1
Release: 1%{?dist}
Summary: A more powerful alternative to kubectx and kubens

License: Zlib
URL:     https://github.com/sbstp/kubie
Source0: https://raw.githubusercontent.com/sbstp/kubie/refs/tags/v%{version}/README.md
Source1: https://raw.githubusercontent.com/sbstp/kubie/refs/tags/v%{version}/LICENSE
Source2: https://raw.githubusercontent.com/sbstp/kubie/refs/tags/v%{version}/completion/kubie.bash
Source3: https://raw.githubusercontent.com/sbstp/kubie/refs/tags/v%{version}/completion/kubie.fish

BuildRequires: wget

%description
%{summary}

%prep
cp %{SOURCE0} CONFIGURATION.md
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

%install
wget https://github.com/sbstp/kubie/releases/download/v%{version}/kubie-linux-amd64
install -p -D %{name}-linux-amd64 %{buildroot}%{_bindir}/%{name}

# Shell completion
install -pvD -m 0644 %{name}.bash %{buildroot}%{bash_completions_dir}/%{name}.bash
install -pvD -m 0644 %{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish

%files
%doc CONFIGURATION.md
%license LICENSE
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}.bash
%{fish_completions_dir}/%{name}.fish

%changelog
%autochangelog

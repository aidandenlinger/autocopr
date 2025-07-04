%global debug_package %{nil}

# Inspired from https://github.com/aidandenlinger/autocopr/blob/main/specs/eza.spec with own changes

Name: eza
Version: 0.22.0
Release: 1%{?dist}
Summary: A modern alternative to ls

License: EUPL-1.2
URL: https://github.com/eza-community/eza
Source0: %{url}/releases/download/v%{version}/%{name}_x86_64-unknown-linux-gnu.tar.gz
Source1: %{url}/releases/download/v%{version}/completions-%{version}.tar.gz
Source2: %{url}/releases/download/v%{version}/man-%{version}.tar.gz
Source3: https://raw.githubusercontent.com/eza-community/eza/v%{version}/LICENSE.txt

BuildRequires: gzip

%description
%{summary}

%prep
%autosetup -c
# autosetup can't extract more than one tarball, extract manually
# https://github.com/rpm-software-management/rpm/issues/2495
%__rpmuncompress -x %{SOURCE1}
%__rpmuncompress -x %{SOURCE2}
cp %{SOURCE3} .

%build
gzip target/man-%{version}/*

%install
install -p -D %{name} %{buildroot}%{_bindir}/%{name}

# Shell completion
# Inspired by alacritty's spec build
install -v -p -D -m 0644 target/completions-%{version}/%{name} %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -v -p -D -m 0644 target/completions-%{version}/%{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish
install -v -p -D -m 0644 target/completions-%{version}/_%{name} %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

# Man pages
install -pvD -m 0644 target/man-%{version}/%{name}.1.gz %{buildroot}%{_mandir}/man1/%{name}.1.gz
install -pvD -m 0644 target/man-%{version}/%{name}_colors.5.gz %{buildroot}%{_mandir}/man5/%{name}_colors.5.gz
install -pvD -m 0644 target/man-%{version}/%{name}_colors-explanation.5.gz %{buildroot}%{_mandir}/man5/%{name}_colors-explanation.5.gz

%files
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}
%{zsh_completions_dir}/_%{name}
%{fish_completions_dir}/%{name}.fish
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man5/%{name}_colors.5.gz
%{_mandir}/man5/%{name}_colors-explanation.5.gz
%license LICENSE.txt

%changelog
%autochangelog


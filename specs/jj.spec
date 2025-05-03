%global debug_package %{nil}

Name:    jj
Version: 0.28.2
Release: 1%{?dist}
Summary: A Git-compatible VCS that is both simple and powerful

License: Apache v2.0
# https://github.com/martinvonz/jj/releases/download/v0.23.0/jj-v0.23.0-x86_64-unknown-linux-musl.tar.gz
URL: https://github.com/martinvonz/jj
Source: %{url}/releases/download/v%{version}/%{name}-v%{version}-x86_64-unknown-linux-musl.tar.gz
Source1: https://raw.githubusercontent.com/martinvonz/jj/v%{version}/README.md
Source2: https://raw.githubusercontent.com/martinvonz/jj/v%{version}/LICENSE

%description
%{summary}

%prep
%autosetup -c
cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} LICENSE

%build

%install
install -p -D %{name} %{buildroot}%{_bindir}/%{name}

%files
%doc CONFIGURATION.md
%license LICENSE
%{_bindir}/%{name}

%changelog
%autochangelog

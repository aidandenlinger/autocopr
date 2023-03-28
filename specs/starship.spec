%global debug_package %{nil}

Name: starship
Version: 1.13.1
Release: 1%{?dist}
Summary: Minimal, blazing-fast, and infinitely customizable prompt for any shell! â˜„ğŸŒŒï¸�

License: ISC
URL: https://github.com/starship/starship
Source: %{url}/releases/download/v%{version}/%{name}-x86_64-unknown-linux-gnu.tar.gz

%description
Minimal, blazing-fast, and infinitely customizable prompt for any shell! â˜„ğŸŒŒï¸�.


%prep
%autosetup -c

%build

%install
mkdir -p %{buildroot}%{_bindir}
install %{name} %{buildroot}%{_bindir}

%files
%{_bindir}/%{name}

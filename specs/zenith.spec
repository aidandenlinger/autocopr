%global debug_package %{nil}
%global raw_ghuc https://raw.githubusercontent.com/bvaisvil/zenith/

Name:    zenith
Version: 0.14.1
Release: 1%{?dist}
Summary: Sort of like top or htop but with zoom-able charts, CPU, GPU, network, and disk usage

License: MIT
# https://github.com/bvaisvil/zenith/releases/download/0.14.1/zenith.x86_64-unknown-linux-musl.tgz
URL:     https://github.com/bvaisvil/zenith
Source:  %{url}/releases/download/%{version}/%{name}.x86_64-unknown-linux-musl.tgz
Source1: %{raw_ghuc}/%{version}/README.md
Source2: %{raw_ghuc}/%{version}/LICENSE

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

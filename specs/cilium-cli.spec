%global debug_package %{nil}

Name:    cilium-cli
Version: 0.16.8
Release: 1%{?dist}
Summary: CLI to install, manage & troubleshoot Kubernetes clusters running Cilium

License: Apache-2.0
URL:     https://github.com/cilium/cilium-cli
Source0: https://github.com/cilium/cilium-cli/archive/v%{version}.tar.gz

BuildRequires: golang >= 1.20
BuildRequires: git

%description
CLI to install, manage & troubleshoot Kubernetes clusters running Cilium.

%prep
%autosetup -n cilium-cli-%{version}

%build
export CGO_CPPFLAGS="${CPPFLAGS}"
export CGO_CFLAGS="${CFLAGS}"
export CGO_CXXFLAGS="${CXXFLAGS}"
export CGO_LDFLAGS="${LDFLAGS}"
go build \
    -trimpath \
    -buildmode=pie \
    -mod=readonly \
    -modcacherw \
    -ldflags "-linkmode=external -X github.com/cilium/cilium-cli/internal/cli/cmd.Version=%{version}" \
    ./cmd/cilium

%install
rm -rf %{buildroot}
install -D -m 0755 cilium %{buildroot}%{_bindir}/cilium
install -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%verifyscript
%{buildroot}%{_bindir}/cilium version

%files
%{_bindir}/cilium
%license %{_datadir}/licenses/%{name}/LICENSE

%changelog
%autochangelog

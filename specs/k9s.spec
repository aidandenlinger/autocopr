%global debug_package %{nil}

Name:    k9s
Version: 0.27.4
Release: 1%{?dist}
Summary: Kubernetes CLI To Manage Your Clusters In Style!

License: Apache-2.0
URL:     https://github.com/derailed/k9s
Source0: https://github.com/derailed/k9s/archive/v%{version}.tar.gz

BuildRequires: golang >= 1.20
BuildRequires: git

%description
K9s provides a terminal UI to interact with your Kubernetes clusters. The aim of this project
is to make it easier to navigate, observe, and manage your applications in the wild.

%prep
tar -xf %{SOURCE0}

%build
cd k9s-%{version}
export CGO_CPPFLAGS="${CPPFLAGS}"
export CGO_CFLAGS="${CFLAGS}"
export CGO_CXXFLAGS="${CXXFLAGS}"
export CGO_LDFLAGS="${LDFLAGS}"
go build \
    -trimpath \
    -buildmode=pie \
    -mod=readonly \
    -modcacherw \
    -ldflags "-linkmode=external -X main.version=%{version}"

%install
rm -rf %{buildroot} && mkdir -p %{buildroot}%{_bindir}/ && cd k9s-%{version}
install -m 0755 k9s %{buildroot}%{_bindir}/k9s
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}/
install -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/

%verifyscript
%{buildroot}%{_bindir}/k9s version

%files
%{_bindir}/k9s
%license %{_datadir}/licenses/%{name}/LICENSE

%changelog
%autochangelog

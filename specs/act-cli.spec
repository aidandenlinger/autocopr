%global debug_package %{nil}
# Inspirated from https://github.com/goncalossilva/rpm-act/blob/main/act-cli.spec

Name:    act-cli
Version: 0.2.74
Release: 1%{?dist}
Summary: Run GitHub Actions locally.

License: MIT
URL:     https://github.com/nektos/act
Source0: https://github.com/nektos/act/archive/v%{version}.tar.gz

BuildRequires: golang >= 1.23
BuildRequires: git
Requires:      (moby or podman or docker or docker-ce or docker-ce-cli or docker-ee)

%description
`act` reads GitHub Actions workflows and determines the set of actions that
need to be run. It uses the Docker API to either pull or build the necessary
images, and determines the execution path based on the defined dependencies.
It then uses the Docker API to run containers for each action based on the
images prepared earlier. The environment variables and filesystem are all
configured to match what GitHub provides.

%prep
tar -xf %{SOURCE0} # TODO: Use autosetup instead

%build
cd act-%{version}
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
rm -rf %{buildroot} && mkdir -p %{buildroot}%{_bindir}/ && cd act-%{version}
install -m 0755 act %{buildroot}%{_bindir}/act
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}/
install -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/

%verifyscript
%{buildroot}%{_bindir}/act --version

%files
%{_bindir}/act
%license %{_datadir}/licenses/%{name}/LICENSE

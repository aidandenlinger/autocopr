%global debug_package %{nil}

Name:    msedit
Version: 1.2.0
Release: 1%{?dist}
Summary: A simple editor for simple needs.

License: MIT
URL:     https://github.com/microsoft/edit
Source0: %{url}/archive/v%{version}.tar.gz

# Standard Rust build dependencies
BuildRequires: rust
BuildRequires: rust-src
BuildRequires: cargo

%description
A simple editor for simple needs. Pays homage to the classic MS-DOS Editor,
but with a modern interface and input controls similar to VS Code. The goal
is to provide an accessible editor that even users largely unfamiliar with
terminals can easily use.

%prep
ls -larth
%autosetup -n edit-%{version}
ls -larth

%build
export RUSTC_BOOTSTRAP=1
cargo build --config .cargo/release.toml --release --verbose

%install
install -D -m 0755 target/release/edit %{buildroot}%{_bindir}/msedit
install -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
install -D -m 0644 README.md %{buildroot}%{_datadir}/doc/%{name}/README.md

%files
%{_bindir}/msedit
%license %{_datadir}/licenses/%{name}/LICENSE
%doc %{_datadir}/doc/%{name}/README.md

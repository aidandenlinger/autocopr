# Written by VarLad, thanks! https://gitlab.com/VarLad/rpm-specs/-/blob/main/zellij/zellij.spec
%global debug_package %{nil}

Name:       zellij
Version:    0.34.4
Release:    1%{?dist}
Summary:    A terminal workspace with batteries included.

License:    MIT
URL:        https://github.com/zellij-org/zellij
Source0:    %{url}/archive/refs/tags/v%{version}.tar.gz

%if 0%{?el8}
%else
BuildRequires: cargo >= 1.39
BuildRequires: rust >= 1.39
%endif
BuildRequires: gcc
BuildRequires: python3-devel

%description
Zellij is a workspace aimed at developers, ops-oriented people and anyone who loves the terminal. At its core, it is a terminal multiplexer (similar to tmux and screen), but this is merely its infrastructure layer. Zellij includes a layout system, and a plugin system allowing one to create plugins in any language that compiles to WebAssembly.


%prep
%autosetup -p1
%if 0%{?el8}
  curl https://sh.rustup.rs -sSf | sh -s -- --profile minimal -y
%endif


%install
export CARGO_PROFILE_RELEASE_BUILD_OVERRIDE_OPT_LEVEL=3
%if 0%{?el8}
  $HOME/.cargo/bin/cargo install --root=%{buildroot}%{_prefix} --path=.
%else
  cargo install --root=%{buildroot}%{_prefix} --path=.
%endif

rm -f %{buildroot}%{_prefix}/.crates.toml \
    %{buildroot}%{_prefix}/.crates2.json
strip --strip-all %{buildroot}%{_bindir}/*


%files
%license LICENSE.md
%doc README.md
%{_bindir}/zellij

# Written by VarLad, thanks! https://gitlab.com/VarLad/rpm-specs/-/blob/main/helix/helix.spec
%global debug_package %{nil}

Name:       helix
Version:    22.12
Release:    1%{?dist}
Summary:    A post-modern modal text editor.

License:    MPL-2.0
URL:        https://github.com/helix-editor/helix
Source0:    %{url}/releases/download/%{version}/helix-%{version}-source.tar.xz

BuildRequires: cargo
BuildRequires: rust
BuildRequires: gcc-c++

%description
A kakoune / neovim inspired editor, written in Rust.
The editing model is very heavily based on kakoune.
Features include Vim-like modal editing, multiple selections, built-in language server support and smart, incremental syntax highlighting and code editing via tree-sitter

%prep
tar -xf %{_sourcedir}/helix-%{version}-source.tar.xz -C %{_builddir}

%install
cargo build --release
HELIX_RUNTIME="$PWD/runtime" ./target/release/hx --grammar build
rm -rf ./runtime/grammars/sources
mkdir -p %{buildroot}%{_datadir}/helix
mkdir -p %{buildroot}%{_libexecdir}
mv ./runtime %{buildroot}%{_datadir}/helix
mv ./target/release/hx %{buildroot}%{_libexecdir}/hx
strip --strip-all %{buildroot}%{_libexecdir}/hx
mkdir -p %{buildroot}%{_datadir}/licenses/helix
mv ./LICENSE %{buildroot}%{_datadir}/licenses/helix/LICENSE
mkdir -p %{buildroot}%{_docdir}/helix
mv README.md %{buildroot}%{_docdir}/helix/README.md

mkdir -p %{buildroot}%{_bindir}
touch %{buildroot}%{_bindir}/hx
cat >> %{buildroot}%{_bindir}/hx <<EOF
#!/usr/bin/env sh

HELIX_RUNTIME="%{_datadir}/helix/runtime" exec %{_libexecdir}/hx "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/hx

%files
%license LICENSE
%doc README.md
%{_bindir}/hx
%{_libexecdir}/hx
%{_datadir}/helix/runtime/

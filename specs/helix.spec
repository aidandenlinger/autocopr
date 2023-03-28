# Slightly reworked from VarLad's version, thanks! https://gitlab.com/VarLad/rpm-specs/-/blob/main/helix/helix.spec
%global debug_package %{nil}

Name:       helix
Version:    22.12
Release:    1%{?dist}
Summary:    A post-modern modal text editor.

License:    MPL-2.0
URL:        https://github.com/helix-editor/helix
Source:     %{url}/releases/download/%{version}/%{name}-%{version}-x86_64-linux.tar.xz

%description
A kakoune / neovim inspired editor, written in Rust.
The editing model is very heavily based on kakoune.
Features include Vim-like modal editing, multiple selections, built-in language server support and smart, incremental syntax highlighting and code editing via tree-sitter

%prep
%autosetup -n %{name}-%{version}-x86_64-linux

%build

%install
mkdir -p %{buildroot}%{_datadir}/helix
mkdir -p %{buildroot}%{_libexecdir}

mv runtime %{buildroot}%{_datadir}/helix
mv hx %{buildroot}%{_libexecdir}/hx

mkdir -p %{buildroot}%{_datadir}/licenses/helix
mv LICENSE %{buildroot}%{_datadir}/licenses/helix
mkdir -p %{buildroot}%{_docdir}/helix
mv README.md %{buildroot}%{_docdir}/helix

mkdir -p %{buildroot}%{_bindir}
touch %{buildroot}%{_bindir}/hx
cat >> %{buildroot}%{_bindir}/hx <<EOF
#!/usr/bin/sh

HELIX_RUNTIME="%{_datadir}/helix/runtime" exec %{_libexecdir}/hx "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/hx

%files
%license %{_datadir}/licenses/helix/LICENSE
%doc %{_docdir}/helix/README.md
%{_bindir}/hx
%{_libexecdir}/hx
%{_datadir}/helix/runtime/

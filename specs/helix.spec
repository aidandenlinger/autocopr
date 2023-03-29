# Slightly reworked from VarLad's version, thanks! https://gitlab.com/VarLad/rpm-specs/-/blob/main/helix/helix.spec
%global debug_package %{nil}

Name:       helix
Version:    22.12
Release:    2%{?dist}
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
# Runtime, holds language grammars/etc
mkdir -p %{buildroot}%{_datadir}/helix
mv runtime %{buildroot}%{_datadir}/helix

# Helix binary, but in libexec because we don't directly call it
install -p -D hx %{buildroot}%{_libexecdir}/hx

# Acutal binary we call that uses the runtime folder
mkdir -p %{buildroot}%{_bindir}
touch %{buildroot}%{_bindir}/hx
cat >> %{buildroot}%{_bindir}/hx <<EOF
#!/usr/bin/sh

HELIX_RUNTIME="%{_datadir}/helix/runtime" exec %{_libexecdir}/hx "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/hx

# License and README
install -p -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/helix/LICENSE
install -p -D -m 0644 README.md %{buildroot}%{_docdir}/helix/README.md

# Shell completion
# Inspired by alacritty's spec build
install -p -D -m 0644 contrib/completion/hx.bash %{buildroot}%{_datadir}/bash-completion/completions/hx
install -p -D -m 0644 contrib/completion/hx.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/hx.fish
install -p -D -m 0644 contrib/completion/hx.zsh %{buildroot}%{_datadir}/zsh/site-functions/_hx

%files
%license %{_datadir}/licenses/helix/LICENSE
%doc %{_docdir}/helix/README.md
%{_bindir}/hx
%{_libexecdir}/hx
%{_datadir}/helix/runtime/
%{_datadir}/bash-completion/completions/hx
%{_datadir}/fish/vendor_completions.d/hx.fish
%{_datadir}/zsh/site-functions/_hx

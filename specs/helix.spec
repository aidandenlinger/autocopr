# Slightly reworked from VarLad's version, thanks! https://gitlab.com/VarLad/rpm-specs/-/blob/main/helix/helix.spec
%global debug_package %{nil}

Name:       helix
Version: 23.10
Release: 1%{?dist}
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
mkdir -pv %{buildroot}%{_libexecdir}/%{name}
mv -v runtime %{buildroot}%{_libexecdir}/%{name}

# Helix binary, store in libexec so runtime is in the same folder and helix will use it
# https://github.com/helix-editor/helix/wiki/Troubleshooting#missing-syntax-highlighting
install -v -p -D hx %{buildroot}%{_libexecdir}/%{name}/hx

# Link hx to bin
mkdir -v %{buildroot}%{_bindir}
ln -srv %{buildroot}%{_libexecdir}/%{name}/hx %{buildroot}%{_bindir}/hx

# Shell completion
# Inspired by alacritty's spec build
install -v -p -D -m 0644 contrib/completion/hx.bash %{buildroot}%{_datadir}/bash-completion/completions/hx
install -v -p -D -m 0644 contrib/completion/hx.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/hx.fish
install -v -p -D -m 0644 contrib/completion/hx.zsh %{buildroot}%{_datadir}/zsh/site-functions/_hx

%files
%license LICENSE
%doc README.md
%{_bindir}/hx
%{_libexecdir}/%{name}
%{_datadir}/bash-completion/completions/hx
%{_datadir}/fish/vendor_completions.d/hx.fish
%{_datadir}/zsh/site-functions/_hx

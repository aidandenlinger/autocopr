%global debug_package %{nil}

Name:    uv
Version: 0.5.1
Release: 1%{?dist}
Summary: An extremely fast Python package and project manager, written in Rust.

License:    MIT
URL:        https://github.com/astral-sh/uv
Source:     %{url}/releases/download/%{version}/%{name}-x86_64-unknown-linux-musl.tar.gz
Source1:    https://raw.githubusercontent.com/astral-sh/uv/%{version}/README.md

%description
Highlights
🚀 A single tool to replace pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, and more.
⚡️ 10-100x faster than pip.
🐍 Installs and manages Python versions.
🛠️ Runs and installs Python applications.
❇️ Runs scripts, with support for inline dependency metadata.
🗂️ Provides comprehensive project management, with a universal lockfile.
🔩 Includes a pip-compatible interface for a performance boost with a familiar CLI.
🏢 Supports Cargo-style workspaces for scalable projects.
💾 Disk-space efficient, with a global cache for dependency deduplication.
⏬ Installable without Rust or Python via curl or pip.
🖥️ Supports macOS, Linux, and Windows.
uv is backed by Astral, the creators of Ruff.

%prep
%autosetup -c -n %{name}

cp %{SOURCE1} CONFIGURATION.md

%build

%install
# Ensure the source binary is in the expected location
install -p -D %{name}-x86_64-unknown-linux-musl/%{name} %{buildroot}%{_bindir}/%{name}

%files
%doc CONFIGURATION.md
%{_bindir}/%{name}

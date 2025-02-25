%global debug_package %{nil}

Name:    lua-language-server
Version: 3.13.6
Release: 1%{?dist}
Summary: A language server that offers Lua language support - programmed in Lua

License: MIT
URL:     https://github.com/LuaLS/lua-language-server
Source:  %{url}/releases/download/%{version}/%{name}-%{version}-linux-x64-musl.tar.gz
Source1: https://raw.githubusercontent.com/LuaLS/lua-language-server/%{version}/README.md
Source2: https://raw.githubusercontent.com/LuaLS/lua-language-server/%{version}/LICENSE
BuildRequires: fdupes
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libstdc++-static

%description
%{summary}

%prep
%autosetup -c
cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} LICENSE

%install
install -d -m 0755 %{buildroot}%{_libexecdir}/%{name}
cp -av bin/* %{buildroot}%{_libexecdir}/%{name}
install -d -m 0755 %{buildroot}%{_datadir}/%{name}
cp -av \
    debugger.lua \
    main.lua \
    locale \
    script \
    meta \
    %{buildroot}%{_datadir}/%{name}/

ls -la %{buildroot}%{_datadir}/%{name}/
install -d -m 0755 %{buildroot}%{_bindir}

%files
%doc CONFIGURATION.md
%license LICENSE
%{_libexecdir}/%{name}/
%{_datadir}/%{name}/

%changelog
%autochangelog

%global debug_package %{nil}

Name:       mise
Version: 2024.11.6
Release: 1%{?dist}
Summary:    dev tools, env vars, task runner

License:    MIT
URL:        https://github.com/jdx/mise
Source:     %{url}/releases/download/v%{version}/%{name}-v%{version}-linux-x64-musl.tar.gz
Source1:    https://raw.githubusercontent.com/jdx/mise/v%{version}/README.md
Source2:    https://raw.githubusercontent.com/jdx/mise/v%{version}/completions/mise.bash
Source3:    https://raw.githubusercontent.com/jdx/mise/v%{version}/completions/mise.fish

%description
mise (pronounced "meez") or "mise-en-place" is a development environment setup tool. The name refers to a French culinary phrase that roughly translates to "setup" or "put in place". The idea is that before one begins cooking, they should have all their utensils and ingredients ready to go in their place.
mise does the same for your projects. Using its mise.toml config file, you'll have a consistent way to setup and interact with your projects no matter what language they're written in.
Its functionality is grouped into 3 categories described below.
mise installs and manages dev tools/runtimes like node, python, or terraform both simplifying installing these tools and allowing you to specify which version of these tools to use in different projects. mise supports hundreds of dev tools.
mise manages environment variables letting you specify configuration like AWS_ACCESS_KEY_ID that may differ between projects. It can also be used to automatically activate a Python virtualenv when entering projects too.
mise is a task runner that can be used to share common tasks within a project among developers and make things like running tasks on file changes easy.

%prep
%autosetup -n mise

cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} .
cp %{SOURCE3} .

%build

%install
# Ensure the source binary is in the expected location
install -p -D bin/%{name} %{buildroot}%{_bindir}/%{name}

# Shell completions
install -pvD -m 0644 %{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
install -pvD -m 0644 %{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish

%files
%doc CONFIGURATION.md
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}
%{fish_completions_dir}/%{name}.fish

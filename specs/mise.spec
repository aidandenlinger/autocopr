%global debug_package %{nil}

Name:       mise
Version:    2024.11.4
Release:    1%{?dist}
Summary:    dev tools, env vars, task runner

License:    MIT
# https://github.com/jdx/mise/releases/download/v2024.11.4/mise-v2024.11.4-linux-x64-musl.tar.gz
URL:        https://github.com/jdx/mise
Source:     %{url}/releases/download/v%{version}/%{name}-v%{version}-linux-x64-musl.tar.gz
#Source1:    https://raw.githubusercontent.com/jdx/mise/v%{version}/docs/MANPAGE.md

BuildRequires: pandoc

%description
mise (pronounced "meez") or "mise-en-place" is a development environment setup tool. The name refers to a French culinary phrase that roughly translates to "setup" or "put in place". The idea is that before one begins cooking, they should have all their utensils and ingredients ready to go in their place.
mise does the same for your projects. Using its .mise.toml config file, you'll have a consistent way to setup and interact with your projects no matter what language they're written in.
Its functionality is grouped into 3 categories described below.
mise installs and manages dev tools/runtimes like node, python, or terraform both simplifying installing these tools and allowing you to specify which version of these tools to use in different projects. mise supports hundreds of dev tools.
mise manages environment variables letting you specify configuration like AWS_ACCESS_KEY_ID that may differ between projects. It can also be used to automatically activate a Python virtualenv when entering projects too.
mise is a task runner that can be used to share common tasks within a project among developers and make things like running tasks on file changes easy.

%prep
# This source file doesn't have a high level directory, so create one
%autosetup -c
# Get the manpage in the build dir
#cp %{SOURCE1} .

#%build
# Generate shell completions
#./%{name} setup --generate-completion bash > %{name}.bash
#./%{name} setup --generate-completion zsh > _%{name}
#./%{name} setup --generate-completion fish > %{name}.fish

# Generate manpage (https://eddieantonio.ca/blog/2015/12/18/authoring-manpages-in-markdown-with-pandoc/)
#pandoc --standalone --to man MANPAGE.md | gzip -c > %{name}.1.gz

%install
install -p -D %{name} %{buildroot}%{_bindir}/%{name}

# Shell completions
#install -pvD -m 0644 %{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
#install -pvD -m 0644 _%{name} %{buildroot}%{zsh_completions_dir}/_%{name}
#install -pvD -m 0644 %{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish

# Man page
#install -pvD -m 0644 %{name}.1.gz %{buildroot}%{_mandir}/man1/%{name}.1.gz

%files
%{_bindir}/%{name}
#%{bash_completions_dir}/%{name}
#%{zsh_completions_dir}/_%{name}
#%{fish_completions_dir}/%{name}.fish
#%{_mandir}/man1/%{name}.1.gz

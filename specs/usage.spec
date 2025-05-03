%global debug_package %{nil}

Name:    usage
Version: 2.1.1
Release: 1%{?dist}
Summary: A specification for CLIs

License:    MIT
URL:        https://github.com/jdx/usage
Source:     %{url}/releases/download/v%{version}/%{name}-x86_64-unknown-linux-musl.tar.gz
Source1:    https://raw.githubusercontent.com/jdx/usage/v%{version}/README.md

%description
Usage is a spec and CLI for defining CLI tools.
Arguments, flags, environment variables, and config files can all be defined in a Usage spec.
It can be thought of like OpenAPI (swagger) for CLIs.
Here are some potential reasons for defining your CLI with a Usage spec:

- Generate autocompletion scripts
- Generate markdown documentation
- Generate man pages
- Use an advanced arg parser in any language
- Scaffold one spec into different CLI frameworks—even different languages

%prep
%autosetup -c -n %{name}

cp %{SOURCE1} CONFIGURATION.md

%build

%install
# Ensure the source binary is in the expected location
install -p -D %{name} %{buildroot}%{_bindir}/%{name}

%files
%doc CONFIGURATION.md
%{_bindir}/%{name}

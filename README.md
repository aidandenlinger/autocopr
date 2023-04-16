# AutoCOPR

Check Github Releases daily for new project versions and updates spec files
accordingly for automatic COPR updates.

AutoCOPR provides a script to check all spec files in a folder, and for those
with github urls, update the version number to the latest version. This repo
integrates that script with Github Actions to automatically update the versions
every 24 hours and automatically trigger a rebuild on COPR. 

TL;DR: Automatic version bumper for projects that use Github Releases :)

## Table of Contents

- [Background](#background)
- [Install/Usage](#installusage)
  - [Using This COPR Repository](#using-this-copr-repository)
  - [The `autocopr.py` Program](#the-autocoprpy-program)
  - [Integrating with Github Actions and COPR Automatic Builds](#integrating-with-github-actions-and-copr-automatic-builds)
- [Thanks](#thanks)
- [Contributing](#contributing)
- [License](#license)

## Background
[Fedora](https://fedoraproject.org/) is a Linux distribution that uses
the [`dnf`](https://docs.fedoraproject.org/en-US/quick-docs/dnf/) package
manager to install, update, and remove packages/software.
[Copr](https://copr.fedorainfracloud.org/) (which stands for Community
Projects) is a build system that takes a
[SPEC file](https://rpm-packaging-guide.github.io/#what-is-a-spec-file) and
builds an [RPM package](https://rpm-packaging-guide.github.io/#what-is-an-rpm)
that can be installed with `dnf`. COPR provides an easy way to integrate user
packages that aren't in the default Fedora repos into the Fedora package
management system. [Github Actions](https://github.com/features/actions) is
Github's Continuous Integration/Development system that runs actions based on
Github events. In our case, we can use it to run a script every 24 hours.

There are a few Rust CLI tools I like to use that aren't in the default
repository (you can read more about some of the interesting challenges
that come with packaging Rust applications
[here](https://lwn.net/Articles/912202/)). There are some wonderful COPR repos
maintained by others (thank you to [Varlad](https://gitlab.com/VarLad/rpm-specs)
and [Atim](https://copr.fedorainfracloud.org/coprs/atim)), but the workflow of
having to wait for the version to be manually bumped seemed to scream for
automation, and here we are.

These specs use the binary packages provided by the project mantainers to try
and ensure the build won't fail, as well as not waste energy compiling something
that is already compiled. However, this requires that you trust the project
maintainers to provide correct binaries. If you don't, please create your own
AutoCOPR that builds from source or explore other alternatives below.

There are several valid alternatives to a system like this:
- [`cargo-binstall`](https://github.com/cargo-bins/cargo-binstall) or
  installing from source with
  [`cargo install`](https://doc.rust-lang.org/cargo/commands/cargo-install.html)
  would use `cargo` as a package manager to download and update these
  programs. This is more idiomatic and certainly easier! However, for me I
  really value having one source of updates for my system so I don't need to
  remember all the different sources, so integrating with `dnf` is ideal.
- There are other COPR repositories that build these. You can go to
  [Copr](https://doc.rust-lang.org/cargo/commands/cargo-install.html), type in
  a program name, hit the arrow to filter for "package name", and go explore the
  projects and repositories! *Be sure to check a build for its spec file to see
  what it's doing!* These often build the packages from source and are actually
  maintained by humans, which should provide a crucial layer of security and
  insurance that the package builds and doesn't mess anything up! However, they
  can also take a bit longer to update and I will take any opportunity to
  over-engineer a solution for something that is barely a problem.

## Install/Usage
There's a few different ways to use this repo, so each one will get its own
section.

### Using This COPR Repository

#### Install
> **Warning**
> This repository is not checked by humans! It automatically updates when a new
> Github release is out and packages the binary package. If this repo or the
> source projects are compromised, this repo will blindly push that software.
> Check all updates before installing them on your system. By adding this repo
> and installing any packages, you are trusting the source project, me, and my
> code. If you do not trust this chain, please make your own autoCOPR or use an
> alternative solution.

You can view the COPR repo on the web
[here](https://copr.fedorainfracloud.org/coprs/adenl/github-releases/).

On a Fedora x86_64 system, to add this COPR repository with the packages in
`specs`, run

```bash
sudo dnf copr enable adenl/github-releases 
```

#### Usage
With the repository installed, you can install like regular from `dnf` - commands
like `sudo dnf install zellij` or `sudo dnf remove zellij` will work as expected
and you will receive updates through GNOME Software or `sudo dnf upgrade`.

See all packages on
[Copr](https://copr.fedorainfracloud.org/coprs/adenl/github-releases/packages/)
or by looking in the [specs folder](specs).

### The `autocopr.py` Program
The `autocopr.py` program (in the [`autocopr` folder](autocopr)) checks all
`.spec` files in the given directory and updates the versions to the latest
Github Release. This doesn't need to be integrated with CI - this can be run
locally to update any compatible spec files automatically.

#### Install

Clone the repo, consider making a
[virtual environment](https://docs.python.org/3/library/venv.html), and run

```shell
python -m pip install -r requirements.txt
```

to install the necessary dependencies.

#### Usage

```shell
python autocopr/autocopr.py
```

By default, running the script will
- check all .spec files in the current working directory 
- if they have github urls, query for the latest release.
- If the spec file has the latest version, move to next file
- If it is not up to date, move the current spec to have a .bk suffix
  and write a new .spec file with the new version and release set to 1.
- When done, print a summary of the updates.

You can specify the directory to search for specs in, for instance with this
repo it would be better to run

```shell
python autocopr/autocopr.py specs
```

to only search the `specs` folder.

There are a few flags:
- `--help` will print all the flags and stop.
- `-d / --dry-run` will not edit any files, and only print if files are
  outdated.
- `-v / --verbose` will print all information to stdout.
- `-i / --in-place` will not keep a backup - it will just edit the file.
  If you have a git repository with the current versions committed, this
  is safe (and probably preferable) to use since you can restore the specs
  to their previous versions.
- `-p / --push` will push all spec file updates to the repo with a COPR
  friendly tag for each. This is good for integrating with Github Actions.
  However, undoing this is annoying since you either need to undo the commits
  and force push, or make a new commit to restore the original state.

The command the Github Action runs is

```shell
python autocopr/autocopr.py --verbose --in-place --push specs
```

which means that it will print all info to standard out, will not create
backups, will push all spec file changes, and only searches the `specs` folder
for spec files.

### Integrating with Github Actions and COPR Automatic Builds
This repo has a Github Action at .github/workflows/update.yml that runs the
script every 24 hours. This process is detailed much further in
[DOCS.md](DOCS.md), but if you know what you're doing here's a quick summary:

- Read through [`autocopr.py`](autocopr/autocopr.py) and the
  [Github Actions workflow](.github/workflows/update.yml) to make sure you
  understand and trust what this is doing
- Fork this repository (button in the top right)
- Go to Settings -> Actions -> General, scroll to the bottom and set Workflow
  Permissions to "Read and write permissions". This allows the Github workflow
  to make pushes to the repo.
- Empty the `specs` folder and put your own specs in.
- Create a COPR repository, set up the packages for autobuild, and add its
  webhook to this repo to create automatic builds (more details in
  [DOCS.md](DOCS.md)).
- Rebuild all packages to get the initial builds.
- Add the COPR repo on your system.

You're done! The action will run at 00:00 UTC automatically, and you can also
run it manually from the Actions -> Update spec files -> "Run Workflow" button.

## Thanks
- [VarLad](https://gitlab.com/VarLad/rpm-specs) for writing the original
  [Zellij](https://zellij.dev/) and [Helix](https://helix-editor.com/) specs!
- [Atim](https://copr.fedorainfracloud.org/coprs/atim/starship/) for writing the
  original [Starship](https://starship.rs/) spec!
- The [python-rpm-spec](https://github.com/bkircher/python-rpm-spec) project -
  I needed to modify the spec so I didn't bring in this whole project, but this
  was a great resource!

## Contributing
Please feel free to leave any issues if you have questions about creating your
own AutoCOPR!

I'm willing to accept PRs for existing specs if they have issues, but I'm not
interested in adding more packages or adding more architectures than what I'm
already doing. I only want to be pushing packages for programs I'm currently
using - if there are issues with packages or architectures I'm not using, I'd
be unaware of those issues, and since this repo is automated the issues could
go undiscovered for a long time. Please feel free to make your own repo though!

## License
MIT

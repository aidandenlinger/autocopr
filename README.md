# AutoCOPR

Check or update RPM spec files to the project's latest version released on Github.

AutoCOPR is a Github Action (or standalone Python script) that checks all
spec files within a folder, and for those with github urls, checks the version
number. Depending on the mode, it can then
- error out to alert you there are updates, or
- update the spec file with the latest version, or
- push a commit with an associated tag for COPR to start building an update.

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

See my [autocopr-specs repo] for an example of using AutoCOPR to automate
updates.

There are several valid alternatives to receive updates for packages not in
the Fedora repos:
- [`cargo-binstall`](https://github.com/cargo-bins/cargo-binstall) or
  installing from source with
  [`cargo install`](https://doc.rust-lang.org/cargo/commands/cargo-install.html)
  would use `cargo` as a package manager to download and update Rust
  programs. This is more idiomatic and certainly easier! However, for me I
  really value having one source of updates for my system so I don't need to
  remember all the different sources, so integrating with `dnf` is ideal.

- There are other COPR repositories. You can go to
  [COPR](https://doc.rust-lang.org/cargo/commands/cargo-install.html), type in
  a program name, hit the arrow to filter for "package name", and go explore the
  projects and repositories! *Be sure to check a build for its spec file to see
  what it's doing!* These often build the packages from source and are actually
  maintained by humans, which should provide a crucial layer of security and
  insurance that the package builds and doesn't mess anything up! However, they
  can also take a bit longer to update and I will take any opportunity to
  over-engineer a solution for something that is barely a problem.

I'd also like to point to [RelativeSure's autocopr
repo](https://github.com/RelativeSure/autocopr) as a downstream repo using
these scripts in a structured manner. You may want to use it as inspiration for
additional features you could use (such as updating a README.md with version
numbers).

## Install

### As a Github Action

You'll need a Github repository of spec files. You can use my
[autocopr-specs repo] as an example. It also has a markdown file
noting how I write a specfile.

### As a Standalone Python Script

You'll also want to have a folder of spec files, although they don't need to be
on Github. See above for notes.

To run this on your system, you'll need [Python](https://www.python.org/) installed.
Check [pyproject.toml](./pyproject.toml) for the required Python version.

Clone the repo, consider making a
[virtual environment](https://docs.python.org/3/library/venv.html), and run

```shell
python -m pip install -r requirements.txt
```

to install the necessary dependencies.

## Usage

### As a Github Action

> [!NOTE]
> This Github action will create a cache named `autocopr-graphql-ids-<hash>`.
> This is normal. The action utilizes the GraphQL API, which
> [identifies repos via a global node id rather than the repo's
> name](https://docs.github.com/en/graphql/guides/using-global-node-ids). This
> cache stores those ids to reuse in the future.

You need to choose which mode to run the script in:

- `push`: Automated updates. If any specfile is outdated, write new specfiles,
  make a commit for each with an associated tag, and push it to the repo.

- `check`: Manual updates. The job succeeds if all specfiles are up to date
  and fails if any are outdated. This mode does not write new files or push any
  updates - updating the specfile requires manual action. This mode is more secure
  since the action is read-only.

For additional details and options, see [action.yml](./action.yml).


#### Push Mode

Here's an example action for push mode:

```yaml
name: Update spec files
on:
  # Allows for manually running an update from the actions tab
  workflow_dispatch:

  schedule:
    # Runs every day at ~12am UTC - see https://crontab.guru/
    - cron: '0 0 * * *'

# Revoke all default permissions
permissions: {}

jobs:
  update:
    name: update
    runs-on: ubuntu-latest
    permissions:
      # needed to push commits to this repo
      # see `check` mode if you don't want to give this permission
      contents: write

    steps:
      - uses: actions/checkout@v5

      - uses: aidandenlinger/autocopr@v1 # Or a specific release tag, or commit
        with:
          mode: "push"
```

With push mode, you most likely want to integrate this with a COPR repo. This
process is detailed further in [COPR.md](COPR.md), but if you know what you're
doing here's a quick summary:

- Create a Github Action that uses "push" mode. You likely want this to run
  on a schedule.

- Create a COPR repository, set up the packages for autobuild, and add its
  webhook to this repo to create automatic builds (more details in
  [COPR.md](COPR.md)).

- Rebuild all packages on COPR to get the initial builds.

- Add the COPR repo to your system.

That's it! Whenever the Github Action is run, if the project has a new release
the specfile will be updated and pushed with a cooresponding tag. This will
send a webhook to COPR, and start an autobuild for the associated package.

#### Check Mode Example Action

```yaml
name: Check specfile updates
on:
  # Allows for manually running an update from the actions tab
  workflow_dispatch:

  schedule:
    # Runs every day at ~12am UTC - see https://crontab.guru/
    - cron: '0 0 * * *'

# Revoke all default permissions
permissions: {}

jobs:
  update:
    name: update
    runs-on: ubuntu-latest
    permissions:
      # Only required if the repo is private.
      # If it's a public repo, you don't need any permissions and can delete this section!
      contents: read

    steps:
      - uses: actions/checkout@v5

      - uses: aidandenlinger/autocopr@v1 # Or a specific release tag, or commit
        with:
          mode: "check"
```

### As a Standalone Python Script

```shell
python main.py <folder-with-spec-files>
```

will run the `main.py` script, searching for spec files in the provided directory.
If you do not provide a folder, it will search the current directory.

By default, running the script will
- check all .spec files recursively in the provided directory
- if they have github urls, query for the latest release.
- If the spec file has the latest version, move to next file
- If it is not up to date, move the current spec to have a .bk suffix
  and write a new .spec file with the new version and release set to 1.
- When done, print a summary of the updates.

There are a few flags:
- `--help` will print all the options.

- `--mode <MODE>` determines how the script should behave. `push` will push
  commits with updates, `check` is read-only and will fail if any scripts
  have updates, `update` will write new spec files but not push anything, and
  `dry-run` acts like `check` but will always exit with 0 regardless of updates.
  See the `--help` output for more details.

- `-v / --verbose` will print additional information to stdout.

- `--github-token` allows you to pass in a github token to use the GraphQL API,
  which makes less requests to the Github API and therefore is often faster.
  It can also be set with the `GITHUB_TOKEN` environment variable (you may want
  to do this to keep the token out of your terminal command history). Any token
  defined with the command line flag will take priority over the environment
  variable.  Using the GraphQL api will create a `graphql_id_cache.json` file
  with your specs that stores GraphQL ids for each repo, this should be left
  alone for quicker GraphQL queries.
    - alternatively, `--rest` forces usage of the REST API, even with a github
      token provided. You'd only want to do this if you're adding a new feature
      and want to specifically work with the REST API.

## Thanks
- The [python-rpm-spec](https://github.com/bkircher/python-rpm-spec) project -
  I needed to modify the spec so I didn't bring in this whole project, but this
  was a great resource!
- [RelativeSure's autocopr repo](https://github.com/RelativeSure/autocopr) for
  doing really cool things downstream, check it out!

## Contributing
Please feel free to leave any issues if you have questions about creating your
own AutoCOPR! I'm open to PRs to the autocopr program to make it better or add
new features.


## License
MIT

[autocopr-specs repo]: https://github.com/aidandenlinger/autocopr-specs

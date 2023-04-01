## Creating a Spec

I am *not* an experienced packager, but here's what worked for me.

I used [distrobox](https://github.com/89luca89/distrobox) to have a separate
Fedora installation to install these RPMs on to not pollute my distro. You'll
have to remove the ``~/rpmbuild` dir when you're done, but otherwise it just
works.

I'm not building the packages, I'm just linking the binaries from Github
Releases. If your project pushes a binary directly to Github Actions, you're in
luck! Look at some of the simple specs like [zellij.spec](specs/zellij.spec) as
an example. For an example of a more complicated spec, look at
[helix.spec](specs/helix.spec). The key process is setting the URL to the github
repo, the Source to the download of the binary you need and using macros like
%{version}, run %autosetup to deal with the source files (and use -c if the
download doesn't come with a top level directory), have an empty %build section
since you don't need to build anything, then finally make the needed _bindir and
run install to install the binary. Put the files you've installed in %files.

To test, use `rpmlint *your spec file*` to lint your file. Once it's good, run
`spectool -g -R -f *your spec file*` to download sources, then `rpmbuild -bb
*your spec file*` to build the rpm. If successful, try installing it with `sudo
dnf install ~/rpmbuild/RPMS/*path to your rpm*`. Try the binary, and if it works
you're set!

There was no real good source of documentation for spec files. Some random links
I did use were
- [Fedora Packaging Tutorial](https://docs.fedoraproject.org/en-US/package-maintainers/Packaging_Tutorial_GNU_Hello/)
- [Fedora RPM Macros](https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/)
- [RPM Packaging Guide](https://rpm-packaging-guide.github.io/)
- and a lot of random stack overflow questions.

## Github Actions
Be sure to go into the repo settings -> Actions -> Workflow permissions and set
it to "Read and write permissions" and save at the bottom of the page, so the
workflow can make commits.

The workflow doesn't run *right* at 00:00 UTC, but it will run within the hour.
This is more than fine since we just want it to run every 24 hours.

You can trigger the workflow manually by going to Actions and clicking on
"Update spec files". This could be useful if you've manually noticed that
something's updated and you want to update the spec without waiting for the
daily check.

## COPR Integration
TL;DR: Create a new COPR project and follow the Webhooks documentation [here](https://
docs.pagure.org/copr.copr/user_documentation.html#webhooks). I'll write exactly
what I did when following the documentation, but steps may have changed so check
the fedora documentation first!

- Create a new project. You don't need to fill out everything now, I just put
  the name and select the last three fedora versions as my chroot. You should
  fill this out later if you intend for it to be public.

- Go to Packages and hit "Create a New Package".
- Choose SCM, fill in the package name, clone url (which is the link to your
  repo), subdirectory (in this repo it's specs), and spec file.
- I left it as using rpkg.
- Click auto-rebuild.
- Hit save.

Repeat this process for all packages you want to build. You can alternatively
create a new project for each binary and this helps with discoverability, but
also means you have a ton of projects which can take longer to check. All up to
you!

You can quickly check that COPR is working by going to Builds and clicking
"Rebuild" to see if your build works.

To set up autobuilds:
- Go to settings -> integrations. You'll see your webhook url, copy the first one.
- Go to Github, go to settings / webhooks, and hit add webhook.
- Paste in the payload URL.
- Select application/json as content type.
- Select individual events, select branch/tag creation, and deselect push.
  - We don't want to fire the webhook on every commit, because some commits
    won't change this specific package! autocopr.py attaches the cooresponding
    tags when needed.

From that point, it just works! The Github Action will run every night, if
there's an update it'll push a commit with the cooresponding tag for the package
and send a webhook to COPR, COPR will launch a rebuild for the tags it receives,
and since the specs just package the binary there shouldn't be any errors :)
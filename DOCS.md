## Creating a Spec

I am *not* an experienced packager, but here's what worked for me.

I used [distrobox](https://github.com/89luca89/distrobox) to have a separate
Fedora installation to install these RPMs on to not pollute my distro. You'll
have to remove the ``~/rpmbuild` dir when you're done, but otherwise it just
works.

I'm not building the packages, I'm just linking the binaries from Github
Releases. Take a look at some of the specs to see how it got pieced together.
The key process is setting the URL to the github repo, the Source to the
download of the binary you need and using macros like %{version}, run %autosetup
to deal with the source files (and use -c if the download doesn't come with a
top level directory), have an empty %build section since you don't need to build
anything, then finally make the needed _bindir and run install to install the
binary. Put the files you've installed in %files.

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

You can trigger the workflow manually by going to Actions and clicking on
"Update spec files". This could be useful if you've manually noticed that
something's updated and you want to update the spec without waiting for the
daily check.
## Triggering Rebuilds on COPR
TL;DR: Create a new COPR project and follow the Webhooks documentation
[here](https://docs.pagure.org/copr.copr/user_documentation.html#webhooks).
I'll write exactly what I did when following the documentation, but steps may
have changed so check the fedora documentation first!

- Create a new project. You don't need to fill out everything now, I just put
  the name and select the last three fedora versions as my chroot. You should
  fill out the instructions if you intend for it to be public.

- Go to Packages and hit "Create a New Package".

- Choose SCM, fill in the package name, clone url (which is the link to your
  repo), subdirectory, and spec file.
  - I left it as using rpkg.

- Click auto-rebuild.

- Hit save.

Repeat this process for all packages you want to build. You can alternatively
create a new project for each binary and this helps with discoverability, but
also means you have a ton of projects which can take longer to check. All up to
you!

You can quickly check that COPR is retrieving the correct specfiles by going to
Builds and clicking "Rebuild" to see if your build works.

To set up autobuilds:
- Ensure your Github Action is in "push" mode.

- In COPR, go to Settings -> integrations. You'll see your webhook url, copy the first one.

- Go to Github, go to settings / webhooks, and hit add webhook.

- Paste in the payload URL.

- Select application/json as content type.

- Select individual events, select branch/tag creation, and deselect push.
  - We don't want to fire the webhook on every commit, because some commits
    won't change this specific package! The script attaches the cooresponding
    tags when needed.

From that point, it just works! Whenever the Github Action runs, if there's an
update it'll push a commit with the cooresponding tag for the package and send a
webhook to COPR. COPR will launch a rebuild for the tags it receives.

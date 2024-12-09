import logging
import subprocess
from pathlib import Path

import autocopr.cli
import autocopr.latestver
import autocopr.specdata
import autocopr.update


def main():
    args = autocopr.cli.create_parser().parse_args()
    root_dir = Path(args.directory)

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    if (
        args.push
        and subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"], capture_output=True
        ).returncode
        != 0
    ):
        # We're not in a git repository, exit
        logging.error("Cannot use --push when not running in a git repository")
        exit(1)

    specs = [
        parsed
        for spec in root_dir.glob("**/*.spec")
        if (parsed := autocopr.specdata.parse_spec(spec)) is not None
    ]

    latest_vers = autocopr.latestver.get_latest_versions(
        specs, root_dir / "graphql_id_cache.json", args.github_token, args.rest if args.rest else None
    )

    update_summary = [f"{'Name':15}\t{'Old Version':8}\tNew Version"]

    update_summary += [
        f"{spec.name:15}\t{spec.version:8}\t"
        f"{'(no update)' if spec.version == latest.ver else latest.ver}"
        for (spec, latest) in latest_vers
    ]

    if not args.dry_run:
        for spec, latest in latest_vers:
            if spec.version != latest.ver:
                autocopr.update.update_version(
                    spec, latest, inplace=args.in_place, push=args.push
                )

    print("\n".join(update_summary))

    if args.dry_run:
        print("To update the spec files, run again without the dry-run flag.")
    elif not args.in_place:
        print(
            "If any specs were updated, the original spec files now have a "
            ".bk suffix, and the spec files are updated with the newest "
            "version."
        )
    else:
        print("Any updates have been applied to the spec files.")


if __name__ == "__main__":
    main()

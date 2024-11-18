#!/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: $0 <copr webhook url> <github sha>"
	exit 1
fi

COPR_WEBHOOK=$1
GITHUB_SHA=$2

files_changed=$(git diff-tree --no-commit-id --name-only -r "$GITHUB_SHA" | grep '.spec')
echo "Files changed: $files_changed"

for file in $files_changed; do
	echo "Processing file: $file"
	filename=$(basename "$file")
	filename_without_ext="${filename%.*}"
	echo "Cleaned up $filename_without_ext by removing extension and specs folder"
	echo "Sending copr webhook of package $filename_without_ext"
	curl -i -H "Accept: application/json" -H "Content-Type:application/json" -X POST "$COPR_WEBHOOK/$filename_without_ext/"
done

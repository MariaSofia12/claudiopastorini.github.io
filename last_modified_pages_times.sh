#!/usr/bin/env bash
git ls-tree -r --name-only HEAD pages | while read filename; do echo "$(git log -1 --format="%ad" --date=iso -- "$filename") $filename"
done
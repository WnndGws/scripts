#!/bin/bash

# While there are unstaged files or diffs; do
while ! git diff --quiet -- . || git ls-files --others --exclude-standard | grep -q .; do
    # stage binary files first
    git diff --numstat . | grep -P '^\-\t\-' | cut -f3- | xargs -r git add --
    # mark untracked files as "intent to add" so they appear in --patch
    git ls-files --others --exclude-standard -z | xargs -0 -r git add -N --
    # interactively stage text hunks + untracked files (full-file additions)
    git add --patch . || break
    # reset -N on anything you skipped so it goes back to untracked
    git diff --name-only --diff-filter=M -z | xargs -0 -r git reset -q
    git commit
done

git push

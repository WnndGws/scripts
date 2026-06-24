#!/bin/zsh
### Find all commits in a repo with message 'try:' at the start, and cherry-pick them into one coherent commit

msg="try:"

# Switch to branch for safety
git checkout -b tmp-harvest

# Find all commits with the target message on current branch and formats to HASH
commits=$(git log --reverse --grep="$msg" --format='%H')

# @f splits by newlines, then # counts them
number_of_commits=${#${(@f)commits}}

if [[ $number_of_commits -eq 0 ]]; then
    echo "No commits found with message: $msg"
    return 1
fi

echo "Found $number_of_commits commit(s) with message '$msg':"
# Again split by @f
for c in "${(@f)commits}"; do
    echo "  $(git log -1 --oneline "$c")"
done
echo ""

# Stash any working changes up front
local had_changes=0
if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
    echo "Stashing your current working changes..."
    git stash push -m "autocommit-harvest-stash"
    had_changes=1
fi

# Reset HEAD to oldest 'try' so can interactively add lines until its at the current state
# Splits by newline, returns 1st element since zsh is 1 indexed not 0
git reset --soft "${${(@f)commits}[1]}"

# Unstage everything
git reset HEAD -- .

# Loop over changes and commit until there are no more unstaged bits
while ! git diff --quiet; do
    git commit --patch
done

git push
gh pr create --fill-verbose
# gh pr merge --rebase --delete-branch
gh pr merge --rebase
git pull

#!/bin/zsh

local msg="try:autocommit"
local new_msg="${1:-"harvested: combined autocommit changes"}"

# Find all commits with the target message
local commits=("$(git log --all --grep="$msg" --format='%H' 2>/dev/null)")

if [[ ${#commits[@]} -eq 0 ]]; then
    echo "No commits found with message: $msg"
    return 1
fi

echo "Found ${#commits[@]} commit(s) with message '$msg':"
for c in "${commits[@]}"; do
    echo "  $(git log -1 --oneline "$c")"
done
echo ""

while true; do
    # Check if there are any remaining diffs from these commits
    # that haven't been applied to the working tree yet
    local remaining=0
    for c in "${commits[@]}"; do
        # Diff each autocommit against its parent, check if any hunks
        # are still unaccounted for in the current branch
        local patch=$(git diff "$c^..$c" 2>/dev/null)
        if [[ -n $patch ]]; then
            remaining=$((remaining + 1))
        fi
    done

    if [[ $remaining -eq 0 ]]; then
        echo "All changes from '$msg' commits have been harvested."
        break
    fi

    echo "--- Remaining autocommit diffs: $remaining ---"
    echo "Cherry-picking each commit (no-commit) so you can select hunks..."

    # Stash any working changes first
    local had_changes=0
    if ! git diff --quiet || ! git diff --cached --quiet; then
        echo "Stashing your current working changes..."
        git stash push -m "autocommit-harvest-stash"
        had_changes=1
    fi

    for c in "${commits[@]}"; do
        echo ""
        echo ">>> Processing $(git log -1 --oneline "$c")"

        # Cherry-pick without committing
        if git cherry-pick -n "$c" 2>/dev/null; then
            # Let user interactively choose what to stage
            echo "Select changes to keep from this commit:"
            git add -p
        else
            echo "  (cherry-pick had conflicts or nothing to apply — skipping)"
            git cherry-pick --abort 2>/dev/null
        fi
    done

    # Commit whatever was staged
    if ! git diff --cached --quiet; then
        git commit -m "$new_msg"
        echo "Committed harvested changes."
    else
        echo "Nothing staged — nothing to commit."
    fi

    # Restore stashed changes
    if [[ $had_changes -eq 1 ]]; then
        echo "Restoring your stashed working changes..."
        git stash pop
    fi

    echo ""
    echo "Press Enter to continue harvesting, or 'q' to quit."
    read -k 1 answer
    if [[ $answer == "q" ]]; then
        break
    fi
done

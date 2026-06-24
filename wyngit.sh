#!/usr/bin/zsh

# Committing
git-try() {
    git add -p -A && git commit -m "try:${1:-autosave}"
}

git-wip() {
    git add -p -A && git commit -m "wip: $1"
}

# Undoing
git-undo() {
    local range=${1:-30}
    local shas=$(git log --oneline -"$range" --reverse | awk '{print $1}')
    if [ "$shas" = "" ]; then echo 'No commits found'; return 0; fi
    local drop=''
    for sha in "${shas[@]}"; do
        local msg=$(git log -1 --format='%s' "$sha")
        echo '' && \
            echo "--- $sha $msg ---" && \
            git diff "$sha^".."$sha" --stat && \
            echo '' && \
            git diff "$sha^".."$sha" && \
            echo '' && \
            echo -n '[k]eep / [d]rop / [q]uit? ' && \
            read -r action && \
            if [ "$action" = 'q' ]; then break; fi && \
            if [ "$action" = 'd' ]; then drop="$drop $sha"; echo "Dropped $sha"; else echo "Kept $sha"; fi
    done
    if [ "$drop" = "" ]; then echo 'Nothing dropped'; return 0; fi
    local kept=$(git log --oneline -"$range" --reverse | awk '{print $1}' | while read sha; do
            echo "$drop" | grep -qw "$sha" || echo "$sha"
    done)
    if [ "$kept" = "" ]; then echo 'All commits would be dropped, aborting'; return 1; fi
    local first_keep=$(echo "$kept" | head -1)
    local base=$(git rev-parse "$first_keep^")
    git reset --hard "$base" && \
        for sha in "${kept[@]}"; do git cherry-pick "$sha"; done && \
        echo "Dropped $(echo "$drop" | wc -w) commit(s). Rebased remaining commits."
}

# Recovering
git-backtrack() {
    git reset --hard HEAD@{"$1"}
}

# Reviewing
git-review() {
    local subcmd=${1:-try}
    case "$subcmd" in
        try|wip)
            ;;
        *)
            echo "Usage: git-review [try|wip]"
            echo "  git-review       (default: try)"
            echo "  git-review try"
            echo "  git-review wip"
            return 1
            ;;
    esac

    local range=${2:-50}
    local grep_pattern
    if [ "$subcmd" = "try" ]; then
        grep_pattern='try:autosave'
    else
        grep_pattern='^wip:'
    fi

    local shas=$(git log --oneline -"$range" --grep="$grep_pattern" --reverse | awk '{print $1}')
    if [ "$shas" = "" ]; then echo "No ${subcmd}: commits found"; return 0; fi
    local remaining=""
    for sha in "${shas[@]}"; do remaining="$remaining $sha"; done
    while true; do
        if [ "$(echo "$remaining" | tr -d ' ')" = "" ]; then echo 'All commits reviewed'; break; fi
        local picked=''
        local new_remaining=''
        for sha in "${remaining[@]}"; do
            local msg=$(git log -1 --format='%s' "$sha")
            echo '' && \
                echo "--- $sha $msg ---" && \
                git diff "$sha^".."$sha" --stat && \
                echo '' && \
                git diff "$sha^".."$sha" && \
                echo '' && \
                echo -n '[p]ick / [s]kip / [q]uit? ' && \
                read -r action && \
                if [ "$action" = 'q' ]; then return 0; fi && \
                if [ "$action" = 'p' ]; then picked="$picked $sha"; else new_remaining="$new_remaining $sha"; fi
        done
        remaining="$new_remaining"
        if [ "$picked" = "" ]; then continue; fi
        picked_arr=("$picked")
        first_sha=${picked_arr[0]}
        echo '' && \
            echo "Picked ${#picked_arr[@]} commits:" && \
            for sha in "${picked_arr[@]}"; do git log -1 --oneline "$sha"; done && \
            echo '' && \
            echo -n '[f]eat / [w]ip / [a]bort? ' && \
            read -r type && \
            if [ "$type" = 'f' ]; then local prefix='feat'; elif [ "$type" = 'w' ]; then local prefix='wip'; else echo 'Aborted'; continue; fi && \
            echo -n 'Message: ' && \
            read -r msg && \
            if [ "$msg" = "" ]; then echo 'Aborted'; continue; fi && \
            git reset --soft "$first_sha^" && \
            git commit -m "$prefix: $msg" && \
            echo "Squashed ${#picked_arr[@]} commits into: '$prefix: $msg'"
    done
    git bloat "$range"
}


# Feat branches
git-propose() {
    local feat_shas=$(git log --oneline --grep='^feat:' --reverse | awk '{print $1}')
    if [ "$feat_shas" = "" ]; then echo 'No feat: commits found on main'; return 0; fi
    local count=$(echo "$feat_shas" | wc -l)
    echo "$count feat: commit(s) to propose:"
    for sha in "${feat_shas[@]}"; do git log -1 --oneline "$sha"; done
    echo ''
    if [ "$1" != "" ]; then local branch="$1"; else
        echo -n 'Branch name [feat/]: ' && \
            read -r name && \
            local branch="feat/${name:-$(date +%Y%m%d-%H%M)}"
    fi
    local first_sha=$(echo "$feat_shas" | head -1)
    local base=$(git rev-parse "$first_sha^")
    git branch "$branch" "$base" && \
        for sha in "${feat_shas[@]}"; do git cherry-pick "$sha"; done && \
        echo "Created branch '$branch' with $count feat commit(s)" && \
        echo '' && \
        echo 'Removing feat commits from main...' && \
        local non_feat=$(git log --oneline --reverse | grep -v 'feat:' | awk '{print $1}')
    if [ "$non_feat" = "" ]; then echo 'No non-feat commits to keep'; return 1; fi
    local first_keep=$(echo "$non_feat" | head -1)
    local base_keep=$(git rev-parse "$first_keep^")
    git reset --hard "$base_keep" && \
        for sha in "${non_feat[@]}"; do git cherry-pick "$sha"; done && \
        echo "Main rebased without feat commits. Branch '$branch' is ready."
}

# Pull feat branches into main
git-ship() {
    local branches=$(git branch --list 'feat/*' | sed 's/^ *//')
    if [ "$branches" = "" ]; then echo 'No feat branches found'; return 0; fi
    echo 'Feat branches:'
    echo "$branches" | while read b; do echo "  $b"; done
    echo ''
    local picked=''
    for b in "${branches[@]}"; do
        echo -n "Include '$b'? [y]es / [n]o / [q]uit: " && \
            read -r action && \
            if [ "$action" = 'q' ]; then return 0; fi && \
            if [ "$action" = 'y' ]; then picked="$picked $b"; fi
    done
    if [ "$picked" = "" ]; then echo 'No branches selected'; return 0; fi
    echo -n 'PR branch name [pr/]: ' && \
        read -r name
    local pr_branch="pr/${name:-$(date +%Y%m%d-%H%M)}"
    git checkout main && \
        git checkout -b "$pr_branch" && \
        for b in "${picked[@]}"; do \
            echo "Merging $b..." && \
            git merge --no-ff "$b" || { echo "Merge conflict with $b. Resolve and commit, then re-run."; return 1; }; \
        done
    git push -u origin "$pr_branch" && \
        echo '' && \
        echo "Pushed PR branch '$pr_branch' with:" && \
        for b in "${picked[@]}"; do echo "  - $b"; done && \
        echo '' && \
        echo 'Cleaning up merged feat branches...' && \
        for b in "${picked[@]}"; do \
            git branch -d "$b"; \
            git push origin --delete "$b" 2>/dev/null; \
            echo "Deleted '$b'"; \
        done
    git checkout main && \
        echo 'Done. PR branch is on origin. Create the pull request on GitHub.'
}

# Debloating
git-bloat() {
    local total=$(git log --oneline -"${1:-30}" | wc -l)
    local autos=$(git log --oneline -"${1:-30}" | grep -c 'try:autosave' || true)
    local pct=$((autos * 100 / total))
    echo "$autos of $total commits are try:autosave ($pct%)"
}


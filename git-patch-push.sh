#!/bin/zsh

while [ "$(git diff --numstat | wc -l)" -gt 0 ]; do
    # Files with "-" in both column 1 and 2
    files=$(git diff --numstat | awk '$1 == "-" && $2 == "-" {print $3}')

    if [ "$files" != "" ]; then
        echo "Binary/untracked files available:"
        echo "$files" | nl -v1

        echo "Enter file numbers to add (space-separated, or 'all'):"
        read -r selection

        if [ "$selection" = "all" ]; then
            echo "$files" | xargs git add
        else
            echo "$files" | sed -n "$(echo "$selection" | tr ' ' ',' | tr -s ',')p" | xargs git add
        fi

        git commit -m "Add selected binary/untracked files"
    else
        # Process remaining files with patch mode
        echo "Processing remaining files with patch mode..."
        git add --patch
        git commit
    fi
done

git push

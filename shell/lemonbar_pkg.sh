#!/usr/bin/env zsh
## Checks how many packages need updating
## NOTE: USES BASHISMS

# Need to update or it wont know there are new packages

ignore_list="(^$(rg "^Ignore.*" /etc/pacman.conf | sed -e 's/^.*= //' -e 's/ /$)|(^/g')$)"

check_pkg() {
    sudo pikaur -Sy > /dev/null 2>&1

    pac=$(pacman -Qqu | rg --invert-match --count "$ignore_list")
    #pac=$(pacman -Qqu)
    if [ -n "$pac" ]; then

        pac=$(echo $pac | wc -l)
        # aur=$(pikaur -Qqu | wc -l)
        aur=$(pikaur -Qqu 2> /dev/null | rg --invert-match --count "$ignore_list")
        # Need to minus 1 since pikaur outputs a non-blank blank line
        #aur=$(awk -v a="$aur" 'BEGIN { printf a-1 }')
        aur=$(awk -v a="$aur" -v p="$pac" 'BEGIN { printf a-p }')

        #[ "$pac" = "0" ] && [ "$aur" = "0" ] && leader="L" || leader="H"
        echo "PH$pac  $aur"

    fi
}

check_pkg

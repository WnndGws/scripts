#!/usr/bin/env zsh
## Battery display in lemonbar
## Note: this uses bashisms so not strictly POSIX

FONT_COLOUR="#eee8d5" # white

print_state() {
    BAT_STRING=$(acpi | sed -n 1p)
    BAT_PERC=$(echo $BAT_STRING | grep --perl-regexp --only-matching '[0-9]+(?=%)')
    BAT_STATE=$(echo $BAT_STRING | grep --extended-regexp --only-matching '(Dis|Not )?[Cc]harging|Unknown|Full')
    TIME=$(echo $BAT_STRING | grep --extended-regexp --only-matching '[0-9]{2}:[0-9]{2}')

    if [ $BAT_STATE = "Not charging" ]; then
        TIME="Charged"
        BAT_PERC=100
        #else
        #TIME=$(acpi | sed -n 1p)
        #TIME=${TIME%:*}
        #TIME=${TIME##* }
    fi

    if [ "$BAT_STATE" = "Charging" ]; then
        ICON="" # fontawesome 'plug' (f1e6)
        UNDERLINE_COLOUR="#99c76c" # green
    elif [ "$BAT_STATE" = "Full" ]; then
        ICON="" # fontawesome 'plug' (f1e6)
        UNDERLINE_COLOUR="#99c76c" # green
        TIME="Charged"
    elif [ "$TIME" = "Charged" ]; then
        ICON="" # fontawesome 'plug' (f1e6)
        UNDERLINE_COLOUR="#99c76c" # green
    elif [ "$BAT_PERC" -gt 95 ]; then
        ICON=""
        UNDERLINE_COLOUR="#99c76c" # green
    elif [ "$BAT_PERC" -gt 75 ]; then
        ICON=""
        UNDERLINE_COLOUR="#99c76c" # green
    elif [ "$BAT_PERC" -gt 50 ]; then
        ICON=""
        UNDERLINE_COLOUR="#ffc24b" # yellow
    elif [ "$BAT_PERC" -gt 15 ]; then
        ICON=""
        UNDERLINE_COLOUR="#ffc24b" # yellow
    else
        ICON=""
        UNDERLINE_COLOUR="#e65350" # red
    fi

    printf "%s\n" "B[%{F$FONT_COLOUR}%{U$UNDERLINE_COLOUR} %{+u}${ICON} ${BAT_PERC}% (${TIME})%{-u} %{U-}%{F-}]"
}

check_state_change() {
    unset changed
    BAT_STRING=$(acpi | sed -n 1p)
    BAT_STATE_OLD=$(echo $BAT_STRING | grep --extended-regexp --only-matching '(Dis)?[Cc]harging')
    sleep 1
    BAT_STRING=$(acpi | sed -n 1p)
    BAT_STATE_NEW=$(echo $BAT_STRING | grep --extended-regexp --only-matching '(Dis)?[Cc]harging')

    if [[ "$BAT_STATE_OLD" != "$BAT_STATE_NEW" ]]; then
        changed=true
    fi
}

# Need to do initial print when script runs, otherwise it will wait until divisible by 5
print_state
while true; do
    check_state_change
    if [[ $changed == true ]]; then
        print_state
    fi
    SYS_TIME=$(date +"%M")
    if [[ $((SYS_TIME % 5)) == "1" ]]; then
        unset recently_changed
    fi
    # Check if remainder of Current time's mins is 0, then
    if [[ $((SYS_TIME % 5)) == "0" ]] && [[ $recently_changed != 1 ]]; then
        print_state
        recently_changed=1
    fi
done

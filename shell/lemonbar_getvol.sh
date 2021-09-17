#!/usr/bin/env sh
## Reads volume

getCurVol() { volume=$(amixer --card 2 get Headphone | rg --only-matching --pcre2 '(on|off)(?=]' | head -n1)
        if [ "$volume" = "off" ]; then
            leader="Vm"
            icon="ﱝ"
            volume=0
        else
            # If not text, then want number
            volume=$(($(amixer --card 2 get Headphone | rg --only-matching --pcre2 '\d{1,3}(?=\%)' | head -n1)))
            if [ "$volume" -gt 50 ]; then
                leader="VH"
                icon=""
            elif [ "$volume" -gt 25 ]; then
                leader="VM"
                icon=""
            else
                leader="VL"
                icon=""
            fi
        fi
}

# Need to print something, otherwise it waits for 1st event
getCurVol
printf "%s\n" "${leader}${icon} ${volume}%"

# Subscribe, and for each line print the current volume
alsactl monitor |\
    while read -r line; do
        getCurVol
        printf "%s\n" "${leader}${icon} ${volume}%"
    done

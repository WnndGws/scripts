#!/usr/bin/env sh
## Reads volumes

getCurMic() { mic_volume=$(pactl list sources | rg -A8 "RUNNING" | rg --only-matching "\d{2,3}%" | sed 's/.$//')
    if [ -z "${mic_volume}" ]; then
        mic_icon=""
        mic_volume=0
    else
        mic_icon=""
    fi
}

getCurVol() { volume=$(pamixer --get-volume-human)
    if [ "$volume" = "muted" ]; then
        leader="Vm"
        icon="󰝟"
        volume=0
    else
        # If not text, then want number
        volume=$(($(pamixer --get-volume)))
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
getCurMic
# printf "%s\n" "${leader}${icon} ${volume}% | ${mic_icon} ${mic_volume}%"
printf "%s\n" "${leader}${icon} ${volume}%"

# Subscribe, and for each line print the current volume
pactl subscribe | grep --line-buffered "sink" |\
    while read -r line; do
    getCurVol
    getCurMic
    # printf "%s\n" "${leader}${icon} ${volume}% | ${mic_icon} ${mic_volume}%"
    printf "%s\n" "${leader}${icon} ${volume}%"
done

#!/usr/bin/env sh
## Changes my wallpaper

# Set wallpaper
xrandr -q | rg ' connected' | while read -r line; do
    disp=$(echo "$line" | awk '{print $1}')
    resol=$(echo "$line" | rg --only-matching '\d{4}x\d{3,4}')
    "$HOME/git/agendrum/agendrum.py" --resolution "$resol" && xwallpaper --output "$disp" --center "/tmp/wallpaper_$resol.png"
done

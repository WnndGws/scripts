#!/usr/bin/env sh
## Run once a day/whenever I remember for a new background and lemonbar

dunstify "Agendrum" "Loading..."
xrandr -q | rg ' connected' | while read -r line; do
  disp=$(echo "$line" | awk '{print $1}')
  resol=$(echo "$line" | rg --only-matching '\d{4}x\d{3,4}')
  "$HOME/git/agendrum/agendrum.py" --resolution "$resol" && xwallpaper --output "$disp" --center "/tmp/wallpaper_$resol.png"
done

ps -aux | grep 'lemonbar -b' | awk '{print $2}' | xargs kill
"$XDG_CONFIG_HOME/lemonbar/init_bottom_bar.sh" &

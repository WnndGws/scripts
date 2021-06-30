#!/usr/bin/env sh
## Changes my wallpaper

if [ "$(bspc query -M | wc -l)" -eq 2 ]; then
  "$HOME/git/agendrum/agendrum.py" --resolution 1366x768 && xwallpaper --output LVDS1 --center /tmp/wallpaper_1366x768.png
  "$HOME/git/agendrum/agendrum.py" --resolution 1920x1080 && xwallpaper --output HDMI3 --center /tmp/wallpaper_1920x1080.png
else
  "$HOME/git/agendrum/agendrum.py" --resolution 1366x768 && xwallpaper --center /tmp/wallpaper_1366x768.png
fi

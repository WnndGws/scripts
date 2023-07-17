#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

if [[ "${TRACE-O}" == "1" ]]; then
  set -o xtrace
fi

xrandr --output VGA-1 --mode 1366x768 --pos 0x0 --rotate left --output LVDS-1 --primary --mode 1366x768 --pos 768x0 --rotate normal
bspc monitor LVDS-1 -d 1 2 3 4 5 6
bspc monitor VGA-1 -d 7 8 9 0
killall -9 sxhkd
sleep 5
"$HOME/git/scripts/shell/bspwm_output_desktops_to_sxhkd.sh"
sxhkd &
xwallpaper --center /tmp/wallpaper_1366x768.png
killall -9 lemonbar
"$HOME/.config/lemonbar/init_bottom_bar.sh" &
"$HOME/.config/lemonbar/init_top_bar.sh" &

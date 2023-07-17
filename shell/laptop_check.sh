#! /bin/zsh

while true; do
  batterybrightness
  xmodmap ~/.config/xmodmap/Xmodmap
  if pgrep lemonbar && pgrep sxhkd; then
    echo "Pass"
    sleep 60
  else
    zsh ~/.config/bspwm/bspwmrc &!
    sleep 300
  fi
done

#! /bin/zsh

while true; do
  batterybrightness
  pgrep sxhkd || (sxhkd & disown)
  xmodmap ~/.config/xmodmap/Xmodmap
  sleep 300
done

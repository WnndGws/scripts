#!/bin/bash
## Straight from the archwiki, but tweaked for keyboard

FILE="/sys/class/leds/tpacpi::kbd_backlight/brightness"
CONTENT=$(cat "$FILE")
if [ "$CONTENT" = "0" ]; then
    echo "1" > "$FILE"
elif [ "$CONTENT" = "1" ]; then
    echo "2" > "$FILE"
elif [ "$CONTENT" = "2" ]; then
    echo "0" > "$FILE"
fi
exit 0

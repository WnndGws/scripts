#!/bin/bash

STATE_FILE="/tmp/headphone_state"

# Initialize state file if it doesn't exist
if [[ ! -f "$STATE_FILE" ]]; then
    echo "speakers" > "$STATE_FILE"
    bluetoothctl disconnect 00:04:32:9A:8E:96
    pactl set-default-sink alsa_output.pci-0000_00_1f.3.analog-stereo
fi

# Read current state
CURRENT_STATE=$(cat "$STATE_FILE")

# Toggle logic
if [[ "$CURRENT_STATE" == "speakers" ]]; then
    echo "headphones" > "$STATE_FILE"
    bluetoothctl connect 00:04:32:9A:8E:96
    sleep 1.0
    pactl set-default-sink bluez_output.00_04_32_9A_8E_96.1
    echo "Audio toggled to: HEADPHONES"
else
    echo "speakers" > "$STATE_FILE"
    bluetoothctl disconnect 00:04:32:9A:8E:96
    pactl set-default-sink alsa_output.pci-0000_00_1f.3.analog-stereo
    echo "Audio toggled to: SPEAKERS"
fi

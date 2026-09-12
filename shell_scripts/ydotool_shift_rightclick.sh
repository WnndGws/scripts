#!/usr/bin/zsh
# Click and hold shift and rightclick for minecraft

ydotool key 42:1  # Left shift down
ydotool click 0x41  # Click right mouse button (1) down (4)
sleep 30
ydotool click 0x81  # Click right mouse button up
ydotool key 42:0  # Left shift up

#!/usr/bin/zsh
## Move mouse, click save, repeat
## Keys shown in /usr/include/linux/input-event-codes.h

# Click Print
ydotool mousemove --absolute -x 450 -y 100
ydotool click 0xC0

# Double click and copy ID by pressing ctrl+c
sleep 1
ydotool mousemove -x -50 -y -30
sleep 1
ydotool click --repeat 2 0xC0
ydotool key 29:1 46:1 46:0 29:0

# Press TAB 6 times, enter
ydotool key --key-delay 50 15:1 15:0 15:1 15:0 15:1 15:0 15:1 15:0 15:1 15:0 15:1 15:0 28:1 28:0
sleep 0.75
# ctrl v, enter
ydotool key 29:1 47:1 47:0 29:0 28:1 28:0
sleep 0.75
#enter to remove dialog
ydotool key 28:1 28:0

# Click Next
ydotool mousemove --absolute -x 425 -y 100
ydotool click 0xC0

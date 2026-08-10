#!/bin/zsh

# Get the PID of the currently focused window
PID=$(hyprctl activewindow -j | jq -r '.pid')

# Walk up the process tree to find the shell's working directory
# (Alacritty -> shell -> ... we want the shell's cwd)
if [ "$PID" != "" ]; then
    # Resolve the actual shell process (child of alacritty)
    SHELL_PID=$(pgrep -P "$PID" | head -1)
    if [ "$SHELL_PID" != "" ]; then
        PID="$SHELL_PID"
    fi

    CWD=$(readlink -f /proc/"$PID"/cwd 2>/dev/null)
    if [ "$CWD" != "" ]; then
        alacritty --working-directory "$CWD"
        exit 0
    fi
fi

# Fallback: just launch alacritty normally
alacritty

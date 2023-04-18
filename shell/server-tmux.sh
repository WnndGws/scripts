#!/bin/zsh
# Start the new tmux sessions on reboot via cron

# create two new sessions SES1 and SES2 and detach them.(-d -s is important)
tmux new-session -d -s convert
tmux new-session -d -s syncplay
tmux new-session -d -s fast_api
tmux new-session -d -s encoder_logging
tmux new-session -d -s podsync
tmux new-session -d -s mumble

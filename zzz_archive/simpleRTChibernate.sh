#!/bin/zsh
## New rtcHibernate to be more customizable

wake_time="9"

wake_time=$(date -d "now + 1day T$(bc <<< ($wake_time + 7))" +%s)
source <(gpg -qd $HOME/.passwords.asc) && export SUDO_PASSPHRASE && expect $HOME/Git/OneOffCodes/Expects/rtcHibernate.exp ${SUDO_PASSPHRASE} $wake_time

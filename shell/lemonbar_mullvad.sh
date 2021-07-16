#!/usr/bin/env sh
## Checks amimullvad to ensure I am connected to vpn

while true; do
    vpn=$(amimullvad)
    case $vpn in
        "You are connected to Mullvad"*) connected="YES" ;;
        *) connected="NO" ;;
    esac

    echo "A$connected"
    sleep 3600
done

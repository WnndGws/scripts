#!/usr/bin/env sh
## Checks amimullvad to ensure I am connected to vpn

while true; do
    vpn=$(amimullvad)
    case $vpn in
        "You are connected to Mullvad"*) connected="YES" ;;
        *) connected="NO" ;;
    esac
    echo "A$connected"

    runtime="10 minute"
    endtime=$(date -ud "$runtime" +%s)
    while [ "$(date -u +%s)" -le "$endtime" ]; do
        number_connections=$(ip add | rg mullvad | wc -l)
        case $number_connections in
            2) connected="YES" ;;
            0) connected="NO" ;;
        esac
        echo "A$connected"
        sleep 5
    done
done

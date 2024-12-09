#!/usr/bin/env sh
## Just prints cpu I have available to use in polybar

red='#65350'
green='#99c76c'
yellow='#ffc24b'

while true; do
    HOSTNAME=$(paste /etc/hostname)
    # Take one_min core load, times by 100 to get percentage, divide by 4 since quadcore cpu
    [ "$HOSTNAME" = "arch-beast" ] && one_min_cpu_load_avg=$(awk '{ printf "%1d",$1*12.5 }' < /proc/loadavg) || one_min_cpu_load_avg=$(awk '{ printf "%1d",$1*25 }' < /proc/loadavg)
    # 44th line in awk, print 4th col starting at 2nd character until 5 from the end
    [ "$HOSTNAME" = "x220" ] && temp=$(sensors -j | gron | rg '.*temp1\.temp1_input.*' | rg --pcre2 --only-matching '\d{2}(?=\.)') || temp=$(liquidctl --json status | gron | rg --pcre2 --only-matching '\d{2}(?=\.)')

    # Start to worry at 70%, investigate at over 100% constantly
    if [ "$one_min_cpu_load_avg" -gt 90 ]; then
        leader="U"
    elif [ "$one_min_cpu_load_avg" -gt 70 ]; then
        leader="H"
    else
        leader="L"
    fi

    echo "C$leader $one_min_cpu_load_avg% ($temp°C)"
    sleep 2
done

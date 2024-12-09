#!/usr/bin/env zsh
## Checks GPU stats

while true; do
    # Get 4th row, 2nd column and strip last character
    temp=$(sensors | rg --after-context 6 "amdgpu" | awk 'NR==7 {print substr($2, 2, length($2)-5)}')
    usage=$(radeontop --dump - | rg --only-matching --pcre2 --max-count 1 "(?<=gpu )\d+\.\d{2}")
    usage=$(printf "%2d" $usage)

    echo "G $usage% ($temp°C)"

    sleep 2
done

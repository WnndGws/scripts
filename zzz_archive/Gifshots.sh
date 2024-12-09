#!/bin/zsh

echo "Starting Peek........."
sleep 0.1
peek > /dev/null 2>&1
sleep 2
while [[ $(insync-headless get_sync_progress) != "No syncing activities"  ]] { echo -ne $(insync-headless get_sync_progress)\\r; sleep 0.1  }
sleep 3
echo -ne "\\nCopying link..........\\n"
find $HOME/GoogleDrive/01_Personal/01_Personal/05_Images/Screenshots -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" " | sed 's/\.\//\/home\/wynand\/GoogleDrive\/01_Personal\/01_Personal\/05_Images\/Screenshots\//g' | xargs -i insync-headless get_link {}
find $HOME/GoogleDrive/01_Personal/01_Personal/05_Images/Screenshots -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" " | sed 's/\.\//\/home\/wynand\/GoogleDrive\/01_Personal\/01_Personal\/05_Images\/Screenshots\//g' | xargs -i insync-headless open_in_gdrive {}
find $HOME/GoogleDrive/01_Personal/01_Personal/05_Images/Screenshots -type f -mtime +7 -execdir rm -f {} \;

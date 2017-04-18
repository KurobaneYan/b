#! /bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage: mykill <username>"
    exit 1
fi

ps -u "$1" | gawk '{if (NR > 1) print $1}' | xargs -r echo 'kill'


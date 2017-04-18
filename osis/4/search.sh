#! /bin/bash

search () {
    ls | while read FILE; do
        if [[ -f $FILE ]]; then
            for PATTERN in "$@"; do
                [[ $FILE =~ $PATTERN ]] && echo "$PWD/$FILE" && break
            done
        else
            cd "$FILE"
            search "$@"
            cd ..
        fi
    done
}

search "$@"

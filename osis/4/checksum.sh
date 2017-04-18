#! /bin/bash

TOTAL_CHECKSUM=0

while read FILE; do
    CHECKSUM=0

    for WORD in `cat < "$FILE"`; do
        WORD_SUM=0

        for (( i=0; i<${#WORD}; i++ )); do
            for BYTE in `echo -n "${WORD:$i:1}" | od -An -tuC`; do
                WORD_SUM=$(($WORD_SUM + $BYTE))
            done
        done

        CHECKSUM=$(($CHECKSUM + $(($WORD_SUM * 2017))))
        CHECKSUM=$(($CHECKSUM ^ $(($CHECKSUM >> 8))))
        CHECKSUM=$(($CHECKSUM & 65535))
    done

    echo "$FILE: $CHECKSUM"
    TOTAL_CHECKSUM=$(($TOTAL_CHECKSUM + $(($CHECKSUM * 2017))))
    TOTAL_CHECKSUM=$(($TOTAL_CHECKSUM ^ $(($TOTAL_CHECKSUM >> 8))))
    TOTAL_CHECKSUM=$(($TOTAL_CHECKSUM & 65535))

done < <(./search.sh "$@")

echo "TOTAL_CHECKSUM: $TOTAL_CHECKSUM"

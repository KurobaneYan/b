#!/bin/bash
START=$(date +%s.%N)
$1 $2
END=$(echo "$(date +%s.%N) - $START" | bc)
echo "$1 : $END" >> file.txt

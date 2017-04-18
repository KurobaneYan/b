#! /bin/bash

echo "User: ${USER}"
echo "Date and time: $(date +"%c")"
echo "Current directory: $(pwd)"
echo "Number of processes: $(pgrep -c "")"
echo "Files in directory: $(ls -l | gawk '{ if (NR > 1) sum += 1}; END { print sum}')"


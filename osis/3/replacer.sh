#! /bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage: replacer <input_file>"
    exit 1
fi

./number_replacer.sed < "$1"

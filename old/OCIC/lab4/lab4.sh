#!/bin/bash
size_all_f=0
number_kilo=0
count_all_f=0
start() {
  if [ $size_all_f -gt 1000 ]
    then
      size_all_f=$(echo "$size_all_f - 1000 + $(stat $1 -c %s)" | bc)
      number_kilo=$(echo "$number_kilo + 1" | bc)
    else
      size_all_f=$(echo "$size_all_f + $(stat $1 -c %s)" | bc)
    fi
  count_all_f=$(echo "$count_all_f + 1" | bc)
  local fullname="$1"
  echo $fullname
}

scan() {
  local x;
  for e in "$1"/*; do
    if [ -d "$e" -a ! -L "$e" ]
    then
      scan "$e" "$2" "$3"
    else
      local filename=`basename "$e"`
      rr="r"
      if [ $2 = $rr ]
      then
        if [ $(echo $filename | sed -ne "$3") ]
        then
          start "$e"
        fi
      else
        if [ $filename = $2 ]
        then
          start "$e"
        fi
      fi
    fi
  done
}

dir="/media/AddDrive/STUD/3stage/sem2/osis/OCIC/lab4/"

scan "$dir" "$1" "$2"
echo "Count files: $count_all_f"
echo "Size: $number_kilo.$size_all_f Kbyte"
echo "Avarage size file: $(echo "($number_kilo * 1000 + $size_all_f) / $count_all_f" | bc) byte"

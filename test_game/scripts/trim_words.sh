#!/bin/bash

if [[ $# == 0 ]];
then
    echo " used for stripping command type text from an adventure game transcript."
    echo " type ./trim_words.sh textfile.txt > output.txt "
    exit
fi

readarray -t my_array < $1

for line in "${my_array[@]}"; do
  # process the lines
  if [[  $line == ">"* ]];
  
  then
    echo $line
  fi
  
  #echo $line
done



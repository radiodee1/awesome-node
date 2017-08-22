#!/bin/bash

if [[ $# == 0 ]];
then
    echo " used for stripping command type text from an adventure game transcript."
    echo " type ./trim_words.sh textfile.txt > output.txt "
    exit
fi

readarray -t my_array < $1

ENDING=" - game"

for line in "${my_array[@]}"; do
  # process the lines
  if [[  $line == ">"* || $line != *"." ]];
  
  then
  
    if [[ $line == ">"* ]];
    then
        #echo $line $ENDING"."
        echo "${line//>/}"
    
    fi
  
    #echo $line"."
  fi
  
  #echo $line
done



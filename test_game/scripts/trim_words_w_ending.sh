#!/bin/bash

if [[ $# == 0 ]];
then
    echo " used for stripping command type text from an adventure game transcript."
    echo " type ./trim_words_w_ending.sh textfile.txt > output.txt "
    exit
fi

readarray -t my_array < $1

ENDING="-z"

for line in "${my_array[@]}"; do
  # process the lines
  if [[  $line == ">"* || $line != *"." ]];
  
  then
  
    if [[ $line == ">"* ]];
    then
    line="${line//>/}"
    COMMAND=""
        for word in $line; do
            COMMAND=$COMMAND" "$word$ENDING
            COMMAND="${COMMAND//$'\n'}"
        done
    
        echo $COMMAND"."
    else
        echo $line"."
    fi
  
    #echo $line"."
  fi
  
  #echo $line
done



#!/bin/bash

for FILE in $(ls *.csv)
do
	if [[ -f ../$FILE ]];
	then
		echo "$FILE already there"
	else
		sed "s/FILE/$FILE/g" keep_balanced_sets.py > temp
		chmod 777 temp
		./temp
		rm temp
	fi
done


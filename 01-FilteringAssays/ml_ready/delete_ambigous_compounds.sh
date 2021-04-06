#!/bin/bash

### ATTENTION: this executable has been written after the project was finished and is untested
### It is symbolic for the changes that have been made to the files first transferred to this directory

# loop through the Cell Painting Files in this directory
for FILE in $(ls cp*)
do
	# delete every line that contains eiterh 'Inconclusive' or 'Unspecified'
	sed -i '/Unspecified/d' $FILE
	sed -i '/Inconclusive/d' $FILE
done

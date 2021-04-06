#!/bin/bash

### this file takes several auxiliary files to generate a list of toxicologically relevant assays, represented by their AIDs
### the description of assays from the pubchem server DESCRIPTIONS contains keywords, one of which is 'Toxicity'
### therefore this file greps all lines containing 'Toxicity'
### Additionally a TARGETLIST contains a range of predicted toxicity targets, which are also greped by this file
### both grep outputs are appended to OUTPUT
### only the pubchem intern AIDs are kept in the list
### last but not least, the assay files, which are related to toxicity are then transferred to TOXASSAYS


### DEFINE GLOBAL VARIABLES
OUTPUT='tox_assays.txt'
TOXASSAYS='tox_assays'
TARGETLIST='tox_targets.txt'
DESCRIPTIONS='assays_descriptions.csv'

### EXTRACT TOXICITYLIST FROM DESCRIPTIONS

# the DESCRIPTIONS file obtained from a jupyter notebook is processed to obtain a list of AIDs that are connected to toxicity
echo "Toxicity related Assays" > $OUTPUT
grep 'Toxicity' $DESCRIPTIONS >> $OUTPUT

# the TOXTARGETS file from a paper of the bender group guides the search to some extend
IFS=$'\r\n' GLOBIGNORE='*' command eval  'TOXTARGETS=($(cat $TARGETLIST))'

for i in ${TOXTARGETS[@]}
do
	grep "$i" $DESCRIPTIONS >> $OUTPUT
done

# the OUTPUT file is then shortened by only printing the AID information
awk -F "," '{print $1}' $OUTPUT > temp
mv temp $OUTPUT

### EXTRACT FILES FROM DIRECTORIES BY TOXICITYLIST

# the OUTPUT is read and saved to the TOXAIDS array
IFS=$'\r\n' GLOBIGNORE='*' command eval  'TOXAIDS=($(cat $OUTPUT))'

# the downloadabel directories PARENT_DIR are the searched for the FILEs with the respective AID number
# the correct FILES are the transferred to the TOXASSAYS directory if present
for PARENT_DIR in $(ls -d [0-9]*/)
do
	PARENT_DIR=${PARENT_DIR%/*}			# get rid of the first match of '/*' from the right side of the variable 
	
	for AID in ${TOXAIDS[@]}			# loop through all the toxicity AIDs saved to TOXAIDS array
	do
		FILE="${PARENT_DIR}/${AID}.csv.gz"	# define the file from the AID the parent directory and the correct file extension
		if [ -f "$FILE" ]			# if statement checks if the file is present; error proofing
		then
			cp $FILE ${TOXASSAYS}/		# copy the file to a new directory if present
		fi
	done
done

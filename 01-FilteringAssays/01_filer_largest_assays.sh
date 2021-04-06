#!/bin/bash

### this bash script screens downloaded folders from ftp://ftp.ncbi.nlm.nih.gov/pubchem/Bioassay/CSV/Description/
### said folders contain compressed csv files from diverse bioassays that feature a certain number of compounds
### The directories contain the assays, which are encoded by their pubchem  assay identification number (AID) and which are listed after sorting them by their size
### Only the first 100 largest AIDs are then listed in another file (OUTPUT)
### OUTPUT will get uploaded to pubchem to obtain descriptions of every AID

OUTPUT='largest_assays.txt'


# create the file OUTPUT that will contain the final Pubchem Assay Identifiers that will be checked manually for toxicity endpoints
echo "AID List" > $OUTPUT

# for loop iterates through all the downloadable parent directories containing assays (listed by their AIDs)
for PARENT_DIR in $(ls -d [0-9]*/)
do
	# get rid of the '/' that makes the variable name to a directory in the eyes of the parser
	PARENT_DIR=${PARENT_DIR%/*}

	# create a list for each parent directory by assigning it a header (to be deleted by 'sed' command below)
	echo "$PARENT_DIR" > ${PARENT_DIR}.list

	# loop through all the AIDs (a.k.a. filenames) in the parent directories sorted by SIZE
	for AID in $(ls -S ${PARENT_DIR}/*)
	do
		AID=${AID##*/}			# shortest left-hand-side ('#') substring matching REGEX '*/' gets removed from the string in the variable 
		AID=${AID%%.*}			# longest right-hand-side ('%%') substring matching REGEX '.*' gets removed from the substring
		echo $AID >> ${PARENT_DIR}.list	# echo the processed AID to the list of the respective parent directory
	done

	# delete ('d') the first ('1') line in the parent directory list, so that only the AIDs will be printed in the next command
	sed -i '1d' ${PARENT_DIR}.list

	# print the first 100 lines to OUTPUT
	# Since they are sorted by size it will be the 100 AID's with most data.
	head -100 ${PARENT_DIR}.list >> $OUTPUT

	# clean up!
	mv ${PARENT_DIR}.list _misc/

done

# delete the header so that it can be simply uploaded to pubchem
sed -i '1d' $OUTPUT

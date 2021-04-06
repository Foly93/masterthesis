#!/bin/bash

### this bash file loops through the files picked by the prior bash programm and filters out the compounds featured in each assay
### the compounds are only identified by the pubchem CID
### all of the CIDs are saved to OUTPUT
### OUTPUT is then uploaded to pubchem to obtain the descriptions of the compounds which also contain inchi keys

OUTPUT='all_featured_compounds.txt'
TOXASSAYS='tox_assays'

# create the OUTPUT file
echo "CID_list" > $OUTPUT
sed -i '1d' $OUTPUT

# give the operator some intel about the ongoings of the programm
printf "starting to unzip and to extract the CIDs..."

# loop through the files saved in the directory TOXASSAYS
for FILE in $(ls $TOXASSAYS)
do
	# unzip the files
	gunzip ${TOXASSAYS}/${FILE}
	# only save the CID which happens to be in the third column. Pattern makes sure no nan values are saved
	awk -F "," '$3 ~ /^[0-9]+$/ {print $3}' ${TOXASSAYS}/${FILE%.*} >> $OUTPUT
done

# let the operator know, that the operation is done
echo "done!"

# give the operator some intel about the ongoings of the programm
printf "starting to remove duplicate values and sort the list..."
# sort the values and only keep every value once
sort -u $OUTPUT > temp
mv temp $OUTPUT
# let the operator know, that the operation is done
echo "done!"

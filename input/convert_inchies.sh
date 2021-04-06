#!/bin/bash

# sed variables:

DATASET='cp'
ORIGINFILE='cp_annotations.csv'
SMILESCOL='StdInChI'
SPLIT='100'

# create the output file and add the column header
echo "StdInChI" > ${DATASET}_inchies.csv

# iterate through the integers of SPLIT in reverse order hence the negative increment
for SUBSETNO in $(seq $SPLIT -1 1)
do
	sed "s/SUBSETNO/${SUBSETNO}/g" convert_inchies.py > convert_inchies_${SUBSETNO}.py
	sed -i "s/DATASET/${DATASET}/g" convert_inchies_${SUBSETNO}.py
	sed -i "s/ORIGINFILE/${ORIGINFILE}/g" convert_inchies_${SUBSETNO}.py
	sed -i "s/SMILESCOL/${SMILESCOL}/g" convert_inchies_${SUBSETNO}.py
	sed -i "s/SPLIT/${SPLIT}/g" convert_inchies_${SUBSETNO}.py

	# make the new file executable
	chmod 777 convert_inchies_${SUBSETNO}.py
	# execute all the files in the background but the first subset to show the progress bar
	if (( $SUBSETNO == 1 ))
	then
		./convert_inchies_${SUBSETNO}.py
	else
		nohup ./convert_inchies_${SUBSETNO}.py & 
	fi
done

# this block makes sure the *.sh waits for all subsets to be ready
# while the number of files is not equal to split, subsets are still missing
while (( $(ls ${DATASET}_inchies_* | wc -l) != $SPLIT ))
do
	echo -ne "InChIs in Progress...\r"
	sleep 15
done

echo -e "\nInChIs done!"

# this for loop appends only the InChIs not the header of each subset to the complete inchi file
for file in $(ls -1v ${DATASET}_inchies_*)
do
	# copy line by line to the output starting from the second line (no header)
	tail -n+2 $file >> ${DATASET}_inchies.csv
done

# some InChIs are embraced by "" and some are not but all of them need ""; the way i did it in dilirank.ipynb it works only without all the quotes (sep='\n')
sed -i 's/\"//g' ${DATASET}_inchies.csv
sed -i 's/^/\"/g' ${DATASET}_inchies.csv
sed -i 's/$/\"/g' ${DATASET}_inchies.csv


# clean up a little
mv convert_inchies_*.py _misc/
mv ${DATASET}_inchies_* _misc/
rm nohup.out

#!/bin/bash

### HEADER

# this script measures the feature importance of an input dataset by means of entropy and gini score
# supporting file is a python script that is generated via nbconvert from a source file (*.ipynb)
# as input the pubchem assays wiht morgan fingerprints are used that be found in ../../03*/_out*/
# this script is part of the masterthesis of luis vollmers

### DEFINE FUNCTIONS

feature_importance() 
{
	# change the placeholder to the concurrent AID and implement it into the filename
	sed "s/AID/$1/g" fi_rf_fp_AID.py > fi_rf_fp_$1.py
	# make file executable
	chmod 777 fi_rf_fp_$1.py
	# make the random forest prediction using cell-painting data to 
	./fi_rf_fp_$1.py
	# after execution the py script is no longer needed
	mv fi_rf_fp_$1.py ../_trash/
}


### CALL FUNCTIONS

# use the nbconvert to generate .py from notebook
jupyter nbconvert --to script fi_rf_fp_1030.ipynb

# rename the notebook and change the iterable (1030) to placeholder (AID)
sed "s/1030/AID/g" fi_rf_fp_1030.py > fi_rf_fp_AID.py

# remove the plt.show() which is disturbing the automatic process
sed -i '/plt.show/d' fi_rf_fp_AID.py

# for loop cycles through the files in the source directory
for aid in $(ls ../../03-GenerateFingerprints/_output/*)
do
	# parameter expansion to get the raw aid from input file names
	aid=${aid%.*}
	aid=${aid##*_}

	# run the feature importance function
	printf "Running for $aid..."
	time feature_importance $aid 
	echo "done"
done

# after looping through all py script the template is no longer needed
mv fi_rf_fp_AID.py ../_trash/



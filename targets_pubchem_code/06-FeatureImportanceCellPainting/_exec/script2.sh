#!/bin/bash


### HEADER

# This script is for adjusting a template jupyter notebook (fi_rf_cp_AID.py) so that a Feature Importance analysis can be conducted from a cluster of *.py programs without human intervention.
# the resulting .py programms execute a Feature Importance analysis for a dataset generated from Cell painting data and Pubchem Assay data.
# feature analysis method include Hierarchical clustering, PCA, RF Feature Importance and Spearman rand correlation
# The Input data for this notebook is stored in 02-CorrectingAssays and is part of the master thesis of Luis Vollmers
# the output is stored in the _output directory of this subproject 06-PredictCellPainting
# a multitude of plots is generated and stored in ../_output/,  also text information and subsets of the original data that contain information about feature importance or only important features
# the for loop of this program which is the center piece gets its variable from script2.sh which adjusts the for loop to run only 5 *.py in sequence so that 11 can run in parallel (52 *.py files in total)


### DEFINE FUNCTIONS

feature_importance() 
{
	# change the placeholder to the concurrent AID and implement it into the filename
	sed "s/AID/$1/g" fi_rf_cp_AID.py > fi_rf_cp_$1.py
	# make file executable
	chmod 777 fi_rf_cp_$1.py
	# make the random forest prediction using cell-painting data to 
	./fi_rf_cp_$1.py
}


### CALL FUNCTIONS

AssayFiles=$(ls ../../02-CorrectingAssays/_output/*)

lower=0
upper=500

i=0

for aid in ${AssayFiles[@]}
do
	i=$(echo "$i+1" | bc)
	if (($lower<i && i<=$upper))
	then
		aid=${aid%.*}
		aid=${aid##*_}
		printf "Running for $aid..."
		feature_importance $aid 
		echo "done"	
	fi
done

mv fi_rf_cp_$1.py ../_trash/

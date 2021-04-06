#!/bin/bash


### DESCRIPTION

# One function with in the *.ipynb file is very time consuming, which makes utilization of multiple cores necessary. Therefore, this scripts purpose split in two distinct tasks.
# 1.: generate *.py files from the *.ipynb file that can be executed from the command line for all different PubChem assays, that are stored in ../../02-*/_output
# 2.: generate *.sh files from script1.sh that execute the corresponding *.py files so that eleven processes are running in parallel at all time
# The output *.ipynb and therefore all the other *.py executables are various files related to the feature importance of the respective assay. For more information look at the *.ipynb file
# note that many files created and used in this script are later transferred into the ../_trash directory, since they are only of temporary use


# use the nbconvert to generate .py from notebook
jupyter nbconvert --to script fi_rf_cp_1030.ipynb

# rename the notebook and change the iterable (1030) to placeholder (AID)
sed "s/1030/AID/g" fi_rf_cp_1030.py > fi_rf_cp_AID.py
# remove the plt.show() which is disturbing the automatic process
sed -i '/plt.show/d' fi_rf_cp_AID.py

for lower in $(seq 0 5 50)
do
	# calculate upper from lower
	upper=$(echo "$lower+5" | bc)

	# change the boundaries of the for loop if statement in the script2.sh which executes the feature importance python files in sequence
	sed "s/upper=.*/upper=$upper/g" script2.sh > script_num_${lower}.sh
	sed -i "s/lower=.*/lower=$lower/g" script_num_${lower}.sh

	# make the files with the correct boundary executable
	chmod 777 script_num_${lower}.sh
	# execute and append to nohup.out but with an ID
	nohup ./script_num_${lower}.sh &> ../_trash/nohup${lower}.out &
done

mv script_num_${lower}.sh ../_trash/
mv fi_rf_cp_AID.py ../_trash/

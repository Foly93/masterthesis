#!/bin/bash

for ASSAYNUMBER in $(ls tox_assays/)
do
	ASSAYNUMBER=${ASSAYNUMBER%.*}
	ASSAYNUMBER=${ASSAYNUMBER#*_}

	sed "s/ASSAYNUMBER/$ASSAYNUMBER/g" 06_overlap_cp.py > temp
	chmod 777 temp
	printf "running for $ASSAYNUMBER..."
	./temp
	echo "done"
done

rm temp

#!/bin/bash

### iterate through all the ASSAYFILES and execute py

for ASSAYNUMBER in $(ls tox_assays/)
do
	sed "s/ASSAYNUMBER/${ASSAYNUMBER%%.*}/" 05_convert_inchikeys.py > temp.py
	chmod 777 temp.py
	./temp.py
	rm temp.py
done


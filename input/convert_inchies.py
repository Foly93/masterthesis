#!/usr/bin/env python

import time
import cirpy
import pandas as pd
from math import ceil
from tqdm import tqdm

# Prerequisites and variables from *.sh are initialized
split = SPLIT                       # SPLIT from *.sh determines the batch sizes
subsetno = SUBSETNO                 # SUBSETNO from *.sh determines the range within the dataset
DATASET = pd.read_csv('ORIGINFILE') # DATASET is read from the ORIGINFILE (both names from *.sh)
inchilist = []                      # initialize empty (global) list to be used in convert_batch

# e and b are calculated from split and subsetno and the number of rows
b=ceil(DATASET.shape[0]/split)*(subsetno-1)
e=ceil(DATASET.shape[0]/split)*subsetno
# if out of bounds, e is assigned None which automatically iterates til the last row of DATASET
if e > DATASET.shape[0]:
    e = None

# smileslist saves DATASET's smiles from SMILESCOL
smileslist = DATASET.SMILESCOL.to_list()[b:e]   

# define a function that fetches the StdInChI for the indexes SMILES
def convert_batch():

    # use a for loop to translate SMILES to InChi's via the cirpy package with progressbar
    for smiles in tqdm(smileslist):
        try:
            inchilist.append(cirpy.resolve(smiles, 'stdinchi'))
        # in case the inchi cannot be resolved a nan is appended to the list for look up
        except:
            inchilist.append("nan")


# use the convert_batch function to fill the inchilist
convert_batch()
# define a dataframe for easier export handling; endpoint is to be changed by an external bashscript
DATASET_inchies_SUBSETNO = pd.DataFrame(inchilist, columns=["StdInChI"])
# use pandas to_csv to output the dataframe; the subsetno is appended for maintaining correct order 
DATASET_inchies_SUBSETNO.to_csv('DATASET_inchies_SUBSETNO.csv', index=False)

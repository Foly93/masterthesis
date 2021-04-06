#!/usr/bin/env python

import pandas as pd

# read the file that annotated the compounds with the inchikeys and ASSAYFILE (to be specified by *.sh)
CID_inchikeys = pd.read_csv('compounds_inchi_keys.txt', sep='\t')
AID_dataframe = pd.read_csv('tox_assays/ASSAYNUMBER.csv')

# 'cid' is the column name designated by pubchem and unfortunately the column has to be transformed to float
# this is because somehow the ASSAYFILE cid-column is read as float too
CID_inchikeys['cid'] = CID_inchikeys['cid'].astype('float64')

# save the dataframe just in case
AID_tmi = AID_dataframe.copy(deep=True)

# drop the rows that contain no information
AID_dataframe = AID_tmi.drop([0,1,2,3,4])

# save the dataframe just in case
AID_noinchi = AID_dataframe.copy(deep=True)

# merge the two dataframes on cids and only keep the overlap (CID_inchikeys contains all the compounds of all assay files)
AID_dataframe = pd.merge(CID_inchikeys, AID_noinchi, left_on='cid', right_on='PUBCHEM_CID', how='inner')

# drop the cid column since it is duplicate
AID_dataframe.drop('cid', axis=1,inplace=True)

# export the dataframe to csv
AID_dataframe.to_csv('tox_assays/inchikeys_ASSAYNUMBER.csv',index=False)


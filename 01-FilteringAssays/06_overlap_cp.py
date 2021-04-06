#!/usr/bin/env python

import pandas as pd

# read the cell-painting data
cp_annotations = pd.read_csv('~/PythonProjects/input/cp_annotations.csv')
# read the assay information of the pubchem assay
pubchem_ASSAYNUMBER = pd.read_csv('tox_assays/inchikeys_ASSAYNUMBER.csv')

# calculate the overlap using merge
pubchem_ASSAYNUMBER = cp_annotations.merge(pubchem_ASSAYNUMBER, how = 'inner', on = ['inchikey', 'inchikey'])

# copy the dataframe to save the results already done so far
pubchem_ASSAYNUMBER_tmi = pubchem_ASSAYNUMBER.copy(deep=True)

# drop the column that containt too much information (tmi) to create the final dataframe
pubchem_ASSAYNUMBER = pubchem_ASSAYNUMBER_tmi.drop(['Unnamed: 0','CPD_NAME','CPD_NAME_TYPE','CPD_SAMPLE_ID','DOS_LIBRARY','SOURCE_NAME','CHEMIST_NAME','VENDOR_CATALOG_ID','CPD_SMILES','USERCOMMENT','StdInChI','inchikey'],axis=1)

### CREATE ML-READY DILIRANK-CP-DATAFRAME

# load centermean into the notebook
cp_data = pd.read_csv('~/PythonProjects/input/CP_center_mean.csv')

# merge cp on dilirank to obtain annotated dataframe
pubchem_ASSAYNUMBER_cp = cp_data.merge(pubchem_ASSAYNUMBER, how='inner', on=['Metadata_broad_sample','Metadata_broad_sample'])

# export the dataframe for later use in ML-algorithm
pubchem_ASSAYNUMBER_cp.to_csv('ml_ready/cp_ASSAYNUMBER.csv',index=False)

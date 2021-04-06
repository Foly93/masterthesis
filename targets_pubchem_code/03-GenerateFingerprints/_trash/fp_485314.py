#!/usr/bin/env python
# coding: utf-8

# ### Generating Molecular Fingerprints for the assay data
# This notebook serves as a first approach to workout a pipeline to generate the molecular fingerprints of the pubchem assay data. It is part of the master's thesis of Luis Vollmers. To generate the finger prints the following steps are undertaken:
# 1. read the input
# 2. generate Morgan Fingerprints
# 3. Append the Morgan Fingerprints to the DF
# 4. Export the Output
# 
# Notice that the pubchem assays have been preprocessed, so that their compounds overlap with the cell painting data set in question and only relevant activity columns are kept as categorization columns for machine learning applications.
# 
# #### Conclusion
# The output of this notebook is a csv file that has the dimensions 5021x2058. The columsn contain meta data labels aswell as the morgan fingerprint bitvector assigned by integer numbers. The rows are assigned to unique compounds identifiable by the 'CAN_SMILES' column.

# In[106]:


import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import AllChem


# #### 1. Read the Input
# - input files are being found in step 2 dirctory and are named after their respective 485314
# - the original notebook was processing the file cp_485314.csv but that is subject to change
# - for generating the Morgan Fingerprints only the meta data columns are necessary (first 10 columns)

# In[107]:


df = pd.read_csv('../../02-CorrectingAssays/_output/cp_485314.csv')
df = df.iloc[:,:10]
# df # just uncomment if you want to have a look at the dataframe


# #### 2. Generate Morgan Fingerprints
# - first the values in the CAN_SMILES column need to be translocated into a list for easier iteration
# - then an rdkit method is used to generate molecular graphs as input for the next step
# - the morgan fingerprints for all compounds are the generated by another rdkit method

# In[108]:


# from the df the canonical SMILES are particularly interesting to generate the molecular fingerprints from
can_smiles_list = df.loc[:,'CAN_SMILES'].to_list()

# to use the respective method of RDkit molecular representations (mol) have to be generated first
mol_list = [Chem.MolFromSmiles(can_smiles) for can_smiles in can_smiles_list]

# from the list of molecular representations fingerprints are getting generated
fp_list = [AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048) for mol in mol_list]


# #### 3. Append the Morgan Fingerprints to the DF
# - the fp are initiated as objects and need to be transformed into an integer array/vector
# - the resulting numpy array is then transformed into a dataframe
# - then the fingerprint data and the original data is concatenated

# In[111]:


# to include the list into the data frame readable bit vectors are needed. therefore the numpy arrays are generated
fp_arr = np.zeros((len(fp_list),2048))
for i in range(len(fp_list)):
    DataStructs.ConvertToNumpyArray(fp_list[i], fp_arr[i])
    
# convert the array into a dataframe to concatenate the fingerprints with the metadata in the next step
FP_data = pd.DataFrame(fp_arr)

# concatenation of the meta data with the molecular fingerprints
df = pd.concat([df, FP_data], axis=1)


# #### 4. Export the Output
# - the output is exported in the according directory in step 3 (current directory)
# - the format is csv and no index is outputted to avoid 'Unnamed: 0' column
# - non-mandatory quality control step to check if the outputtet dataframe looks as expected

# In[114]:


# output the fingerprints of assay 'assaynummer' to the _output directory
df.to_csv('../_output/fp_485314.csv',index=False)

# pd.read_csv('../_output/fp_485314.csv') # only uncomment to check if the output was done correctly


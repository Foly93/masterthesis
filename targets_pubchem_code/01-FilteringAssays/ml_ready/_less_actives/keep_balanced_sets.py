#!/usr/bin/env python

import pandas as pd

df = pd.read_csv('FILE')

print('FILE')
if df.PUBCHEM_ACTIVITY_OUTCOME.value_counts().shape[0] > 1:
    if df.PUBCHEM_ACTIVITY_OUTCOME.value_counts()['Active'] > 100:
        df.to_csv('../FILE')
        print(df.PUBCHEM_ACTIVITY_OUTCOME.value_counts())

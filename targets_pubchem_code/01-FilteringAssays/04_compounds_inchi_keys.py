#!/usr/bin/env python

import pandas as pd

CID_in=pd.read_csv('compounds_descriptions.csv')
CID_out = CID_in[['cid','inchikey']]
CID_out.to_csv('compounds_inchi_keys.txt', sep='\t', index=False)

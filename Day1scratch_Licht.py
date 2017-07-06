#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 16:52:27 2017

@author: Daniel E. Licht

subway data cleaning trials for group 1, project Benson

"""

import numpy as np
import pandas as pd

#df = py.read_csv("/Users/dlicht/ds/metis/metisgh/sf17_ds7/projects/01-benson/turnstile_170624.csv")
df = pd.read_csv("turnstile_170624.txt")
df2 = pd.read_csv("turnstile_170617.txt")
df_all = df.append(df2)

for col in df.columns:
    if df[col].dtype == 'O':
        df[col] = df[col].str.strip()

df.rename(columns = {'EXITS                                                               '\
                     : 'EXITS'}, inplace = True)
#    
#df.DATE = pd.to_datetime(df.DATE)
#

df_s = df.sort_values(['C/A','SCP','DATE','TIME'], ascending = [True,True,True,True])

#do row subraction   - this doesn't account for counter roll-over :-()
df_s["Nenter"] = df.ENTRIES.diff()
df_s["Nexits"] = df.EXITS.diff()







#total up number of entries and exits per turnstile
ins = df_s.groupby(['STATION','C/A','SCP'])[['Nenter']].agg(['count', 'mean','std'])
outs = df_s.groupby(['STATION','C/A','SCP'])[['Nexits']].agg(['count', 'mean','std'])



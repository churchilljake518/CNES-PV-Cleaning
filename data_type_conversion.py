# -*- coding: utf-8 -*-
"""
Created on Sat Oct  4 15:18:02 2025

@author: Churc
"""
import pandas as pd

# Save once (from Excel)
df = pd.read_excel("data/InverterData_2025.xlsx", sheet_name="INV 9 2-22-25", skiprows=9)
df = df.drop(df.columns[[0,1,3,7,8]],axis=1)
df.to_parquet("data/INV 9 2-22-25.parquet", index=False)


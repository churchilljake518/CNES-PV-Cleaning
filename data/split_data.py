from pathlib import Path
import pandas as pd

# Load xlsx file
file_path = Path(__file__).resolve().parent / 'InverterData_2025.xlsx'
sheets = pd.read_excel(file_path, sheet_name=None) 

# Split first half of worksheets into one file
names = list(sheets.keys())
# mid = len(names) // 2
# first_half = names[:mid]
# second_half = names[mid:]

# Save each sheet as its own CSV, named after the tab
for n in names:
    sheets[n].to_csv(f'{n}.csv', index=False)

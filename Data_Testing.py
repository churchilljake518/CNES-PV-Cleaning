# -*- coding: utf-8 -*-
"""
Testing Data Stuff and Github
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# First, get the sheet names
xls = pd.ExcelFile("InverterData_2025.xlsx")
print(xls.sheet_names)  # see all sheet names

# Choose the ones you want
sheets_to_load = [xls.sheet_names[1], xls.sheet_names[2]]

# Load only those sheets, with their names as keys
data = pd.read_excel(
    "InverterData_2025.xlsx",
    sheet_name=sheets_to_load,
    skiprows=9  # since data starts on row 11
)

# print(data.keys())  # will show sheet names now

# Pick the first device sheet
first_device_name = sheets_to_load[0]
df_first_device = data[first_device_name]

# Select timestamp (3rd col) and energy in (6th col)
time_col = df_first_device.columns[2]
energy_col = df_first_device.columns[5]

# Ensure timestamp column is datetime
df_first_device[time_col] = pd.to_datetime(df_first_device[time_col])

# Filter first hour of data
start_time = df_first_device[time_col].iloc[0]
mask = (df_first_device[time_col] < start_time + pd.Timedelta(hours=1))
df_first_hour = df_first_device[mask]

#%% Fifteen Minute Data
#Now look at fifteen minute data
cum_energy_col = df_first_device.columns[6]

# Set timestamp as index
df_first_device = df_first_device.set_index(time_col)


# Resample to 15-minute intervals, take the last cumulative value in each bin
resampled = df_first_device[cum_energy_col].resample("15min").last()

# Compute energy produced in each 15-minute bin (difference of cumulative)
energy_15min = resampled.diff().dropna() #dropna will remove the first row which becomes N/A when subtracting

# %% 1 Day
# Restrict to the first day of data
start_time = energy_15min.index[0].normalize() + pd.Timedelta(days=1) # midnight of first full day
# start_time = energy_15min.index[0] # One day from the next 15 min timestamp

end_time = start_time + pd.Timedelta(days=1)
energy_first_day = energy_15min.loc[start_time:end_time]

# Reset index into a dataframe for inspection if desired
df_energy_first_day = energy_first_day.reset_index()
df_energy_first_day.columns = ["DateTime", "EnergyProduced_15min"]
#%% Plotting
fig,ax = plt.subplots(figsize=(10,6))
ax.scatter(df_energy_first_day["DateTime"], df_energy_first_day["EnergyProduced_15min"], s=60, c="purple")
ax.set_xlabel("Hour", fontsize=14)
ax.set_ylabel("Energy Produced (kWh)", fontsize=14)
#plt.tick_params(axis='both', which='major', labelsize=12)
parts = first_device_name.split()   # ['INV', '9', '2-22-25']
inverter_name = f"Inverter {parts[1]}"
plot_date = df_energy_first_day["DateTime"].iloc[0].date()  # just the date part
plot_date_str = plot_date.strftime('%m-%d-%Y')  
plt.title(f"{inverter_name} Energy Produced:  {plot_date_str}", fontsize=16)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
fig.autofmt_xdate()
plt.savefig("energy_plot.png", dpi=300, bbox_inches="tight")
plt.show()
#%% Save Figure

"""
# Scatter plot
plt.figure(figsize=(10,6))
plt.scatter(df_first_hour[time_col], df_first_hour[energy_col], s=20, c="green")
plt.title(f"First Hour Energy Readings - {first_device_name}")
plt.xlabel("Time")
plt.ylabel("Energy In (Wh)")  # adjust units if needed
plt.grid(True)
plt.show()
"""



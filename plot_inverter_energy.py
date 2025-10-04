# -*- coding: utf-8 -*-
"""
Created on Sat Oct  4 12:28:10 2025

@author: Churc
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


def plot_inverter_energy(selected_date, res, excel_path="data/InverterData_2025.xlsx"):
    """Plot 15-min energy production for the given date."""
    # --- Load only the relevant sheet or subset ---
    # Assuming one sheet with timestamp column:
    # df = pd.read_excel(excel_path, sheet_name = 1, usecols=[2, 6], skiprows=9)
    
    # Later, in your function
    df = pd.read_parquet("data/INV 9 2-22-25.parquet")
    df = df.iloc[:, [0, 3]]  # select columns by index
    df.columns = ['Timestamp', 'Cumulative_Energy']
    
    # --- Convert and filter by date ---
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    mask = df['Timestamp'].dt.date == selected_date
    df_day = df.loc[mask].copy()

    if df_day.empty:
        return None  # no data for that day
    df_day = df_day.set_index('Timestamp')
 # --- Resampling logic ---
    if res.lower() == "15 min":
        resampled = df_day['Cumulative_Energy'].resample('15min').last().dropna()
        df_plot = resampled.diff().dropna().reset_index(name='Energy')
        title_res = "15-Minute"
    elif res.lower() == "hourly":
        resampled = df_day['Cumulative_Energy'].resample('1h').last().dropna()
        df_plot = resampled.diff().dropna().reset_index(name='Energy')
        title_res = "Hourly"
    elif res.lower() == "1 min":
        # Data is already at 1-minute intervals — just take differences
        df_plot = df_day['Cumulative_Energy'].diff().dropna().reset_index(name='Energy')
        title_res = "1-Minute"
    else:
        raise ValueError(f"Invalid resolution: {res}. Use 'Hourly', '15 min', or '1 min'.")
    """
    # --- Compute 15-min energy increments ---
    # Resample to 15-minute intervals, take the last cumulative value in each bin
    df_day['Timestamp'] = pd.to_datetime(df_day['Timestamp'])
    df_day = df_day.set_index('Timestamp')
    
    # Keep the last cumulative energy in each 15-min bin
    resampled = df_day['Cumulative_Energy'].resample('15min').last()
         
    # Compute 15-min energy production
    energy_15min = resampled.diff().dropna()  # Drop NaN if any
    energy_15min = energy_15min.to_frame()
    energy_15min.rename(columns={'Cumulative_Energy': 'Energy_15min'}, inplace=True)
    """
    # --- Plot ---
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(df_plot['Timestamp'], df_plot['Energy'], s=15)
    ax.set_xlabel("Time of Day", fontsize=12)
    ax.set_ylabel("Energy Produced (kWh)", fontsize=12)
    ax.set_title(f"{title_res} Energy Produced on {selected_date.strftime('%B %d, %Y')}", fontsize=14)
    # Format x-axis to show only hours
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%H:%M"))
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

"""
selected_date = date(2025, 2, 3)
fig = plot_inverter_energy(selected_date,res="15 min")
plt.show()
"""
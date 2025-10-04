# -*- coding: utf-8 -*-
"""
Created on Sat Oct  4 14:01:59 2025

@author: Churc
"""
"""
cd C:\\Users\\Churc\\Documents\\GitHub\\CNES-PV-Cleaning
streamlit run app.py

"""

import streamlit as st
from datetime import date
from plot_inverter_energy import plot_inverter_energy

st.title("Inverter Energy Data Viewer")

year = st.selectbox("Year", [2025])
month = st.selectbox("Month", list(range(1, 13)))
day = st.selectbox("Day", list(range(1, 32)))
resolution = st.selectbox("resolution", ["Hourly","15 min","1 min"])

try:
    selected_date = date(year, month, day)
except ValueError:
    st.error("Invalid date (e.g., Feb 30 doesn’t exist).")
    st.stop()

fig = plot_inverter_energy(selected_date,res=resolution)

if fig is None:
    st.warning(f"No data available for {selected_date.strftime('%B %d, %Y')}.")
else:
    st.pyplot(fig)

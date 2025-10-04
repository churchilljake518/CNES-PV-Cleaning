# -*- coding: utf-8 -*-
"""
Created on Sat Oct  4 00:58:41 2025

@author: Churc

Copy lines below into cmd to run page 
"""
"""
cd C:\\Users\\Churc\\Documents\\GitHub\\CNES-PV-Cleaning
streamlit run testpage.py

"""


import streamlit as st
from datetime import date
import os


# Path to folder relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")

# --- Page setup ---
st.set_page_config(page_title="Daily Image Viewer", layout="centered")
st.title("Daily Image Viewer")

# --- Date selection ---
st.subheader("Select a date")

# Dropdowns for year, month, day
year = st.selectbox("Year", [2024, 2025])
month = st.selectbox("Month", list(range(1, 13)))
day = st.selectbox("Day", list(range(1, 32)))

# Combine into a date object (with validation)
try:
    selected_date = date(year, month, day)
except ValueError:
    st.error("Invalid date (e.g., Feb 30 doesn’t exist).")
    st.stop()

# --- Check for corresponding image ---
image_folder = "images"
# Construct image path safely
image_filename = f"{selected_date.strftime('%Y-%m-%d')}.png"
image_path = os.path.join(IMAGE_FOLDER, image_filename)

st.write(f"Looking for image at: {image_path}")

# --- Display image or message ---
if os.path.exists(image_path):
    st.image(image_path, caption=f"Data for {selected_date.strftime('%B %d, %Y')}", use_column_width=True)
else:
    st.warning(f"No data available for {selected_date.strftime('%B %d, %Y')}.")

#This will be the streamlit file
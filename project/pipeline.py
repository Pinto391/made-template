#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import requests
import zipfile

# Constants
DATA_URL = "https://www.kaggle.com/api/v1/datasets/download/pinto391/380000-weather-data"  # Replace with your dataset's URL
DATA_DIR = "./data"
ZIP_FILE_PATH = os.path.join(DATA_DIR, "dataset.zip")
OUTPUT_FILE = os.path.join(DATA_DIR, "cleaned_data.csv")


if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Download the ZIP file
print("Downloading dataset...")
response = requests.get(DATA_URL)
if response.status_code == 200:
    with open(ZIP_FILE_PATH, "wb") as f:
        f.write(response.content)
    print(f"ZIP file downloaded and saved to {ZIP_FILE_PATH}")
else:
    raise Exception(f"Failed to download data. Status code: {response.status_code}")

# Extract the ZIP file
print("Extracting ZIP file...")
with zipfile.ZipFile(ZIP_FILE_PATH, "r") as zip_ref:
    zip_ref.extractall(DATA_DIR)

# Find the CSV file in the extracted files
csv_file = None
for file in os.listdir(DATA_DIR):
    if file.endswith(".csv"):
        csv_file = os.path.join(DATA_DIR, file)
        break

if not csv_file:
    raise FileNotFoundError("CSV file not found in the extracted dataset.")

# Load and Clean the Data
print("Loading data...")
df = pd.read_csv(csv_file)

# Data Cleaning and Transformation
print("Cleaning data...")


# - Drop rows with missing values
df.dropna(inplace=True)

# - Convert date columns to datetime format
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.dropna(subset=['date'], inplace=True)


# Assuming there's a 'temperature' column where values below -50 or above 60 are considered errors
if 'temperature' in df.columns:
    df = df[(df['temperature'] >= -50) & (df['temperature'] <= 60)]


# Save the Cleaned Data
print("Saving cleaned data...")
df.to_csv(OUTPUT_FILE, index=False)
print(f"Cleaned data saved to {OUTPUT_FILE}")

# Remove the ZIP file after extraction
os.remove(ZIP_FILE_PATH)
print(f"ZIP file {ZIP_FILE_PATH} removed after extraction.")


# In[ ]:





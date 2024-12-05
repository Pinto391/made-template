#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import requests
import zipfile

# Constants
DATA_DIR = "./data"
DATASETS = {
    "weather_data": {
        "url": "https://www.kaggle.com/api/v1/datasets/download/pinto391/380000-weather-data",
        "zip_file": os.path.join(DATA_DIR, "weather_data.zip"),
        "output_file": os.path.join(DATA_DIR, "cleaned_weather_data.csv"),
    },
    "seattle_weather": {
        "url": "https://www.kaggle.com/api/v1/datasets/download/petalme/seattle-weather-prediction-dataset",
        "zip_file": os.path.join(DATA_DIR, "seattle_weather.zip"),
        "output_file": os.path.join(DATA_DIR, "cleaned_seattle_weather.csv"),
    },
}

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def download_dataset(url, zip_file_path):
    """Download a dataset from a given URL."""
    print(f"Downloading dataset from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(zip_file_path, "wb") as f:
            f.write(response.content)
        print(f"Dataset downloaded and saved to {zip_file_path}")
    else:
        raise Exception(f"Failed to download dataset. Status code: {response.status_code}")


def extract_zip(zip_file_path, extract_to):
    """Extract a ZIP file to a specified directory."""
    print(f"Extracting {zip_file_path}...")
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted to {extract_to}")


def find_csv_file(directory):
    """Find the first CSV file in a directory."""
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            return os.path.join(directory, file)
    raise FileNotFoundError("CSV file not found in the extracted dataset.")


def clean_and_transform_data(csv_file, output_file):
    """Clean and transform the dataset."""
    print(f"Processing {csv_file}...")
    df = pd.read_csv(csv_file)

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Convert date columns to datetime format if available
    if "date_time" in df.columns:
        df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")
        df.dropna(subset=["date_time"], inplace=True)

    # Filter out invalid temperature ranges
    if "maxtempC" in df.columns:
        df = df[df["maxtempC"] <= 60]
    if "mintempC" in df.columns:
        df = df[df["mintempC"] >= -50]

    # Save the cleaned data
    print(f"Saving cleaned data to {output_file}...")
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")


def process_dataset(name, info):
    """Download, extract, and process a dataset."""
    url = info["url"]
    zip_file = info["zip_file"]
    output_file = info["output_file"]

    # Download the dataset
    download_dataset(url, zip_file)

    # Extract the dataset
    extract_zip(zip_file, DATA_DIR)

    # Find the CSV file
    csv_file = find_csv_file(DATA_DIR)

    # Clean and transform the data
    clean_and_transform_data(csv_file, output_file)

    # Remove the ZIP file after processing
    os.remove(zip_file)
    print(f"Removed ZIP file: {zip_file}\n")


def main():
    for name, info in DATASETS.items():
        print(f"Processing dataset: {name}")
        process_dataset(name, info)
    print("All datasets processed successfully.")


if __name__ == "__main__":
    main()


# In[ ]:





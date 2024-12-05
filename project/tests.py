#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import subprocess

# Constants
DATA_DIR = "data"
EXPECTED_FILES = ["cleaned_weather_data.csv", "cleaned_seattle_weather.csv"]
PIPELINE_SCRIPT = "pipeline.py"

def run_pipeline():
    """Runs the pipeline script."""
    print("Running the data pipeline...")
    result = subprocess.run(["python3", PIPELINE_SCRIPT], capture_output=True, text=True)
    if result.returncode == 0:
        print("Pipeline executed successfully.")
    else:
        print("Pipeline execution failed.")
        print(result.stderr)
        exit(1)

def validate_outputs():
    """Validates the output files."""
    print("Validating output files...")
    all_files_exist = True
    for file in EXPECTED_FILES:
        file_path = os.path.join(DATA_DIR, file)
        if os.path.exists(file_path):
            print(f"✅ Found {file_path}")
        else:
            print(f"❌ Missing {file_path}")
            all_files_exist = False
    return all_files_exist

def main():
    run_pipeline()
    if validate_outputs():
        print("✅ All tests passed. Pipeline outputs are present.")
    else:
        print("❌ Tests failed. Some outputs are missing.")
        exit(1)

if __name__ == "__main__":
    main()


# In[ ]:





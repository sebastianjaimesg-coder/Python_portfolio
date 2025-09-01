import os
import pandas as pd

# Path where the Excel files are located
Attachments_route = os.path.join(os.getcwd(), "Attachments")

# List of all .xlsx files
Excel_files = [f for f in os.listdir(Attachments_route) if f.endswith('.xlsx')]

# List for storing dataframes
dataframes = []

for File in Excel_files:
    Complete_route = os.path.join(Attachments_route, File)

    try:
        # Read only columns A through AE (indexes 0 through 30), skipping the first row.
        df = pd.read_excel(Complete_route, usecols="A:AE", skiprows=1)
        dataframes.append(df)
        print(f"✅ Read: {File}")
    except Exception as e:
        print(f"❌ error reading {File}: {e}")

# Merge all DataFrames into one
if dataframes:
    Consolidated = pd.concat(dataframes, ignore_index=True)
    Output_route = os.path.join(os.getcwd(), "consolidated.xlsx")
    Consolidated.to_excel(Output_route, index=False)
    print(f"\n📁 Consolidation completed: {Output_route}")
else:
    print("\n⚠️ No valid data was found to consolidate.")


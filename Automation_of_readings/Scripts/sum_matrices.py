import os
import pandas as pd

# Folder path with daily Excel files
folder = 'Attachments'
files = [f for f in os.listdir(folder) if f.endswith('.xlsx')]

sum_matrix = None
columns_b_f = None

for idx, file in enumerate(files):
    file_path = os.path.join(folder, file)

    try:
        df = pd.read_excel(file_path, header=1)  # Read starting from row 2
        print(f"✅ Successfully read: {file}")

        df_g_ae = df.iloc[:, 6:31]  # Columns G-AE (25 columns)
        df_b_f = df.iloc[:, 1:6]    # Columns B-F (5 columns)

        if sum_matrix is None:
            sum_matrix = df_g_ae.copy()
            columns_b_f = df_b_f.copy()
        else:
            sum_matrix += df_g_ae

    except Exception as e:
        print(f"❌ Error reading {file}: {e}")

print(f"\n📊 Total files read: {len(files)}")

# Create column A with fixed text
col_a = pd.Series(['all frontiers'] * len(sum_matrix), name='Frontier')

# Assemble final DataFrame
consolidated = pd.concat([col_a, columns_b_f, sum_matrix], axis=1)

# Save as Excel
consolidated.to_excel('total_consumption.xlsx', index=False)

print("✅ Consolidated file saved as: total_consumption.xlsx")

import os
import pandas as pd

# Folder path with daily Excel files
folder = 'Attachments'
files = [f for f in os.listdir(folder) if f.endswith('.xlsx')]

matriz_suma = None
columnas_b_f = None

for idx, file in enumerate(files):
    ruta = os.path.join(folder, file)

    try:
        df = pd.read_excel(ruta, header=1)  # Read from row 2
        print(f"✅ Leído con éxito: {file}")

        df_g_ae = df.iloc[:, 6:31]  # Columns G-AE (25 columns)
        df_b_f = df.iloc[:, 1:6]    # Columns B-F (5 columns)

        if matriz_suma is None:
            matriz_suma = df_g_ae.copy()
            columnas_b_f = df_b_f.copy()
        else:
            matriz_suma += df_g_ae

    except Exception as e:
        print(f"❌  Error reading {file}: {e}")

print(f"\n📊 Total files read: {len(files)}")

# Create column A with fixed text
columna_a = pd.Series(['todas las fronteras'] * len(matriz_suma), name='Frontera')

# Assemble final DataFrame
consolidado = pd.concat([columna_a, columnas_b_f, matriz_suma], axis=1)

# Save as Excel
consolidado.to_excel('total_consumption.xlsx', index=False)

print("✅ Consolidated saved as: total_consumption.xlsx")

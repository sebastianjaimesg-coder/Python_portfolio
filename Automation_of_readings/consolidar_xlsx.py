import os
import pandas as pd

# Ruta donde están los archivos Excel
RUTA_ADJUNTOS = os.path.join(os.getcwd(), "adjuntos")

# Lista de todos los archivos .xlsx
archivos_excel = [f for f in os.listdir(RUTA_ADJUNTOS) if f.endswith('.xlsx')]

# Lista para guardar los dataframes
dataframes = []

for archivo in archivos_excel:
    ruta_completa = os.path.join(RUTA_ADJUNTOS, archivo)

    try:
        # Leer solo las columnas A a AE (índices 0 a 30), saltando la primera fila
        df = pd.read_excel(ruta_completa, usecols="A:AE", skiprows=1)
        dataframes.append(df)
        print(f"✅ Leído: {archivo}")
    except Exception as e:
        print(f"❌ Error leyendo {archivo}: {e}")

# Unir todos los DataFrames en uno solo
if dataframes:
    consolidado = pd.concat(dataframes, ignore_index=True)
    ruta_salida = os.path.join(os.getcwd(), "consolidado_diario.xlsx")
    consolidado.to_excel(ruta_salida, index=False)
    print(f"\n📁 Consolidación completada: {ruta_salida}")
else:
    print("\n⚠️ No se encontraron datos válidos para consolidar.")

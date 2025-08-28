import os
import pandas as pd

# Ruta de carpeta con los archivos Excel diarios
carpeta = 'adjuntos'
archivos = [f for f in os.listdir(carpeta) if f.endswith('.xlsx')]

matriz_suma = None
columnas_b_f = None

for idx, archivo in enumerate(archivos):
    ruta = os.path.join(carpeta, archivo)

    try:
        df = pd.read_excel(ruta, header=1)  # Leer desde la fila 2
        print(f"✅ Leído con éxito: {archivo}")

        df_g_ae = df.iloc[:, 6:31]  # Columnas G-AE (25 columnas)
        df_b_f = df.iloc[:, 1:6]    # Columnas B-F (5 columnas)

        if matriz_suma is None:
            matriz_suma = df_g_ae.copy()
            columnas_b_f = df_b_f.copy()
        else:
            matriz_suma += df_g_ae

    except Exception as e:
        print(f"❌ Error al leer {archivo}: {e}")

print(f"\n📊 Total archivos leídos: {len(archivos)}")

# Crear columna A con texto fijo
columna_a = pd.Series(['todas las fronteras'] * len(matriz_suma), name='Frontera')

# Armar DataFrame final
consolidado = pd.concat([columna_a, columnas_b_f, matriz_suma], axis=1)

# Guardar como Excel
consolidado.to_excel('consumos_sumados.xlsx', index=False)
print("✅ Consolidado guardado como: consumos_sumados.xlsx")
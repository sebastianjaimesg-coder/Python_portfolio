import pandas as pd

# Ruta del archivo
archivo_entrada = "datos/precio_original.xlsx"
archivo_salida = "datos/precio_transformado.xlsx"

# Leer archivo
df = pd.read_excel(archivo_entrada)

# Eliminar columna "Grand Total" si existe
if 'Grand Total' in df.columns:
    df = df.drop(columns=['Grand Total'])

# Transformar de ancho a largo
df_largo = df.melt(id_vars=["FECHA"], var_name="HORA", value_name="PRECIO")

# Conversión de tipos
df_largo["HORA"] = df_largo["HORA"].astype(int)
df_largo["FECHA"] = pd.to_datetime(df_largo["FECHA"])

# Agregar franja horaria
def clasificar_franja(hora):
    return "Día" if 6 <= hora <= 17 else "Noche"

df_largo["FRANJA_HORARIA"] = df_largo["HORA"].apply(clasificar_franja)

# Agregar tipo de día
def clasificar_dia(fecha):
    dia_semana = fecha.weekday()  # lunes=0, domingo=6
    if dia_semana < 5:
        return "Ordinario"
    elif dia_semana == 5:
        return "Sábado"
    else:
        return "Domingo"

df_largo["TIPO_DIA"] = df_largo["FECHA"].apply(clasificar_dia)

# Guardar archivo transformado
df_largo.to_excel(archivo_salida, index=False)

print("✅ Transformación completa. Archivo guardado en:", archivo_salida)

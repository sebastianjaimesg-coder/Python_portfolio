import pandas as pd

# file path
input_file = "datos/original_prices.xlsx"
output_file = "datos/processed_prices.xlsx"

# reading file
df = pd.read_excel(input_file)

# Remove the “Grand Total” column if it exists.
if 'Grand Total' in df.columns:
    df = df.drop(columns=['Grand Total'])

# Transform from wide to long
df_largo = df.melt(id_vars=["FECHA"], var_name="HORA", value_name="PRECIO")

# Type conversion
df_largo["HORA"] = df_largo["HORA"].astype(int)
df_largo["FECHA"] = pd.to_datetime(df_largo["FECHA"])

# Add time slot
def clasificar_franja(hora):
    return "Día" if 6 <= hora <= 17 else "Noche"

df_largo["FRANJA_HORARIA"] = df_largo["HORA"].apply(clasificar_franja)

# Add day type
def clasificar_dia(fecha):
    dia_semana = fecha.weekday()  # monday=0, sunday=6
    if dia_semana < 5:
        return "Ordinario"
    elif dia_semana == 5:
        return "Sábado"
    else:
        return "Domingo"

df_largo["TIPO_DIA"] = df_largo["FECHA"].apply(clasificar_dia)

# Save transformed file
df_largo.to_excel(output_file, index=False)

print("✅ Complete transformation. File saved in:", output_file)


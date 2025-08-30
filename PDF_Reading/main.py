import os
import re
import pdfplumber
import pandas as pd

PDF_FOLDER = "data"
OUTPUT_EXCEL = "output/facturas_procesadas.xlsx"

def extraer_campos(texto):
    def buscar(patron, default=""):
        resultado = re.search(patron, texto, re.IGNORECASE)
        return resultado.group(1).strip() if resultado else default

    return {
        "numero_factura": buscar(r"Factura de venta No\.?\s*(\d+)"),
        "fecha_expedicion": buscar(r"Fecha de expedición\s*([\d/]+)"),
        "fecha_pago_oportuno": buscar(r"pago oportuno[:\s]*([\d/]+)"),
        "fecha_suspension": buscar(r"Fecha de suspensión\s*([\d/]+)"),
        "periodo_facturado": buscar(r"Periodo Facturado\s*([\d/]+.*?)\s*\n"),
        "total_pagar": buscar(r"Total a pagar\s*\$?\s*([\d\.,]+)"),
        "direccion": buscar(r"Dirección:\s*(.*)"),
        "ciudad_departamento": buscar(r"Ciudad y Depto:\s*(.*)"),
        "codigo_sic": buscar(r"Código SIC:\s*([^\s]+)"),
        "estrato": buscar(r"Estrato:\s*(.*)"),
        "tipo_servicio": buscar(r"Clase de servicio:\s*(.*)"),
        "razon_social": buscar(r"Razón Social:\s*(.*?)\s+Ciudad"),
        "kwh_consumidos": buscar(r"Activa\s+([\d\.]+)"),
        "reactiva_facturada": buscar(r"Reactiva Ind Facturada\s+([\d\.]+)"),
        "subtotal_energia": buscar(r"Subtotal Energía\s*\$?\s*([\d\.,]+)"),
        "otros_cobros": buscar(r"Subtotal otros cobros\s*\$?\s*([\d\.,]+)"),
        "valor_energia_reactiva": buscar(r"Reactiva Ind Facturada\s+[\d\.]+\s+\$?\s*([\d\.,]+)"),
        "componente_generacion": buscar(r"Generaci[oó]n\s*\(G\)\s*([\d\.,]+)"),
        "componente_transmision": buscar(r"Transmisi[oó]n\s*\(T\)\s*([\d\.,]+)"),
        "componente_distribucion": buscar(r"Distribuci[oó]n\s*\(D\)\s*([\d\.,]+)"),
        "componente_comercial": buscar(r"Comercializaci[oó]n\s*\(C\)\s*([\d\.,]+)"),
        "componente_perdidas": buscar(r"P[eé]rdidas\s*\(PR\)\s*([\d\.,]+)"),
        "componente_restricciones": buscar(r"Restricciones\s*\(R\)\s*([\d\.,]+)")
    }

def leer_y_procesar_pdfs(carpeta):
    registros = []
    archivos_pdf = [f for f in os.listdir(carpeta) if f.lower().endswith(".pdf")]
    
    for archivo in archivos_pdf:
        ruta = os.path.join(carpeta, archivo)
        print(f"📄 Procesando: {archivo}")
        
        with pdfplumber.open(ruta) as pdf:
            texto = "\n".join(pagina.extract_text() for pagina in pdf.pages if pagina.extract_text())
            datos = extraer_campos(texto)
            registros.append(datos)
    
    return registros

def exportar_a_excel(datos, salida):
    df = pd.DataFrame(datos)
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    df.to_excel(salida, index=False)
    print(f"\n✅ Archivo Excel guardado en: {salida}")

if __name__ == "__main__":
    registros = leer_y_procesar_pdfs(PDF_FOLDER)
    exportar_a_excel(registros, OUTPUT_EXCEL)

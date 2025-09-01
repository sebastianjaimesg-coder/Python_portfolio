import os
import re
import pdfplumber
import pandas as pd

PDF_FOLDER = "data"
OUTPUT_EXCEL = "output/processed_invoices.xlsx"

def extract_fields(text):
    """Extract key fields from invoice text using regex patterns."""
    
    def search(pattern, default=""):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else default

    return {
        "invoice_number": search(r"Factura de venta No\.?\s*(\d+)"),
        "issue_date": search(r"Fecha de expedición\s*([\d/]+)"),
        "due_date": search(r"pago oportuno[:\s]*([\d/]+)"),
        "suspension_date": search(r"Fecha de suspensión\s*([\d/]+)"),
        "billing_period": search(r"Periodo Facturado\s*([\d/]+.*?)\s*\n"),
        "total_amount": search(r"Total a pagar\s*\$?\s*([\d\.,]+)"),
        "address": search(r"Dirección:\s*(.*)"),
        "city_department": search(r"Ciudad y Depto:\s*(.*)"),
        "sic_code": search(r"Código SIC:\s*([^\s]+)"),
        "stratum": search(r"Estrato:\s*(.*)"),
        "service_type": search(r"Clase de servicio:\s*(.*)"),
        "company_name": search(r"Razón Social:\s*(.*?)\s+Ciudad"),
        "kwh_consumed": search(r"Activa\s+([\d\.]+)"),
        "reactive_billed": search(r"Reactiva Ind Facturada\s+([\d\.]+)"),
        "subtotal_energy": search(r"Subtotal Energía\s*\$?\s*([\d\.,]+)"),
        "other_charges": search(r"Subtotal otros cobros\s*\$?\s*([\d\.,]+)"),
        "reactive_energy_value": search(r"Reactiva Ind Facturada\s+[\d\.]+\s+\$?\s*([\d\.,]+)"),
        "generation_component": search(r"Generaci[oó]n\s*\(G\)\s*([\d\.,]+)"),
        "transmission_component": search(r"Transmisi[oó]n\s*\(T\)\s*([\d\.,]+)"),
        "distribution_component": search(r"Distribuci[oó]n\s*\(D\)\s*([\d\.,]+)"),
        "commercial_component": search(r"Comercializaci[oó]n\s*\(C\)\s*([\d\.,]+)"),
        "losses_component": search(r"P[eé]rdidas\s*\(PR\)\s*([\d\.,]+)"),
        "restrictions_component": search(r"Restricciones\s*\(R\)\s*([\d\.,]+)")
    }

def read_and_process_pdfs(folder):
    """Read all PDFs in the folder and extract invoice data."""
    records = []
    pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    
    for pdf_file in pdf_files:
        file_path = os.path.join(folder, pdf_file)
        print(f"📄 Processing: {pdf_file}")
        
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            data = extract_fields(text)
            records.append(data)
    
    return records

def export_to_excel(data, output_path):
    """Export extracted records to an Excel file."""
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False)
    print(f"\n✅ Excel file saved at: {output_path}")

if __name__ == "__main__":
    records = read_and_process_pdfs(PDF_FOLDER)
    export_to_excel(records, OUTPUT_EXCEL)


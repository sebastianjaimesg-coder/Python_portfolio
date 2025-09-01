# PDF Reading Automation

This project demonstrates how to **extract structured information from PDF files** using Python.
The workflow automates the process of reading user invoices (or similar PDF documents), transforming the extracted data into a **clean tabular format**, and exporting it for further analysis in **Power BI or other BI tools**.

---

## 📂 Project Structure

```
PDF_Reading/
│── Data/              # Raw PDF files (input)
│── output/            # Processed data (Excel/CSV output)
│── main.py            # Main Python script for PDF parsing
│── requirements.txt   # Dependencies
│── README.md          # Documentation
```

---

## ⚙️ How it Works

1. **Input**

   * Place PDF files inside the `Data/` folder.

2. **Processing** (`main.py`)

   * Uses Python libraries to extract relevant information (e.g., name, code, address, consumption).
   * Cleans and structures the data into tabular format.

3. **Output**

   * Processed files are exported to the `output/` folder.
   * Output formats: `.xlsx` or `.csv`.

4. **Visualization**

   * The processed data can be loaded into Power BI to analyze metrics such as:

     * Average consumption
     * Energy usage trends
     * Cost distribution

---

## 📦 Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

Run the main script:

```bash
python main.py
```

---

## 📊 Example Use Case

This pipeline was designed for the energy sector to **automatically extract data from invoices** and centralize it in a database or BI tool.
It can be adapted for other contexts where **batch PDF processing** is required (financial reports, bills, contracts, etc.).

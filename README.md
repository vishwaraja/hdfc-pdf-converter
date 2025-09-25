# HDFC PDF to CSV Converter

A robust, open-source tool to extract transaction data from HDFC Bank PDF statements and convert them to CSV format with automatic categorization and detailed analysis.

> 📖 **Read the full story**: [Building a PDF Parser for HDFC Bank Statements: From 165 Pages to CSV in Minutes](https://dev.to/vishwaraja_pathivishwa/building-a-pdf-parser-for-hdfc-bank-statements-from-165-pages-to-csv-in-minutes-34c6) on Dev.to

## 🚀 Features

- **Complete Transaction Extraction**: Extracts all transactions from HDFC Bank PDF statements
- **Automatic Categorization**: Intelligently categorizes transactions (UPI, Foreign Exchange, Salary, etc.)
- **Multiple Output Formats**: CSV, Excel, and detailed summary reports
- **Robust Parsing**: Handles multi-line narrations and various PDF formats
- **Data Validation**: Ensures data integrity and completeness
- **Beautiful Web Interface**: User-friendly web UI for non-technical users
- **Command Line Tool**: Powerful CLI for developers and automation

## 📦 Installation

### Option 1: Clone and Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/vishwaraja/hdfc-pdf-converter.git
cd hdfc-pdf-converter

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Direct Download

```bash
# Download and extract the latest release
wget https://github.com/vishwaraja/hdfc-pdf-converter/archive/main.zip
unzip main.zip
cd hdfc-pdf-converter-main
pip install -r requirements.txt
```

## 🌐 Web Interface

**🚀 Live Demo: [https://pdf2csv.in](https://pdf2csv.in)**

For non-technical users, we provide a beautiful web interface where you can:
- Drag and drop your PDF file
- Watch real-time processing progress
- Download CSV, Excel, and summary files
- Use the live demo or run locally with the backend server

## 📖 Usage

### Web Interface (Recommended for most users)

**Option 1: Use Live Demo (Easiest)**
1. **Visit**: [https://pdf2csv.in](https://pdf2csv.in)
2. **Upload PDF**: Drag and drop your HDFC PDF statement
3. **Download Results**: Get your CSV, Excel, and summary files

**Option 2: Run Locally**
1. **Install Dependencies**: `pip install -r web-ui/requirements.txt`
2. **Start Server**: `cd web-ui && python start_server.py`
3. **Open Browser**: Go to `http://localhost:5000`
4. **Upload PDF**: Drag and drop your HDFC PDF statement
5. **Download Results**: Get your CSV, Excel, and summary files

### Command Line Interface

### Basic Usage

```bash
# Convert a PDF statement (creates ./results/ directory automatically)
python src/hdfc_converter.py your_statement.pdf

# Custom output directory
python src/hdfc_converter.py statement.pdf --output-dir ./my_results

# Verbose logging for debugging
python src/hdfc_converter.py statement.pdf --verbose

# Convert PDF from different directory
python src/hdfc_converter.py /path/to/statements/hdfc_2024.pdf
```

### Command Line Options

```bash
python src/hdfc_converter.py PDF_PATH [OPTIONS]

Arguments:
  PDF_PATH              Path to the HDFC PDF statement file (required)

Options:
  -o, --output-dir DIR  Output directory for CSV files (default: results)
  -v, --verbose         Enable verbose logging
  -h, --help            Show help message
```

### Programmatic Usage

```python
from src.hdfc_converter import HDFCConverter

# Initialize converter
converter = HDFCConverter()

# Convert PDF to CSV
result = converter.convert('statement.pdf', 'output_dir')

if result['success']:
    print(f"Extracted {result['transaction_count']} transactions")
    print(f"CSV saved to: {result['csv_file']}")
    print(f"Excel saved to: {result['excel_file']}")
    print(f"Summary saved to: {result['summary_file']}")
else:
    print(f"Error: {result['error']}")
```

## 📊 Output Files

The converter generates several output files:

- **`hdfc_transactions_YYYYMMDD_HHMMSS.csv`**: Complete transaction data
- **`hdfc_transactions_YYYYMMDD_HHMMSS.xlsx`**: Excel version with formatting
- **`EXTRACTION_REPORT_YYYYMMDD_HHMMSS.md`**: Detailed analysis report
- **`summary_YYYYMMDD_HHMMSS.csv`**: Category-wise breakdown
- **`extraction_stats_YYYYMMDD_HHMMSS.csv`**: Processing statistics

## 🎯 Transaction Categories

The tool automatically categorizes transactions into:

- **UPI Payments**: UPI, IMPS, NEFT, RTGS transactions
- **Foreign Exchange**: International transfers and currency conversions
- **Salary & Employment**: Salary credits and payroll transactions
- **Card Payments**: ATM withdrawals, POS transactions, card payments
- **Cheque Transactions**: Cheque payments and deposits
- **Investment Income**: Interest, dividends, and investment returns
- **Utilities**: Electricity, water, gas, and other utility bills
- **Shopping & Retail**: Online and offline purchases
- **Food & Dining**: Restaurant, food delivery, and dining expenses
- **Charitable & Donations**: Donations and charitable contributions
- **And many more...**

## 🔧 Technical Details

- **PDF Processing**: Uses Camelot and pdfplumber for robust table extraction
- **Data Processing**: Pandas for data manipulation and analysis
- **Categorization**: Advanced regex patterns and keyword matching
- **Multi-line Support**: Handles transactions with multi-line descriptions
- **Error Handling**: Comprehensive error handling and validation

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src
```

## 📁 Project Structure

```
hdfc-pdf-converter/
├── src/
│   └── hdfc_converter.py      # Main converter class
├── web-ui/                    # Web interface
│   ├── index.html            # Frontend HTML
│   ├── styles.css            # CSS styling
│   ├── script.js             # Frontend JavaScript
│   ├── backend.py            # Flask backend
│   ├── start_server.py       # Server startup script
│   └── requirements.txt      # Web UI dependencies
├── examples/                  # Usage examples
├── tests/                     # Unit tests
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
├── Dockerfile                 # Docker configuration
├── railway.json              # Railway deployment config
├── setup.py                  # Package setup
└── requirements.txt           # Python dependencies
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/vishwaraja/hdfc-pdf-converter.git
cd hdfc-pdf-converter

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/vishwaraja/hdfc-pdf-converter/issues)
- **Email**: vishwaraja.pathi@adiyogitech.com
- **Technical Article**: [Read the full story on Dev.to](https://dev.to/vishwaraja_pathivishwa/building-a-pdf-parser-for-hdfc-bank-statements-from-165-pages-to-csv-in-minutes-34c6)

## 📖 Related Content

- **Technical Article**: [Building a PDF Parser for HDFC Bank Statements: From 165 Pages to CSV in Minutes](https://dev.to/vishwaraja_pathivishwa/building-a-pdf-parser-for-hdfc-bank-statements-from-165-pages-to-csv-in-minutes-34c6) on Dev.to
- **Author**: [@vishwaraja_pathivishwa](https://dev.to/vishwaraja_pathivishwa) on Dev.to

## 🔄 Version History

- **v1.0.0** - Initial release with full HDFC PDF support
- **v1.1.0** - Added web interface and improved categorization
- **v1.2.0** - Enhanced multi-line transaction support

---

*Made with ❤️ for the HDFC Bank community*
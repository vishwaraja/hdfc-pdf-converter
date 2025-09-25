# HDFC PDF to CSV Converter

A robust, open-source tool to extract transaction data from HDFC Bank PDF statements and convert them to CSV format with automatic categorization and detailed analysis.

## 🚀 Features

- **Complete Transaction Extraction**: Extracts all transactions from HDFC Bank PDF statements
- **Multi-line Narration Support**: Handles transactions with multi-line descriptions
- **Automatic Categorization**: Categorizes transactions into meaningful groups (UPI, Foreign Exchange, Salary, etc.)
- **Multiple Output Formats**: Generates CSV, Excel, and Markdown reports
- **Detailed Analytics**: Provides comprehensive financial summaries and category breakdowns
- **Command Line Interface**: Easy-to-use CLI with flexible options
- **Robust Error Handling**: Handles various PDF formats and edge cases
- **Page-by-page Statistics**: Detailed extraction statistics for verification

## 📋 Requirements

- Python 3.8 or higher
- HDFC Bank PDF statement (password-protected or unprotected)

## 🛠️ Installation

### Option 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/vishwarajapathi/hdfc-pdf-converter.git
cd hdfc-pdf-converter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Option 2: Direct Installation

```bash
pip install hdfc-pdf-converter
```

## 📖 Usage

### Basic Usage

```bash
# Convert a PDF statement
python src/hdfc_converter.py your_statement.pdf

# Use default PDF file
python src/hdfc_converter.py --default

# Specify output directory
python src/hdfc_converter.py statement.pdf --output-dir ./results

# Enable verbose logging
python src/hdfc_converter.py statement.pdf --verbose
```

### Command Line Options

```bash
python src/hdfc_converter.py [PDF_PATH] [OPTIONS]

Arguments:
  PDF_PATH              Path to the HDFC PDF statement file

Options:
  -o, --output-dir DIR  Output directory for CSV files (default: output)
  --default             Use default PDF path (hdfc_bank_statement_unprotected.pdf)
  -v, --verbose         Enable verbose logging
  -h, --help            Show help message
```

### Programmatic Usage

```python
from src.hdfc_converter import HDFCConverter

# Initialize converter
converter = HDFCConverter('path/to/statement.pdf', output_dir='./results')

# Convert PDF to CSV
success = converter.convert()

if success:
    print("Conversion completed successfully!")
else:
    print("Conversion failed!")
```

## 📊 Output Files

The converter generates several output files:

1. **`hdfc_transactions_YYYYMMDD_HHMMSS.csv`** - Main transaction data
2. **`hdfc_transactions_YYYYMMDD_HHMMSS.xlsx`** - Excel version
3. **`extraction_stats_YYYYMMDD_HHMMSS.csv`** - Page-by-page statistics
4. **`summary_YYYYMMDD_HHMMSS.csv`** - Category-wise summary
5. **`EXTRACTION_REPORT_YYYYMMDD_HHMMSS.md`** - Detailed markdown report
6. **`hdfc_conversion.log`** - Conversion log file

## 📈 Transaction Categories

The tool automatically categorizes transactions into:

- **Foreign Exchange** - International transactions and remittances
- **Salary & Employment** - Salary payments and employment-related transactions
- **UPI Payments** - UPI-based digital payments
- **Card Payments** - Credit/debit card transactions
- **Cheque Transactions** - Cheque-based payments
- **Personal Transfers** - NEFT/RTGS/IMPS transfers
- **Charitable & Donations** - Donations and charity payments
- **Investment Income** - Interest, dividends, and investment returns
- **Banking & Financial Services** - Bank charges and fees
- **Utilities** - Electricity, water, gas bills
- **Shopping & Retail** - Online and offline shopping
- **Food & Dining** - Restaurant and food delivery expenses
- **Transportation** - Fuel, taxi, and transport expenses
- **Communication** - Mobile, internet, and communication bills
- **Entertainment** - Movies, streaming, and entertainment expenses
- **Insurance & Medical** - Health insurance and medical expenses
- **Education** - Educational expenses and courses
- **Government & Taxes** - Tax payments and government fees
- **Lottery & Gambling** - Lottery and gambling transactions
- **Refunds** - Various merchant refunds
- **Other** - Uncategorized transactions

## 🔧 Configuration

### PDF Requirements

- **Format**: HDFC Bank PDF statements
- **Structure**: Standard 7-column transaction table
- **Pages**: Any number of pages (tested with 165+ pages)
- **Security**: Works with both password-protected and unprotected PDFs

### Column Structure

The tool expects the following column structure:
1. **Date** - Transaction date
2. **Narration** - Transaction description (can span multiple lines)
3. **Reference Number** - Cheque/Reference number
4. **Value Date** - Value date
5. **Withdrawal Amount** - Debit amount
6. **Deposit Amount** - Credit amount
7. **Closing Balance** - Account balance

## 🐛 Troubleshooting

### Common Issues

1. **"No transactions found"**
   - Ensure the PDF is a valid HDFC Bank statement
   - Check if the PDF is password-protected (remove password first)
   - Verify the PDF contains transaction tables

2. **"Module not found" errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Ensure you're using Python 3.8+

3. **"Permission denied" errors**
   - Check file permissions
   - Ensure output directory is writable

4. **Low extraction rate**
   - Try with `--verbose` flag to see detailed logs
   - Check if PDF format matches expected structure

### Debug Mode

```bash
# Enable verbose logging for debugging
python src/hdfc_converter.py statement.pdf --verbose
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🚀 **Ways to Contribute**

- **🐛 Bug Reports**: Found a bug? Please report it using our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
- **💡 Feature Requests**: Have an idea? Use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
- **📝 Documentation**: Help improve our docs, examples, or README
- **🧪 Testing**: Test with different PDF formats and report issues
- **🔧 Code**: Submit pull requests for bug fixes or new features

### 🛠️ **Development Setup**

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/your-username/hdfc-pdf-converter.git`
3. **Create a branch**: `git checkout -b feature/your-feature-name`
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Make your changes**
6. **Run tests**: `pytest tests/`
7. **Submit a pull request**

### 📋 **Contribution Guidelines**

- Follow our [Code of Conduct](CODE_OF_CONDUCT.md)
- Read our [Contributing Guide](CONTRIBUTING.md)
- Use our [Pull Request Template](.github/pull_request_template.md)
- Ensure all tests pass
- Update documentation for new features

### 🏷️ **Good First Issues**

Look for issues labeled with:
- `good first issue` - Perfect for newcomers
- `help wanted` - Community help needed
- `documentation` - Documentation improvements
- `bug` - Bug fixes needed

### Development Setup

```bash
# Clone repository
git clone https://github.com/vishwarajapathi/hdfc-pdf-converter.git
cd hdfc-pdf-converter

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black src/

# Lint code
flake8 src/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Camelot](https://camelot-py.readthedocs.io/) for PDF table extraction
- Uses [Pandas](https://pandas.pydata.org/) for data processing
- Inspired by the need for better bank statement analysis tools

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Open an [issue](https://github.com/vishwarajapathi/hdfc-pdf-converter/issues)
3. Contact: vishwarajapathi@example.com

## 🔄 Version History

- **v1.0.0** - Initial release with full HDFC PDF support
  - Complete transaction extraction
  - Automatic categorization
  - Multiple output formats
  - Command line interface

---

**Made with ❤️ for the HDFC Bank community**

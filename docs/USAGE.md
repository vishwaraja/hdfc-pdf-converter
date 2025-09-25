# Usage Guide

This guide provides detailed instructions on how to use the HDFC PDF to CSV Converter.

## Quick Start

1. **Prepare your PDF**
   - Ensure your HDFC Bank statement is in PDF format
   - Remove password protection if present
   - Place the PDF file in an accessible location

2. **Run the converter**
   ```bash
   python src/hdfc_converter.py your_statement.pdf
   ```

3. **Check results**
   - Output files will be created in the `output` directory
   - Review the generated CSV and summary files

## Command Line Usage

### Basic Commands

```bash
# Convert a PDF statement
python src/hdfc_converter.py statement.pdf

# Use default PDF file
python src/hdfc_converter.py --default

# Specify custom output directory
python src/hdfc_converter.py statement.pdf --output-dir ./my_results

# Enable verbose logging
python src/hdfc_converter.py statement.pdf --verbose
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `PDF_PATH` | Path to HDFC PDF statement | `statement.pdf` |
| `-o, --output-dir` | Output directory for CSV files | `--output-dir ./results` |
| `--default` | Use default PDF path | `--default` |
| `-v, --verbose` | Enable verbose logging | `--verbose` |
| `-h, --help` | Show help message | `--help` |

### Examples

```bash
# Basic conversion
python src/hdfc_converter.py bank_statement.pdf

# Custom output directory
python src/hdfc_converter.py bank_statement.pdf -o ./converted_data

# Verbose output for debugging
python src/hdfc_converter.py bank_statement.pdf --verbose

# Use default PDF file
python src/hdfc_converter.py --default

# Get help
python src/hdfc_converter.py --help
```

## Programmatic Usage

### Basic Usage

```python
from src.hdfc_converter import HDFCConverter

# Initialize converter
converter = HDFCConverter('statement.pdf', output_dir='./results')

# Convert PDF to CSV
success = converter.convert()

if success:
    print("Conversion completed successfully!")
else:
    print("Conversion failed!")
```

### Advanced Usage

```python
from src.hdfc_converter import HDFCConverter

# Initialize converter
converter = HDFCConverter('statement.pdf', output_dir='./results')

# Extract transactions
transactions, page_stats = converter.extract_transactions()

# Categorize transactions
categorized = converter.categorize_transactions(transactions)

# Generate summary
summary = converter.generate_summary(categorized)

# Save results
output_files = converter.save_results(categorized, page_stats, summary)

print(f"Files saved: {output_files}")
```

### Batch Processing

```python
import os
from src.hdfc_converter import HDFCConverter

# List of PDF files to process
pdf_files = [
    'statement_2023.pdf',
    'statement_2024.pdf',
    'statement_2025.pdf'
]

for pdf_file in pdf_files:
    if os.path.exists(pdf_file):
        print(f"Processing {pdf_file}...")
        
        output_dir = f"output_{pdf_file.replace('.pdf', '')}"
        converter = HDFCConverter(pdf_file, output_dir)
        success = converter.convert()
        
        if success:
            print(f"✅ {pdf_file} processed successfully!")
        else:
            print(f"❌ Failed to process {pdf_file}")
```

## Output Files

The converter generates several output files:

### 1. Transaction Data
- **`hdfc_transactions_YYYYMMDD_HHMMSS.csv`** - Main transaction data
- **`hdfc_transactions_YYYYMMDD_HHMMSS.xlsx`** - Excel version

**Columns:**
- Date
- Narration
- Reference_Number
- Value_Date
- Withdrawal_Amount
- Deposit_Amount
- Closing_Balance
- Page_Number
- Category

### 2. Statistics
- **`extraction_stats_YYYYMMDD_HHMMSS.csv`** - Page-by-page statistics

**Columns:**
- Page
- Rows_Processed
- Valid_Transactions

### 3. Summary
- **`summary_YYYYMMDD_HHMMSS.csv`** - Category-wise summary
- **`EXTRACTION_REPORT_YYYYMMDD_HHMMSS.md`** - Detailed markdown report

### 4. Logs
- **`hdfc_conversion.log`** - Conversion log file

## Understanding the Output

### Transaction Categories

The converter automatically categorizes transactions:

| Category | Description | Examples |
|----------|-------------|----------|
| Foreign Exchange | International transactions | USD remittances, foreign transfers |
| Salary & Employment | Employment income | Salary credits, payroll |
| UPI Payments | UPI transactions | UPI payments to merchants |
| Card Payments | Card transactions | POS, ATM, card payments |
| Cheque Transactions | Cheque payments | Cheque-based transactions |
| Personal Transfers | Bank transfers | NEFT, RTGS, IMPS |
| Charitable & Donations | Donations | Charity payments, donations |
| Investment Income | Investment returns | Interest, dividends |
| Banking & Financial Services | Bank charges | Fees, charges, penalties |
| Utilities | Utility bills | Electricity, water, gas |
| Shopping & Retail | Retail purchases | Online shopping, stores |
| Food & Dining | Food expenses | Restaurants, food delivery |
| Transportation | Transport costs | Fuel, taxi, transport |
| Communication | Communication bills | Mobile, internet |
| Entertainment | Entertainment | Movies, streaming |
| Insurance & Medical | Health expenses | Insurance, medical |
| Education | Educational expenses | Courses, education |
| Government & Taxes | Government payments | Taxes, government fees |
| Lottery & Gambling | Gambling | Lottery, gambling |
| Refunds | Refunds | Merchant refunds |
| Other | Uncategorized | Other transactions |

### Financial Summary

The summary includes:
- Total number of transactions
- Total withdrawals and deposits
- Net amount (deposits - withdrawals)
- Category-wise breakdown
- Date range of transactions

## Best Practices

### 1. PDF Preparation
- Remove password protection before conversion
- Ensure PDF is not corrupted
- Use the original PDF from HDFC Bank

### 2. File Organization
- Keep PDF files in a dedicated folder
- Use descriptive names for output directories
- Regularly clean up old output files

### 3. Data Verification
- Always review the generated CSV files
- Check transaction counts against the original PDF
- Verify financial totals

### 4. Error Handling
- Use verbose mode for debugging: `--verbose`
- Check log files for detailed error information
- Test with a small PDF first

## Troubleshooting

### Common Issues

1. **"No transactions found"**
   - Check if PDF is a valid HDFC Bank statement
   - Ensure PDF is not password-protected
   - Verify PDF contains transaction tables

2. **"Permission denied" errors**
   - Check file permissions
   - Ensure output directory is writable
   - Run with appropriate permissions

3. **"Module not found" errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)
   - Verify virtual environment is activated

4. **Low extraction rate**
   - Use verbose mode to see detailed logs
   - Check if PDF format matches expected structure
   - Verify PDF is not corrupted

### Debug Mode

```bash
# Enable verbose logging
python src/hdfc_converter.py statement.pdf --verbose

# Check log file
tail -f hdfc_conversion.log
```

### Getting Help

If you encounter issues:

1. Check the [troubleshooting section](#troubleshooting)
2. Review the log file: `hdfc_conversion.log`
3. Open an [issue](https://github.com/vishwarajapathi/hdfc-pdf-converter/issues)
4. Check the [FAQ](FAQ.md)

## Advanced Features

### Custom Categorization

You can modify the categorization logic by editing the `categorize_transactions` method in the converter.

### Custom Output Formats

The converter supports multiple output formats:
- CSV (default)
- Excel (.xlsx)
- Markdown reports

### Integration with Other Tools

The generated CSV files can be easily imported into:
- Excel
- Google Sheets
- Accounting software
- Data analysis tools (Pandas, R, etc.)

## Performance Tips

1. **Large PDFs**: For PDFs with 100+ pages, the conversion may take several minutes
2. **Memory Usage**: Large PDFs may require 2GB+ RAM
3. **Disk Space**: Ensure sufficient disk space for output files
4. **Batch Processing**: Process multiple PDFs sequentially to avoid memory issues

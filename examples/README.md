# Examples

This directory contains example scripts showing how to use the HDFC PDF to CSV Converter.

## Files

- **`example_usage.py`** - Comprehensive examples showing different ways to use the converter
- **`README.md`** - This file

## Running Examples

```bash
# Navigate to the examples directory
cd examples

# Run the example script
python example_usage.py
```

## Example Scenarios

### 1. Basic Usage
```python
from hdfc_converter import HDFCConverter

converter = HDFCConverter('statement.pdf', 'output')
success = converter.convert()
```

### 2. Custom Processing
```python
# Extract transactions
transactions, page_stats = converter.extract_transactions()

# Categorize manually
categorized = converter.categorize_transactions(transactions)

# Generate custom summary
summary = converter.generate_summary(categorized)
```

### 3. Batch Processing
```python
pdf_files = ['statement1.pdf', 'statement2.pdf', 'statement3.pdf']

for pdf_file in pdf_files:
    converter = HDFCConverter(pdf_file, f'output_{pdf_file}')
    converter.convert()
```

## Sample Data

To test the examples, you can use:
- Your own HDFC Bank PDF statements
- The sample PDF provided in the main directory
- Any HDFC Bank statement with the standard 7-column format

## Notes

- Make sure to install all dependencies before running examples
- Examples assume the PDF files are in the same directory
- Adjust file paths as needed for your setup

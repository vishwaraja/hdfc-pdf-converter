#!/usr/bin/env python3
"""
HDFC Bank PDF Statement to CSV Converter

A robust tool to extract transaction data from HDFC Bank PDF statements
and convert them to CSV format with proper categorization.

Author: Vishwaraja Pathi
Email: vishwaraja.pathi@adiyogitech.com
License: MIT
Repository: https://github.com/vishwaraja/hdfc-pdf-converter
"""

import argparse
import sys
import os
import pandas as pd
import camelot
from datetime import datetime
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hdfc_conversion.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class HDFCConverter:
    """Main converter class for HDFC Bank PDF statements."""
    
    def __init__(self, pdf_path, output_dir=None):
        """
        Initialize the converter.
        
        Args:
            pdf_path (str): Path to the HDFC PDF statement
            output_dir (str, optional): Output directory for CSV files
        """
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir) if output_dir else Path('output')
        self.output_dir.mkdir(exist_ok=True)
        
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Initialized converter for: {self.pdf_path}")
        logger.info(f"Output directory: {self.output_dir}")
    
    def extract_transactions(self):
        """Extract all transactions from the PDF."""
        logger.info("Starting transaction extraction...")
        
        all_transactions = []
        page_stats = []
        
        try:
            # Extract tables from all pages with memory optimization
            logger.info(f"Attempting to extract tables from: {self.pdf_path}")
            tables = camelot.read_pdf(
                str(self.pdf_path), 
                pages='all', 
                flavor='lattice',
                line_scale=40,
                split_text=True,  # Split text to avoid memory issues
                flag_size=True,   # Flag size to optimize memory
                copy_text=['v']   # Copy text vertically to reduce memory usage
            )
            
            logger.info(f"Found {len(tables)} tables across all pages")
            
            if len(tables) == 0:
                logger.warning("No tables found with lattice method, trying stream method...")
                tables = camelot.read_pdf(
                    str(self.pdf_path), 
                    pages='all', 
                    flavor='stream',
                    split_text=True,
                    flag_size=True,
                    copy_text=['v']
                )
                logger.info(f"Found {len(tables)} tables with stream method")
            
            # Process tables in batches to manage memory
            batch_size = 5  # Process 5 tables at a time
            for batch_start in range(0, len(tables), batch_size):
                batch_end = min(batch_start + batch_size, len(tables))
                batch_tables = tables[batch_start:batch_end]
                
                logger.info(f"Processing batch {batch_start//batch_size + 1}: tables {batch_start+1}-{batch_end}")
                
                for i, table in enumerate(batch_tables):
                    try:
                        df = table.df
                        
                        # Get page number
                        page_num = table.page
                        
                        logger.info(f"Table {i+1} on page {page_num}: {len(df)} rows, {len(df.columns)} columns")
                        
                        # Skip if table is empty
                        if len(df) < 1:
                            logger.info(f"Skipping table {i+1} on page {page_num}: empty table")
                            continue
                        
                        # Check if this looks like a transaction table (at least 5 columns)
                        if len(df.columns) >= 5:
                            logger.info(f"Processing table {i+1} on page {page_num}: {len(df)} rows, {len(df.columns)} columns")
                            # First page has headers, others don't
                            if page_num == 1:
                                # Skip header row on first page
                                transaction_rows = df.iloc[1:]
                            else:
                                # No headers on subsequent pages
                                transaction_rows = df
                            
                            # Check if rows are concatenated with newlines (common camelot issue)
                            if len(transaction_rows) == 1 and '\n' in str(transaction_rows.iloc[0, 0]):
                                # Split concatenated rows
                                split_transactions = self._split_concatenated_rows(transaction_rows.iloc[0], page_num)
                                all_transactions.extend(split_transactions)
                            else:
                                # Process each transaction row normally
                                for _, row in transaction_rows.iterrows():
                                    if self._is_valid_transaction_row(row):
                                        transaction = self._parse_transaction_row(row, page_num)
                                        if transaction:
                                            all_transactions.append(transaction)
                            
                            page_stats.append({
                                'Page': page_num,
                                'Rows_Processed': len(transaction_rows),
                                'Valid_Transactions': len([t for t in all_transactions if t['Page_Number'] == page_num])
                            })
                            
                            logger.info(f"Page {page_num}: Processed {len(transaction_rows)} rows")
                    
                    except Exception as e:
                        logger.warning(f"Error processing table {i}: {e}")
                        continue
                
                # Clear memory after each batch
                import gc
                gc.collect()
            
            logger.info(f"Total transactions extracted: {len(all_transactions)}")
            return all_transactions, page_stats
            
        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            raise
    
    def _split_concatenated_rows(self, concatenated_row, page_num):
        """Split a concatenated row into individual transactions."""
        transactions = []
        
        try:
            # Get all column data as strings
            dates = str(concatenated_row.iloc[0]).split('\n')
            narrations = str(concatenated_row.iloc[1]).split('\n') if len(concatenated_row) > 1 else []
            ref_nos = str(concatenated_row.iloc[2]).split('\n') if len(concatenated_row) > 2 else []
            value_dates = str(concatenated_row.iloc[3]).split('\n') if len(concatenated_row) > 3 else []
            withdrawals = str(concatenated_row.iloc[4]).split('\n') if len(concatenated_row) > 4 else []
            deposits = str(concatenated_row.iloc[5]).split('\n') if len(concatenated_row) > 5 else []
            balances = str(concatenated_row.iloc[6]).split('\n') if len(concatenated_row) > 6 else []
            
            # Find the maximum length to iterate through
            max_len = max(len(dates), len(narrations), len(ref_nos), len(value_dates), 
                         len(withdrawals), len(deposits), len(balances))
            
            for i in range(max_len):
                # Get values for this transaction (with fallback to empty string)
                date = dates[i] if i < len(dates) else ''
                narration = narrations[i] if i < len(narrations) else ''
                ref_no = ref_nos[i] if i < len(ref_nos) else ''
                value_date = value_dates[i] if i < len(value_dates) else ''
                withdrawal = withdrawals[i] if i < len(withdrawals) else ''
                deposit = deposits[i] if i < len(deposits) else ''
                balance = balances[i] if i < len(balances) else ''
                
                # Skip if date is empty or doesn't look like a date
                if not date or not self._is_valid_date(date):
                    continue
                
                # Clean up amounts
                withdrawal = self._clean_amount(withdrawal)
                deposit = self._clean_amount(deposit)
                balance = self._clean_amount(balance)
                
                transaction = {
                    'Date': date.strip(),
                    'Narration': narration.strip(),
                    'Reference_Number': ref_no.strip(),
                    'Value_Date': value_date.strip(),
                    'Withdrawal_Amount': withdrawal,
                    'Deposit_Amount': deposit,
                    'Closing_Balance': balance,
                    'Page_Number': page_num
                }
                
                transactions.append(transaction)
                
        except Exception as e:
            logger.warning(f"Error splitting concatenated rows: {e}")
            
        return transactions
    
    def _is_valid_date(self, date_str):
        """Check if a string looks like a valid date."""
        if not date_str or date_str == 'nan':
            return False
        date_str = str(date_str).strip()
        return (len(date_str) >= 8 and 
                any(char.isdigit() for char in date_str) and
                '/' in date_str)
    
    def _is_valid_transaction_row(self, row):
        """Check if a row contains valid transaction data."""
        # Check if first column looks like a date
        first_col = str(row.iloc[0]).strip()
        return (len(first_col) >= 8 and 
                any(char.isdigit() for char in first_col) and
                '/' in first_col)
    
    def _parse_transaction_row(self, row, page_num):
        """Parse a single transaction row."""
        try:
            # Handle multi-line narrations
            narration_parts = []
            date = None
            withdrawal = None
            deposit = None
            balance = None
            ref_no = None
            value_date = None
            
            # First column should be date
            date = str(row.iloc[0]).strip()
            
            # Last column should be balance
            balance = str(row.iloc[-1]).strip()
            
            # Second to last column should be deposit amount
            deposit = str(row.iloc[-2]).strip()
            
            # Third to last column should be withdrawal amount
            withdrawal = str(row.iloc[-3]).strip()
            
            # Fourth to last column should be value date
            value_date = str(row.iloc[-4]).strip()
            
            # Fifth to last column should be reference number
            ref_no = str(row.iloc[-5]).strip()
            
            # Everything in between is narration (can span multiple columns)
            narration_start = 1
            narration_end = len(row) - 5
            
            for i in range(narration_start, narration_end):
                part = str(row.iloc[i]).strip()
                if part and part != 'nan':
                    narration_parts.append(part)
            
            narration = ' '.join(narration_parts)
            
            # Clean up amounts
            withdrawal = self._clean_amount(withdrawal)
            deposit = self._clean_amount(deposit)
            balance = self._clean_amount(balance)
            
            return {
                'Date': date,
                'Narration': narration,
                'Reference_Number': ref_no,
                'Value_Date': value_date,
                'Withdrawal_Amount': withdrawal,
                'Deposit_Amount': deposit,
                'Closing_Balance': balance,
                'Page_Number': page_num
            }
            
        except Exception as e:
            logger.warning(f"Error parsing row: {e}")
            return None
    
    def _clean_amount(self, amount_str):
        """Clean and format amount strings."""
        if not amount_str or amount_str == 'nan':
            return '0.00'
        
        # Remove commas and extra spaces
        cleaned = str(amount_str).replace(',', '').strip()
        
        # If it's just a number, format it
        try:
            if cleaned.replace('.', '').replace('-', '').isdigit():
                return f"{float(cleaned):.2f}"
        except:
            pass
        
        return cleaned
    
    def categorize_transactions(self, transactions):
        """Categorize transactions for better analysis."""
        logger.info("Categorizing transactions...")
        
        categorized = []
        for transaction in transactions:
            narration = transaction['Narration'].lower()
            
            # Determine category
            if any(word in narration for word in ['salary', 'payroll', 'betterplace']):
                category = 'Salary & Employment'
            elif any(word in narration for word in ['foreign', 'usd', 'eur', 'gbp', 'inw']):
                category = 'Foreign Exchange'
            elif any(word in narration for word in ['upi']):
                category = 'UPI Payments'
            elif any(word in narration for word in ['card', 'pos', 'atm']):
                category = 'Card Payments'
            elif any(word in narration for word in ['chq', 'cheque']):
                category = 'Cheque Transactions'
            elif any(word in narration for word in ['transfer', 'trf', 'neft', 'rtgs', 'imps']):
                category = 'Personal Transfers'
            elif any(word in narration for word in ['tasmac', 'lottery']):
                category = 'Lottery & Gambling'
            elif any(word in narration for word in ['donation', 'charity', 'isha']):
                category = 'Charitable & Donations'
            elif any(word in narration for word in ['interest', 'dividend']):
                category = 'Investment Income'
            elif any(word in narration for word in ['refund']):
                category = 'Refunds'
            elif any(word in narration for word in ['charge', 'fee', 'banking']):
                category = 'Banking & Financial Services'
            else:
                category = 'Other'
            
            transaction['Category'] = category
            categorized.append(transaction)
        
        logger.info(f"Categorized {len(categorized)} transactions")
        return categorized
    
    def generate_summary(self, transactions):
        """Generate summary statistics."""
        logger.info("Generating summary statistics...")
        
        df = pd.DataFrame(transactions)
        
        # Convert amounts to numeric
        df['Withdrawal_Numeric'] = pd.to_numeric(
            df['Withdrawal_Amount'].str.replace(',', ''), 
            errors='coerce'
        )
        df['Deposit_Numeric'] = pd.to_numeric(
            df['Deposit_Amount'].str.replace(',', ''), 
            errors='coerce'
        )
        
        # Calculate totals
        total_withdrawals = df['Withdrawal_Numeric'].sum()
        total_deposits = df['Deposit_Numeric'].sum()
        net_amount = total_deposits - total_withdrawals
        
        # Category breakdown
        category_summary = df.groupby('Category').agg({
            'Withdrawal_Numeric': 'sum',
            'Deposit_Numeric': 'sum',
            'Date': 'count'
        }).round(2)
        
        category_summary['Net_Amount'] = (
            category_summary['Deposit_Numeric'] - category_summary['Withdrawal_Numeric']
        )
        
        summary = {
            'total_transactions': len(df),
            'total_withdrawals': total_withdrawals,
            'total_deposits': total_deposits,
            'net_amount': net_amount,
            'category_breakdown': category_summary,
            'date_range': {
                'start': df['Date'].min(),
                'end': df['Date'].max()
            }
        }
        
        return summary
    
    def save_results(self, transactions, page_stats, summary):
        """Save all results to files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save main transaction CSV
        transactions_file = self.output_dir / f"hdfc_transactions_{timestamp}.csv"
        df = pd.DataFrame(transactions)
        df.to_csv(transactions_file, index=False)
        logger.info(f"Saved transactions to: {transactions_file}")
        
        # Save Excel version
        excel_file = self.output_dir / f"hdfc_transactions_{timestamp}.xlsx"
        df.to_excel(excel_file, index=False)
        logger.info(f"Saved Excel file to: {excel_file}")
        
        # Save page statistics
        stats_file = self.output_dir / f"extraction_stats_{timestamp}.csv"
        pd.DataFrame(page_stats).to_csv(stats_file, index=False)
        logger.info(f"Saved page statistics to: {stats_file}")
        
        # Save summary
        summary_file = self.output_dir / f"summary_{timestamp}.csv"
        summary_df = summary['category_breakdown'].reset_index()
        summary_df.to_csv(summary_file, index=False)
        logger.info(f"Saved summary to: {summary_file}")
        
        # Generate markdown report
        self._generate_markdown_report(summary, timestamp)
        
        return {
            'transactions_file': transactions_file,
            'excel_file': excel_file,
            'stats_file': stats_file,
            'summary_file': summary_file
        }
    
    def _generate_markdown_report(self, summary, timestamp):
        """Generate a markdown summary report."""
        report_file = self.output_dir / f"EXTRACTION_REPORT_{timestamp}.md"
        
        with open(report_file, 'w') as f:
            f.write("# HDFC Bank Statement Analysis Report\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"**Source**: {self.pdf_path.name}\n\n")
            
            f.write("## 📊 Summary\n\n")
            f.write(f"- **Total Transactions**: {summary['total_transactions']:,}\n")
            f.write(f"- **Total Withdrawals**: ₹{summary['total_withdrawals']:,.2f}\n")
            f.write(f"- **Total Deposits**: ₹{summary['total_deposits']:,.2f}\n")
            f.write(f"- **Net Amount**: ₹{summary['net_amount']:,.2f}\n")
            f.write(f"- **Date Range**: {summary['date_range']['start']} to {summary['date_range']['end']}\n\n")
            
            f.write("## 📋 Category Breakdown\n\n")
            f.write("| Category | Transactions | Withdrawals | Deposits | Net Amount |\n")
            f.write("|----------|-------------|-------------|----------|------------|\n")
            
            for category, data in summary['category_breakdown'].iterrows():
                f.write(f"| {category} | {data['Date']} | ₹{data['Withdrawal_Numeric']:,.2f} | "
                       f"₹{data['Deposit_Numeric']:,.2f} | ₹{data['Net_Amount']:,.2f} |\n")
        
        logger.info(f"Generated markdown report: {report_file}")
    
    def convert(self):
        """Main conversion method."""
        try:
            logger.info("Starting HDFC PDF to CSV conversion...")
            
            # Extract transactions
            transactions, page_stats = self.extract_transactions()
            
            if not transactions:
                logger.error("No transactions found in the PDF!")
                return {
                    'success': False,
                    'error': 'No transactions found in the PDF'
                }
            
            # Categorize transactions
            categorized_transactions = self.categorize_transactions(transactions)
            
            # Generate summary
            summary = self.generate_summary(categorized_transactions)
            
            # Save results
            output_files = self.save_results(categorized_transactions, page_stats, summary)
            
            logger.info("Conversion completed successfully!")
            logger.info(f"Output files saved in: {self.output_dir}")
            
            return {
                'success': True,
                'csv_file': str(output_files['transactions_file']),
                'excel_file': str(output_files['excel_file']),
                'summary_file': str(output_files['summary_file']),
                'pages_processed': len(page_stats)
            }
            
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """Main entry point for command line usage."""
    parser = argparse.ArgumentParser(
        description="Convert HDFC Bank PDF statements to CSV format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hdfc_converter.py statement.pdf
  python hdfc_converter.py statement.pdf --output-dir ./results
  python hdfc_converter.py /path/to/statements/hdfc_2024.pdf --verbose
        """
    )
    
    parser.add_argument(
        'pdf_path',
        help='Path to the HDFC PDF statement file'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        default='results',
        help='Output directory for CSV files (default: results)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Use the provided PDF path
    pdf_path = args.pdf_path
    
    try:
        # Create converter and run conversion
        converter = HDFCConverter(pdf_path, args.output_dir)
        success = converter.convert()
        
        if success:
            logger.info("✅ Conversion completed successfully!")
            sys.exit(0)
        else:
            logger.error("❌ Conversion failed!")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

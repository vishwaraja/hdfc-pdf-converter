#!/usr/bin/env python3
"""
Example usage of HDFC PDF to CSV Converter

This script demonstrates how to use the converter programmatically
and shows various configuration options.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hdfc_converter import HDFCConverter


def example_basic_usage():
    """Basic usage example."""
    print("=== Basic Usage Example ===")
    
    # Initialize converter with a PDF file
    pdf_path = "sample_statement.pdf"  # Replace with your PDF path
    output_dir = "example_output"
    
    try:
        converter = HDFCConverter(pdf_path, output_dir)
        success = converter.convert()
        
        if success:
            print("✅ Conversion completed successfully!")
            print(f"Check the '{output_dir}' directory for output files.")
        else:
            print("❌ Conversion failed!")
            
    except FileNotFoundError:
        print(f"❌ PDF file not found: {pdf_path}")
        print("Please provide a valid HDFC Bank PDF statement.")
        print("Usage: python src/hdfc_converter.py your_statement.pdf")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_with_custom_settings():
    """Example with custom settings and error handling."""
    print("\n=== Custom Settings Example ===")
    
    pdf_path = "hdfc_bank_statement_unprotected.pdf"
    output_dir = "custom_output"
    
    try:
        # Create converter
        converter = HDFCConverter(pdf_path, output_dir)
        
        # Extract transactions
        print("Extracting transactions...")
        transactions, page_stats = converter.extract_transactions()
        
        if not transactions:
            print("❌ No transactions found!")
            return
        
        print(f"✅ Found {len(transactions)} transactions")
        
        # Categorize transactions
        print("Categorizing transactions...")
        categorized = converter.categorize_transactions(transactions)
        
        # Generate summary
        print("Generating summary...")
        summary = converter.generate_summary(categorized)
        
        # Print summary
        print(f"\n📊 Summary:")
        print(f"Total Transactions: {summary['total_transactions']:,}")
        print(f"Total Withdrawals: ₹{summary['total_withdrawals']:,.2f}")
        print(f"Total Deposits: ₹{summary['total_deposits']:,.2f}")
        print(f"Net Amount: ₹{summary['net_amount']:,.2f}")
        
        # Save results
        print("Saving results...")
        output_files = converter.save_results(categorized, page_stats, summary)
        
        print(f"✅ Files saved:")
        for file_type, file_path in output_files.items():
            print(f"  - {file_type}: {file_path}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_analyze_categories():
    """Example showing how to analyze transaction categories."""
    print("\n=== Category Analysis Example ===")
    
    # This would typically be done after conversion
    # Here we show how to analyze the results
    
    try:
        import pandas as pd
        
        # Load the generated CSV (assuming it exists)
        csv_file = "output/hdfc_transactions_*.csv"  # Replace with actual file
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            
            # Analyze categories
            category_analysis = df.groupby('Category').agg({
                'Withdrawal_Amount': 'sum',
                'Deposit_Amount': 'sum',
                'Date': 'count'
            }).round(2)
            
            print("📋 Category Analysis:")
            print(category_analysis)
            
        else:
            print("❌ No CSV file found. Run conversion first.")
            
    except Exception as e:
        print(f"❌ Error analyzing categories: {e}")


def example_batch_processing():
    """Example showing how to process multiple PDF files."""
    print("\n=== Batch Processing Example ===")
    
    # List of PDF files to process
    pdf_files = [
        "statement_2023.pdf",
        "statement_2024.pdf",
        "statement_2025.pdf"
    ]
    
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            print(f"Processing {pdf_file}...")
            
            try:
                output_dir = f"output_{pdf_file.replace('.pdf', '')}"
                converter = HDFCConverter(pdf_file, output_dir)
                success = converter.convert()
                
                if success:
                    print(f"✅ {pdf_file} processed successfully!")
                else:
                    print(f"❌ Failed to process {pdf_file}")
                    
            except Exception as e:
                print(f"❌ Error processing {pdf_file}: {e}")
        else:
            print(f"⚠️  File not found: {pdf_file}")


if __name__ == "__main__":
    print("HDFC PDF to CSV Converter - Example Usage")
    print("=" * 50)
    
    # Run examples
    example_basic_usage()
    example_with_custom_settings()
    example_analyze_categories()
    example_batch_processing()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nTo use the converter:")
    print("1. Run: python src/hdfc_converter.py your_statement.pdf")
    print("2. Check the 'results' directory for results")
    print("3. Use --help for more options: python src/hdfc_converter.py --help")

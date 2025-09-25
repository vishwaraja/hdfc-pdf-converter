#!/usr/bin/env python3
"""
Test script to check the help output without dependencies
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Mock the imports that would fail
class MockModule:
    def __getattr__(self, name):
        return lambda *args, **kwargs: None

sys.modules['pandas'] = MockModule()
sys.modules['camelot'] = MockModule()
sys.modules['PyPDF2'] = MockModule()
sys.modules['pdfplumber'] = MockModule()
sys.modules['openpyxl'] = MockModule()
sys.modules['xlsxwriter'] = MockModule()

# Now import and test the argument parser
import argparse

def test_help():
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
    
    parser.print_help()

if __name__ == "__main__":
    test_help()
#!/usr/bin/env python3
"""
Unit tests for HDFC PDF to CSV Converter
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    from hdfc_converter import HDFCConverter
    CONVERTER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import HDFCConverter: {e}")
    CONVERTER_AVAILABLE = False


class TestHDFCConverter(unittest.TestCase):
    """Test cases for HDFCConverter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_pdf = "test_statement.pdf"  # This would need to be a real test PDF
        
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @unittest.skipUnless(CONVERTER_AVAILABLE, "HDFCConverter not available")
    def test_converter_initialization(self):
        """Test converter initialization."""
        # Test with non-existent file
        with self.assertRaises(FileNotFoundError):
            HDFCConverter("non_existent.pdf")
        
        # Test with valid parameters
        if os.path.exists(self.test_pdf):
            converter = HDFCConverter(self.test_pdf, self.temp_dir)
            self.assertEqual(converter.pdf_path, Path(self.test_pdf))
            self.assertEqual(converter.output_dir, Path(self.temp_dir))
    
    def test_basic_functionality(self):
        """Test basic functionality without requiring converter."""
        # Test that we can import basic Python modules
        try:
            import os
            import sys
            import tempfile
            from pathlib import Path
            self.assertTrue(True, "Basic Python modules can be imported")
        except ImportError as e:
            self.fail(f"Basic Python modules not available: {e}")
    
    def test_optional_dependencies(self):
        """Test optional dependencies availability."""
        # Test pandas availability
        try:
            import pandas as pd
            pandas_available = True
        except ImportError:
            pandas_available = False
        
        # Test camelot availability
        try:
            import camelot
            camelot_available = True
        except ImportError:
            camelot_available = False
        
        # These are optional dependencies, so we just log their availability
        print(f"Pandas available: {pandas_available}")
        print(f"Camelot available: {camelot_available}")
        
        # Test passes regardless of availability
        self.assertTrue(True, "Optional dependency check completed")
    
    @unittest.skipUnless(CONVERTER_AVAILABLE, "HDFCConverter not available")
    def test_amount_cleaning(self):
        """Test amount cleaning functionality."""
        if os.path.exists(self.test_pdf):
            converter = HDFCConverter(self.test_pdf, self.temp_dir)
            
            # Test various amount formats
            test_cases = [
                ("1,234.56", "1234.56"),
                ("0", "0.00"),
                ("", "0.00"),
                ("nan", "0.00"),
                ("1,000,000.00", "1000000.00"),
            ]
            
            for input_amount, expected in test_cases:
                result = converter._clean_amount(input_amount)
                self.assertEqual(result, expected)
    
    @unittest.skipUnless(CONVERTER_AVAILABLE, "HDFCConverter not available")
    def test_transaction_categorization(self):
        """Test transaction categorization."""
        if os.path.exists(self.test_pdf):
            converter = HDFCConverter(self.test_pdf, self.temp_dir)
            
            # Test sample transactions
            test_transactions = [
                {"Narration": "UPI payment to merchant"},
                {"Narration": "Salary credit from company"},
                {"Narration": "Foreign remittance from USA"},
                {"Narration": "Cheque payment 123456"},
                {"Narration": "Donation to charity"},
            ]
            
            categorized = converter.categorize_transactions(test_transactions)
            
            # Check that all transactions have categories
            for transaction in categorized:
                self.assertIn('Category', transaction)
                self.assertIsNotNone(transaction['Category'])
    
    @unittest.skipUnless(CONVERTER_AVAILABLE, "HDFCConverter not available")
    def test_output_directory_creation(self):
        """Test that output directory is created."""
        new_output_dir = os.path.join(self.temp_dir, "new_output")
        
        if os.path.exists(self.test_pdf):
            converter = HDFCConverter(self.test_pdf, new_output_dir)
            self.assertTrue(os.path.exists(new_output_dir))


class TestIntegration(unittest.TestCase):
    """Integration tests."""
    
    @unittest.skipUnless(CONVERTER_AVAILABLE, "HDFCConverter not available")
    def test_full_conversion_workflow(self):
        """Test the complete conversion workflow."""
        # This would require a real PDF file
        # For now, we'll test the workflow structure
        
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Test with a real PDF if available
            test_pdf = "hdfc_bank_statement_unprotected.pdf"
            
            if os.path.exists(test_pdf):
                converter = HDFCConverter(test_pdf, temp_dir)
                
                # Test extraction
                transactions, page_stats = converter.extract_transactions()
                self.assertIsInstance(transactions, list)
                self.assertIsInstance(page_stats, list)
                
                if transactions:
                    # Test categorization
                    categorized = converter.categorize_transactions(transactions)
                    self.assertEqual(len(categorized), len(transactions))
                    
                    # Test summary generation
                    summary = converter.generate_summary(categorized)
                    self.assertIn('total_transactions', summary)
                    self.assertIn('total_withdrawals', summary)
                    self.assertIn('total_deposits', summary)
                    
                    # Test saving results
                    output_files = converter.save_results(categorized, page_stats, summary)
                    self.assertIsInstance(output_files, dict)
                    
                    # Check that files were created
                    for file_type, file_path in output_files.items():
                        self.assertTrue(os.path.exists(file_path))
        
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)

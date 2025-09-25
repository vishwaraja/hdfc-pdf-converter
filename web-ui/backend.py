#!/usr/bin/env python3
"""
Backend API for HDFC PDF to CSV Converter Web UI
Handles actual PDF processing and CSV generation
"""

import os
import sys
import json
import tempfile
import subprocess
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import pandas as pd
from datetime import datetime

# Add the src directory to the path so we can import our converter
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from hdfc_converter import HDFCConverter
    print("Successfully imported HDFCConverter")
except ImportError as e:
    print(f"Warning: Could not import HDFCConverter: {e}")
    HDFCConverter = None
except Exception as e:
    print(f"Error importing HDFCConverter: {e}")
    HDFCConverter = None

# Fallback to simple converter
try:
    from simple_converter import SimpleHDFCConverter
    print("Successfully imported SimpleHDFCConverter as fallback")
except ImportError as e:
    print(f"Warning: Could not import SimpleHDFCConverter: {e}")
    SimpleHDFCConverter = None
except Exception as e:
    print(f"Error importing SimpleHDFCConverter: {e}")
    SimpleHDFCConverter = None

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/styles.css')
def styles():
    return send_file('styles.css')

@app.route('/script.js')
def script():
    return send_file('script.js')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        temp_pdf_path = os.path.join(temp_dir, filename)
        file.save(temp_pdf_path)
        
        # Process the PDF using our converter
        if HDFCConverter is not None:
            # Use full converter if available
            print(f"Using full HDFCConverter for: {temp_pdf_path}")
            try:
                converter = HDFCConverter(temp_pdf_path, temp_dir)
                result = converter.convert()
                print(f"Full converter result: {result}")
            except Exception as e:
                print(f"Full converter failed: {e}")
                # Fall back to simple converter
                if SimpleHDFCConverter is not None:
                    print(f"Falling back to SimpleHDFCConverter")
                    converter = SimpleHDFCConverter(temp_pdf_path, temp_dir)
                    result = converter.convert()
                    print(f"Simple converter result: {result}")
                else:
                    return jsonify({'error': f'PDF processing failed: {str(e)}'}), 500
        elif SimpleHDFCConverter is not None:
            # Use simple converter as fallback
            print(f"Using SimpleHDFCConverter fallback for: {temp_pdf_path}")
            converter = SimpleHDFCConverter(temp_pdf_path, temp_dir)
            result = converter.convert()
            print(f"Simple converter result: {result}")
        else:
            return jsonify({'error': 'PDF processing not available. Please use the command line version.'}), 500
        
        if result['success']:
            # Read the generated CSV to get transaction count
            csv_path = result['csv_file']
            df = pd.read_csv(csv_path)
            
            # Get summary statistics
            stats = {
                'transaction_count': len(df),
                'page_count': result.get('pages_processed', 0),
                'category_count': df['Category'].nunique() if 'Category' in df.columns else 0,
                'date_range': {
                    'start': df['Date'].min() if 'Date' in df.columns else 'N/A',
                    'end': df['Date'].max() if 'Date' in df.columns else 'N/A'
                },
                'total_withdrawals': df['Withdrawal_Amount'].sum() if 'Withdrawal_Amount' in df.columns else 0,
                'total_deposits': df['Deposit_Amount'].sum() if 'Deposit_Amount' in df.columns else 0
            }
            
            # Store file paths for download
            session_data = {
                'csv_file': csv_path,
                'excel_file': result.get('excel_file'),
                'summary_file': result.get('summary_file'),
                'stats': stats,
                'temp_dir': temp_dir
            }
            
            return jsonify({
                'success': True,
                'message': 'PDF processed successfully',
                'stats': stats,
                'session_id': os.path.basename(temp_dir)  # Use temp dir name as session ID
            })
        else:
            return jsonify({'error': result.get('error', 'PDF processing failed')}), 500
            
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/download/<session_id>/<file_type>')
def download_file(session_id, file_type):
    try:
        # Reconstruct temp directory path
        temp_dir = os.path.join(tempfile.gettempdir(), session_id)
        
        if not os.path.exists(temp_dir):
            return jsonify({'error': 'Session expired or invalid'}), 404
        
        file_path = None
        filename = None
        mime_type = None
        
        if file_type == 'csv':
            # Find CSV file in temp directory
            for file in os.listdir(temp_dir):
                if file.endswith('.csv') and 'transactions' in file.lower():
                    file_path = os.path.join(temp_dir, file)
                    filename = file
                    mime_type = 'text/csv'
                    break
        elif file_type == 'excel':
            # Find Excel file in temp directory
            for file in os.listdir(temp_dir):
                if file.endswith('.xlsx'):
                    file_path = os.path.join(temp_dir, file)
                    filename = file
                    mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    break
        elif file_type == 'summary':
            # Find summary file in temp directory
            for file in os.listdir(temp_dir):
                if file.endswith('.md') and 'summary' in file.lower():
                    file_path = os.path.join(temp_dir, file)
                    filename = file
                    mime_type = 'text/markdown'
                    break
        
        if file_path and os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename, mimetype=mime_type)
        else:
            return jsonify({'error': f'{file_type} file not found'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'converter_available': HDFCConverter is not None or SimpleHDFCConverter is not None,
        'full_converter_available': HDFCConverter is not None,
        'simple_converter_available': SimpleHDFCConverter is not None
    })

@app.route('/debug')
def debug():
    import_info = {
        'converter_available': HDFCConverter is not None,
        'pandas_available': False,
        'camelot_available': False,
        'error_details': None
    }
    
    try:
        import pandas as pd
        import_info['pandas_available'] = True
    except Exception as e:
        import_info['error_details'] = f"Pandas import failed: {e}"
    
    try:
        import camelot
        import_info['camelot_available'] = True
    except Exception as e:
        if import_info['error_details']:
            import_info['error_details'] += f"; Camelot import failed: {e}"
        else:
            import_info['error_details'] = f"Camelot import failed: {e}"
    
    return jsonify(import_info)

@app.route('/')
def root():
    return jsonify({'message': 'HDFC PDF Converter API is running', 'status': 'healthy'})

if __name__ == '__main__':
    print("Starting HDFC PDF Converter Web Backend...")
    print(f"HDFCConverter available: {HDFCConverter is not None}")
    
    # Get port from environment (Railway sets this)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(debug=debug, host='0.0.0.0', port=port)

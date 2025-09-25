#!/usr/bin/env python3
"""
Simple Flask backend for Railway deployment
"""

from flask import Flask, request, jsonify
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

@app.route('/')
def root():
    return jsonify({
        'message': 'HDFC PDF Converter API is running',
        'status': 'healthy',
        'version': '1.0.1',
        'deployment': 'fixed'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'converter_available': False,  # Simplified for Railway
        'message': 'Basic API is running'
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        # For now, return a mock response
        return jsonify({
            'success': True,
            'message': 'PDF received successfully (demo mode)',
            'stats': {
                'transaction_count': 3602,
                'page_count': 165,
                'category_count': 22,
                'date_range': {
                    'start': '15/07/2020',
                    'end': '12/08/2025'
                },
                'total_withdrawals': 57764839.23,
                'total_deposits': 78842318.06
            },
            'session_id': 'demo_session_123'
        })
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/download/<session_id>/<file_type>')
def download_file(session_id, file_type):
    # Return a simple demo response
    return jsonify({
        'message': 'Demo mode - file download not available',
        'session_id': session_id,
        'file_type': file_type
    })

if __name__ == '__main__':
    print("Starting Simple HDFC PDF Converter Web Backend...")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

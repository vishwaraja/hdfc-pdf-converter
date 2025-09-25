#!/usr/bin/env python3
"""
Start the HDFC PDF Converter Web Server
"""

import os
import sys
import subprocess

def main():
    print("🚀 Starting HDFC PDF Converter Web Server...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('backend.py'):
        print("❌ Error: backend.py not found. Please run this from the web-ui directory.")
        sys.exit(1)
    
    # Check if Flask is installed
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask not found. Installing requirements...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
    # Check if our converter is available
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
        from hdfc_converter import HDFCConverter
        print("✅ HDFC Converter is available")
    except ImportError:
        print("⚠️  Warning: HDFC Converter not found. Web UI will show demo data only.")
        print("   Make sure the src/hdfc_converter.py file exists in the parent directory.")
    
    print("\n🌐 Starting web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the Flask server
    os.system('python backend.py')

if __name__ == '__main__':
    main()

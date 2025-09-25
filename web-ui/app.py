#!/usr/bin/env python3
"""
Flask app entry point for Railway deployment
"""

import os
import sys

# Try to import the full backend, fallback to simple backend
try:
    # Add the src directory to the path so we can import our converter
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
    from backend import app
    print("Using full backend with PDF processing")
except ImportError as e:
    print(f"Full backend not available: {e}")
    print("Using simple backend for Railway deployment")
    from simple_backend import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

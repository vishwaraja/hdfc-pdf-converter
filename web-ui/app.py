#!/usr/bin/env python3
"""
Flask app entry point for Railway deployment
"""

import os
import sys

# Add the src directory to the path so we can import our converter
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from backend import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

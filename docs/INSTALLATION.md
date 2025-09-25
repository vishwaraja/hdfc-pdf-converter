# Installation Guide

This guide provides detailed installation instructions for the HDFC PDF to CSV Converter.

## Prerequisites

- **Python 3.8 or higher** - The converter requires Python 3.8 or newer
- **Operating System** - Works on Windows, macOS, and Linux
- **Memory** - At least 2GB RAM recommended for large PDF files
- **Disk Space** - At least 100MB free space for dependencies

## Installation Methods

### Method 1: Clone and Install (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/vishwarajapathi/hdfc-pdf-converter.git
   cd hdfc-pdf-converter
   ```

2. **Create a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package**
   ```bash
   pip install -e .
   ```

### Method 2: Direct Installation

```bash
pip install hdfc-pdf-converter
```

### Method 3: Development Installation

```bash
# Clone repository
git clone https://github.com/vishwarajapathi/hdfc-pdf-converter.git
cd hdfc-pdf-converter

# Install in development mode
pip install -e .[dev]
```

## System-Specific Instructions

### Windows

1. **Install Python**
   - Download Python from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Install Git** (if not already installed)
   - Download from [git-scm.com](https://git-scm.com/download/win)

3. **Open Command Prompt or PowerShell**
   ```cmd
   # Navigate to your desired directory
   cd C:\Users\YourName\Documents
   
   # Clone and install
   git clone https://github.com/vishwarajapathi/hdfc-pdf-converter.git
   cd hdfc-pdf-converter
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .
   ```

### macOS

1. **Install Python** (if not already installed)
   ```bash
   # Using Homebrew
   brew install python
   
   # Or download from python.org
   ```

2. **Install Git** (if not already installed)
   ```bash
   # Using Homebrew
   brew install git
   ```

3. **Install the converter**
   ```bash
   git clone https://github.com/vishwarajapathi/hdfc-pdf-converter.git
   cd hdfc-pdf-converter
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -e .
   ```

### Linux (Ubuntu/Debian)

1. **Install Python and pip**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv git
   ```

2. **Install the converter**
   ```bash
   git clone https://github.com/vishwarajapathi/hdfc-pdf-converter.git
   cd hdfc-pdf-converter
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -e .
   ```

## Dependencies

The converter requires the following Python packages:

### Core Dependencies
- **camelot-py[cv]** - PDF table extraction
- **pandas** - Data manipulation
- **numpy** - Numerical operations
- **PyPDF2** - PDF processing
- **pdfplumber** - PDF text extraction

### Optional Dependencies
- **openpyxl** - Excel file support
- **xlsxwriter** - Excel writing
- **opencv-python** - Image processing
- **Pillow** - Image handling

### Development Dependencies
- **pytest** - Testing framework
- **black** - Code formatting
- **flake8** - Code linting

## Verification

After installation, verify that everything works:

```bash
# Check if the converter is installed
python -c "import hdfc_converter; print('Installation successful!')"

# Run a test conversion (if you have a sample PDF)
python src/hdfc_converter.py --help
```

## Troubleshooting

### Common Issues

1. **"python: command not found"**
   - Make sure Python is installed and added to PATH
   - Try using `python3` instead of `python`

2. **"pip: command not found"**
   - Install pip: `python -m ensurepip --upgrade`
   - Or download get-pip.py and run it

3. **"Permission denied" errors**
   - Use virtual environment: `python -m venv venv`
   - Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)

4. **"Module not found" errors**
   - Make sure you're in the correct directory
   - Check that all dependencies are installed: `pip install -r requirements.txt`

5. **Camelot installation issues**
   - On Windows: Install Visual C++ Build Tools
   - On Linux: Install system dependencies: `sudo apt-get install python3-tk ghostscript`
   - On macOS: Install Ghostscript: `brew install ghostscript`

### Getting Help

If you encounter issues:

1. Check the [troubleshooting section](#troubleshooting)
2. Open an [issue](https://github.com/vishwarajapathi/hdfc-pdf-converter/issues)
3. Check the [FAQ](FAQ.md)

## Uninstallation

To uninstall the converter:

```bash
# If installed with pip
pip uninstall hdfc-pdf-converter

# If installed in development mode
pip uninstall -e .

# Remove the cloned repository
rm -rf hdfc-pdf-converter
```

## Updating

To update to the latest version:

```bash
# Navigate to the project directory
cd hdfc-pdf-converter

# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Reinstall the package
pip install -e .
```

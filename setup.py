#!/usr/bin/env python3
"""
Setup script for HDFC PDF to CSV Converter
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "HDFC Bank PDF Statement to CSV Converter"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="hdfc-pdf-converter",
    version="1.0.0",
    author="Vishwaraja Pathi",
    author_email="vishwaraja.pathi@adiyogitech.com",
    description="A robust tool to extract transaction data from HDFC Bank PDF statements and convert them to CSV format",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/vishwaraja/hdfc-pdf-converter",
    project_urls={
        "Bug Tracker": "https://github.com/vishwaraja/hdfc-pdf-converter/issues",
        "Documentation": "https://github.com/vishwaraja/hdfc-pdf-converter#readme",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial",
        "Topic :: Text Processing :: Markup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    py_modules=["hdfc_converter"],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "hdfc-converter=hdfc_converter:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords="hdfc, bank, pdf, csv, converter, statement, transactions, finance",
    zip_safe=False,
)

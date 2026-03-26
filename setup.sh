#!/bin/bash
# Setup script for Data Mining Assignment 1
# Creates virtual environment and installs dependencies

echo "========================================"
echo "Data Mining Assignment 1 - Setup"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from python.org"
    exit 1
fi

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi
echo "     Virtual environment created: venv/"

echo ""
echo "[2/4] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo "     Virtual environment activated"

echo ""
echo "[3/4] Installing dependencies..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "     Dependencies installed successfully"

echo ""
echo "[4/4] Setting up Task 1 database..."
cd task1
python database.py
cd ..
if [ $? -ne 0 ]; then
    echo "WARNING: Task 1 database setup failed"
else
    echo "     Task 1 database created"
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: streamlit run app.py"
echo ""
echo "To deactivate virtual environment: deactivate"
echo ""

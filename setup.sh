#!/bin/bash
# Setup and Installation Script for ABSA Pipeline

echo "========================================"
echo "ABSA Pipeline Setup and Installation"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python --version
if [ $? -ne 0 ]; then
    echo "✗ Python is not installed or not in PATH"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✓ Installation Successful!"
    echo "========================================"
    echo ""
    echo "Next steps:"
    echo "1. Verify installation: python test_pipeline.py"
    echo "2. Try quick start: python quick_start.py"
    echo "3. Run full demo: python demo.py"
    echo "4. See documentation: cat PIPELINE_README.md"
    echo ""
else
    echo ""
    echo "✗ Installation failed"
    exit 1
fi

#!/bin/bash
# This script automates the setup of the local development environment for bash shells
# (including macOS, Linux, and Git Bash on Windows).

echo "--- Checking for Python ---"
# Find a valid python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "Error: Python is not installed or not available in your PATH."
    echo "Please install Python 3 and ensure it's added to your PATH."
    exit 1
fi
echo "Using '$PYTHON_CMD' to create virtual environment."

echo "--- Setting up Python virtual environment ---"
$PYTHON_CMD -m venv venv

# Activate the virtual environment (handling different paths)
if [ -f "venv/bin/activate" ]; then
  # For macOS/Linux
  source venv/bin/activate
  ACTIVATION_PATH="source venv/bin/activate"
elif [ -f "venv/Scripts/activate" ]; then
  # For Git Bash on Windows
  source venv/Scripts/activate
  ACTIVATION_PATH="source venv/Scripts/activate"
else
  echo "Error: Could not find the virtual environment activation script after creation."
  exit 1
fi

echo -e "\n--- Installing required Python libraries ---"
pip install -r requirements.txt


echo -e "\n--- Running the ETL script ---"
# The Python script will handle database creation automatically.
$PYTHON_CMD etl.py


echo -e "\n--- Setup Complete ---"
echo "The virtual environment is active, libraries are installed, and the ETL script has been run."
echo "To run the script again in the future, just activate the environment and run the python script:"
echo "  $ACTIVATION_PATH"
echo "  $PYTHON_CMD etl.py"

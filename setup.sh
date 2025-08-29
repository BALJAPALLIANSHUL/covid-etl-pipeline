#!/bin/bash
# This script automates the setup of the local development environment.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Setting up Python virtual environment --- "
# Create a virtual environment named 'venv' if it doesn't exist
[ -d "venv" ] || python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

echo "\n--- Installing required Python libraries ---"
pip install -r requirements.txt

echo "\n--- Running the ETL script ---"
# The Python script will now handle database creation automatically.
# It will also provide instructions if the database user needs to be created.
python etl.py

# --- Instructions for the user ---
echo "\n--- Setup Complete ---"
echo "The virtual environment is active, libraries are installed, and the ETL script has been run."
echo "To run the script again in the future, just activate the environment and run the python script:"
echo "  source venv/bin/activate"
echo "  python etl.py"

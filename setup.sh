#!/bin/bash
# This script automates the setup of the local development environment for bash shells
# (including macOS, Linux, and Git Bash on Windows).

echo "--- Setting up Python virtual environment ---"
python3 -m venv venv

# Activate the virtual environment (handling different paths)
if [ -f "venv/bin/activate" ]; then
  # For macOS/Linux
  source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
  # For Git Bash on Windows
  source venv/Scripts/activate
else
  echo "Error: Could not find the virtual environment activation script."
  exit 1
fi

echo -e "\n--- Installing required Python libraries ---"
pip install -r requirements.txt

echo -e "\n--- Running the ETL script ---"
# The Python script will handle database creation automatically.
python3 etl.py

echo -e "\n--- Setup Complete ---"
echo "The virtual environment is active, libraries are installed, and the ETL script has been run."
echo "To run the script again in the future, just activate the environment and run the python script:"

# Provide the correct activation command for the detected OS
if [ -f "venv/bin/activate" ]; then
  echo "  source venv/bin/activate"
else
  echo "  source venv/Scripts/activate"
fi

echo "  python3 etl.py"

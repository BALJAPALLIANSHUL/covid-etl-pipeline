@echo off
REM This script automates the setup of the local development environment on Windows.

ECHO --- Setting up Python virtual environment --- 
REM Create a virtual environment named 'venv' if it doesn't exist
IF NOT EXIST venv ( python3 -m venv venv )

REM Activate the virtual environment
call .\venv\Scripts\activate

ECHO.\n--- Installing required Python libraries ---
pip install -r requirements.txt

ECHO.\n--- Running the ETL script ---
REM The Python script will now handle database creation automatically.
REM It will also provide instructions if the database user needs to be created.
python3 etl.py

ECHO.\n--- Setup Complete ---
ECHO The virtual environment is active, libraries are installed, and the ETL script has been run.
ECHO To run the script again in the future, just activate the environment and run the python script:
ECHO   .\venv\Scripts\activate
ECHO   python3 etl.py

@echo off
REM This script automates the setup of the local development environment on Windows.

ECHO --- Checking for Python ---
REM Use the 'py' launcher to ensure the correct Python version is used.
py -3 -V >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Python 3 is not installed or the 'py' launcher is not available.
    ECHO Please install Python 3 from python.org and ensure it's added to your PATH.
    EXIT /B 1
)
ECHO Using 'py -3' launcher.

ECHO --- Setting up Python virtual environment ---
REM Create a virtual environment named 'venv' if it doesn't exist
IF NOT EXIST venv ( py -3 -m venv venv )

REM Activate the virtual environment
call .\venv\Scripts\activate

ECHO.\n--- Installing required Python libraries ---
pip install -r requirements.txt

ECHO.\n--- Running the ETL script ---
REM The Python script will now handle database creation automatically.
py -3 etl.py

ECHO.\n--- Setup Complete ---
ECHO The virtual environment is active, libraries are installed, and the ETL script has been run.
ECHO To run the script again in the future, just activate the environment and run the python script:
ECHO   .\venv\Scripts\activate
ECHO   py -3 etl.py

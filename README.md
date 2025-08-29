# ETL Pipeline for US COVID-19 Data

This project contains a Python-based ETL (Extract, Transform, Load) pipeline that fetches daily COVID-19 data for the USA, processes it, and stores it in a local PostgreSQL database.

## Features

- **Extract**: Fetches historical COVID-19 data from the disease.sh API.
- **Transform**: Converts the data into a clean, structured format, calculating daily new cases and deaths.
- **Load**: Inserts the transformed data into a PostgreSQL database.
- **Incremental Updates**: On subsequent runs, the pipeline checks for the most recent data in the database and only loads newer records, preventing duplication.

## Local Setup

This guide will help you set up and run the project on your local machine.

### Prerequisites

- **Python 3**: You will need Python 3 installed on your system.
- **PostgreSQL**: You need a running PostgreSQL server.

### Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/BALJAPALLIANSHUL/covid-etl-pipeline.git
    cd covid-etl-pipeline
    ```

2.  **Run the Setup Script**:
    This script creates a Python virtual environment, installs dependencies, and sets up your local database credentials.

    - On **macOS or Linux**:
      ```bash
      bash setup.sh
      ```
    - On **Windows**:
      ```batch
      setup.bat
      ```

3.  **Activate the Virtual Environment**:
    - On **macOS or Linux**:
      ```bash
      source venv/bin/activate
      ```
    - On **Windows**:
      ```powershell
      .\venv\Scripts\Activate.ps1
      ```

### Running the ETL Pipeline

Once setup is complete, you can run the main ETL script:

```bash
python etl.py
```

## Project Structure

```
.gitignore          # Specifies files to be ignored by Git.
README.md           # This file.
etl.py              # The main ETL script.
requirements.txt    # Python dependencies.
setup.sh            # Setup script for macOS and Linux.
setup.bat           # Setup script for Windows.
```

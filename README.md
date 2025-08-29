# ETL Pipeline for US COVID-19 Data

This project contains a Python-based ETL (Extract, Transform, Load) pipeline that fetches daily COVID-19 data for the USA, processes it, and stores it in a local PostgreSQL database.

## Project Overview

### Problem Statement
The challenge is to reliably source, process, and store historical COVID-19 data for the United States. The data needs to be cleaned, transformed into a usable format, and stored in a database in a way that is both efficient and prevents data duplication on repeated runs. This automated process is essential for creating a reliable dataset for analysis, visualization, or monitoring dashboards.

### Solution
An automated ETL (Extract, Transform, Load) pipeline was developed in Python to solve this problem.
-   **Extract:** The pipeline connects to the public `disease.sh` API to fetch comprehensive historical COVID-19 case and death data for the USA.
-   **Transform:** Using the `pandas` library, the raw JSON data is transformed into a structured format. It calculates daily new cases and deaths from the cumulative totals, providing more valuable metrics for analysis.
-   **Load:** The transformed data is loaded into a PostgreSQL database. The pipeline includes an incremental loading strategy, where it first checks the latest record in the database and only inserts newer data, making the process highly efficient for daily updates.

### Key Achievements
-   **Fully Automated Pipeline:** A single script (`etl.py`) orchestrates the entire process, from data fetching to database loading.
-   **Incremental Updates:** The pipeline intelligently handles data updates, avoiding redundant data storage and reducing processing time on subsequent runs.
-   **Reproducible Setup:** The project includes setup scripts (`setup.sh` and `setup.bat`) that create an isolated Python environment and install all necessary dependencies, making it easy to run on different machines.
-   **Secure Credential Management:** Database credentials are managed securely using a `.env` file, which is kept out of version control thanks to a robust `.gitignore` file.

### Dataset Used
-   **Source:** [NovelCOVID API (disease.sh)](https://disease.sh/v3/covid-19/historical/usa?lastdays=all)
-   **Description:** The dataset provides historical, day-by-day cumulative counts of COVID-19 cases and deaths in the United States. The pipeline transforms this into daily new cases and deaths.
-   **Format:** The API returns data in JSON format.

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

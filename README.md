# COVID-19 ETL Pipeline

This project contains a Python-based ETL (Extract, Transform, Load) pipeline that fetches daily COVID-19 data for the USA from a public API, processes it, and loads it into a PostgreSQL database.

The project is configured to run in two ways:
1.  **In the Cloud**: Using the pre-configured Firebase Studio (IDX) environment.
2.  **On a Local Machine**: Using setup scripts for a seamless local development experience.

---

## Running the Project in Firebase Studio (IDX)

This environment is ready to go. The `.idx/dev.nix` file automatically handles all setup and execution:

1.  **PostgreSQL Service**: A managed PostgreSQL database is automatically started.
2.  **Database Creation**: The `covid_data` database is created on startup.
3.  **ETL Execution**: The `etl.py` script is automatically run every time the workspace starts, loading the latest data into the database.

When you open the project in the IDE, the entire pipeline will execute, and you will see the logs in the terminal, ending with a query that displays the 10 most recent days of data.

---

## Running the Project on a Local Machine

To run this project locally, you will need to have **Python 3** and **PostgreSQL** installed on your system.

### Step 1: Clone the Repository

First, clone this repository to your local machine:

```bash
git clone <your-repository-url>
cd <repository-folder>
```

### Step 2: One-Time Database User Setup

Before you run the project for the first time, you need to create the database user (role) that the script will use to connect. **This only needs to be done once.**

1.  Open `psql` or your preferred PostgreSQL client.
2.  Run the following SQL command:
    ```sql
    CREATE ROLE "user" WITH LOGIN PASSWORD 'password';
    ```
    *Note: These credentials match the `.env.example` file. If you plan to use different credentials, you will need to update them in the next step.*

### Step 3: Configure Your Environment

The repository includes an `.env.example` file that serves as a template for your local configuration.

1.  **Create a `.env` file** by copying the example file:

    ```bash
    # For macOS/Linux
    cp .env.example .env

    # For Windows
    copy .env.example .env
    ```

2.  **Edit the `.env` file.** The default credentials should work with the command from Step 2, but you can change them if your local PostgreSQL setup is different.

    *This `.env` file is listed in `.gitignore` and will **not** be committed to the repository, keeping your local credentials secure.*

### Step 4: Run the Automated Setup Script

The project includes setup scripts to automate the rest of the process. These scripts will create a Python virtual environment, install all dependencies, and run the ETL script.

*   **For macOS or Linux:**
    *   Make the script executable: `chmod +x setup.sh`
    *   Run the script: `./setup.sh`

*   **For Windows:**
    *   Simply run the batch file: `setup.bat`

The script will run the ETL process, and because of our `initialize_database` function in `etl.py`, it will automatically create the `covid_data` database for you on the first run.

---

## Project Structure

```
.gitignore          # Specifies files to be ignored by Git (e.g., venv, .env)
.idx/
  dev.nix           # Configuration for the cloud (IDX) environment
.env                # (Local Only) Your local database credentials. Ignored by Git.
.env.example        # A template for the .env file.
etl.py              # The main Python script for the ETL pipeline.
README.md           # This file.
requirements.txt    # A list of Python libraries for local setup.
setup.bat           # Windows script for automating local setup.
setup.sh            # macOS/Linux script for automating local setup.
```

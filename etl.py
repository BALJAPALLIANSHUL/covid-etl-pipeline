import os
import pandas as pd
import requests
import psycopg2
import logging
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection details from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "covid_data")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# API Endpoint
API_URL = "https://disease.sh/v3/covid-19/historical/usa?lastdays=all"

# --- DATABASE INITIALIZATION ---
def initialize_database():
    """Ensures the target database exists, creating it if necessary."""
    logging.info("Initializing database...")
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname='postgres'
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        if not cur.fetchone():
            logging.info(f"Database '{DB_NAME}' not found. Creating...")
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            logging.info(f"Database '{DB_NAME}' created.")
        else:
            logging.info(f"Database '{DB_NAME}' already exists.")
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        if f'role "{DB_USER}" does not exist' in str(e):
            logging.error(f"Database user '{DB_USER}' does not exist. Please create it first.")
            sys.exit(1)
        elif "connection refused" in str(e).lower():
            logging.error("Could not connect to PostgreSQL. Is the server running?")
            sys.exit(1)
        else:
            logging.error(f"Error during database initialization: {e}")
            sys.exit(1)

# --- INCREMENTAL LOAD HELPER ---
def get_most_recent_date(conn_string):
    """Queries the database to find the most recent date already stored."""
    try:
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT MAX(report_date) FROM covid_us_daily;")
                result = cur.fetchone()[0]
                if result:
                    logging.info(f"Most recent date in database is {result}.")
                    return result
    except (psycopg2.Error, TypeError):
        # Table might not exist on first run, which is expected.
        logging.info("No existing data found. Proceeding with a full load.")
        return None

# --- EXTRACT ---
def extract_data():
    """Fetches COVID-19 data from the API."""
    logging.info("Extracting data from API...")
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json().get('timeline', {})
    except requests.exceptions.RequestException as e:
        logging.error(f"API data extraction error: {e}")
        return None

# --- TRANSFORM ---
def transform_data(data, most_recent_date=None):
    """Transforms raw data into a clean DataFrame, filtering for new data only."""
    if not data or not data.get('cases'):
        logging.warning("No data to transform.")
        return None
    
    logging.info("Transforming data...")
    df = pd.DataFrame(data['cases'].items(), columns=['date', 'total_cases'])
    df_deaths = pd.DataFrame(data['deaths'].items(), columns=['date', 'total_deaths'])
    df = pd.merge(df, df_deaths, on='date')
    
    df['report_date'] = pd.to_datetime(df['date'], format='%m/%d/%y')
    df.sort_values(by='report_date', inplace=True)
    
    df['new_cases'] = df['total_cases'].diff().fillna(0).astype(int)
    df['new_deaths'] = df['total_deaths'].diff().fillna(0).astype(int)
    
    # Filter for new data only
    if most_recent_date:
        df = df[df['report_date'] > most_recent_date]
        logging.info(f"Found {len(df)} new records to load.")

    df = df[['report_date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']]
    return df

# --- LOAD ---
def load_data(df):
    """Loads the DataFrame into the PostgreSQL database."""
    if df is None or df.empty:
        logging.warning("No new data to load.")
        return

    conn_string = f"host='{DB_HOST}' port='{DB_PORT}' dbname='{DB_NAME}' user='{DB_USER}' password='{DB_PASSWORD}'"
    logging.info(f"Loading {len(df)} records into '{DB_NAME}'...")
    
    try:
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS covid_us_daily (
                        report_date DATE PRIMARY KEY, total_cases BIGINT, new_cases INTEGER,
                        total_deaths BIGINT, new_deaths INTEGER
                    );
                """)
                
                for _, row in df.iterrows():
                    cur.execute("""
                        INSERT INTO covid_us_daily (report_date, total_cases, new_cases, total_deaths, new_deaths)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (report_date) DO UPDATE SET
                            total_cases = EXCLUDED.total_cases, new_cases = EXCLUDED.new_cases,
                            total_deaths = EXCLUDED.total_deaths, new_deaths = EXCLUDED.new_deaths;
                    """, tuple(row))
        logging.info("Data loaded successfully.")
    except psycopg2.Error as e:
        logging.error(f"Database load error: {e}")
        sys.exit(1)

# --- ETL JOB ---
def etl_job():
    """The main ETL job function orchestrating the entire process."""
    logging.info("Starting ETL job...")
    conn_string = f"host='{DB_HOST}' port='{DB_PORT}' dbname='{DB_NAME}' user='{DB_USER}' password='{DB_PASSWORD}'"

    most_recent_date = get_most_recent_date(conn_string)
    raw_data = extract_data()
    transformed_data = transform_data(raw_data, most_recent_date)
    load_data(transformed_data)
    logging.info("ETL job finished.")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    initialize_database()
    etl_job()

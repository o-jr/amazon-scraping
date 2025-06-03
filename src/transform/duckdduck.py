import os
import json
import pandas as pd
import duckdb
import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    "file_path": "C:/Users/W4rne4/git/ml-scraping/data/data5.json",
    "duckdb_path": "C:/Users/W4rne4/git/ml-scraping/data/duckdb2.duckdb",
    "source_label": "amzn/oculos-masculino"
}

def load_json_data(file_path: str) -> list:
    logger.info(f"Loading JSON data from {file_path}")
    
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read()
        json_str = raw_data.decode('utf-8', errors='replace')
        return json.loads(json_str)
    except Exception as e:
        logger.error(f"Error reading or decoding JSON: {e}")
        raise


def save_cleaned_json(data: list, file_path: str) -> None:
    logger.info(f"Saving cleaned JSON to {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning(f"Failed to save cleaned JSON: {e}")


def create_dataframe(data: list) -> pd.DataFrame:
    logger.info("Creating DataFrame from JSON data")
    df = pd.DataFrame(data)

    # Add metadata columns
    df['Source'] = CONFIG["source_label"]
    df['Created_at'] = datetime.datetime.now()

    # Data cleaning
    df = df[df['brand'].notnull() & df['price'].notnull()]
    df['brand'] = df['brand'].replace({'Generic': 'Genérico', 'ROCK BROS': 'ROCKBROS'})
    df['price'] = df['price'].fillna(0).astype(float)
    df['rating'] = df['rating'].fillna(0).astype(float)
    df['title'] = df['title'].str.strip()

    return df


def save_to_duckdb(df: pd.DataFrame, db_path: str) -> None:
    logger.info(f"Saving data to DuckDB at {db_path}")

    try:
        conn = duckdb.connect(db_path)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS ml_items (
                brand VARCHAR,
                price FLOAT,
                rating FLOAT,
                title VARCHAR,
                page INTEGER,
                Source VARCHAR,
                Created_at TIMESTAMP
            )
        """)

        conn.register('ml_items_temp', df)
        conn.execute("INSERT INTO ml_items SELECT * FROM ml_items_temp")

        conn.close()
        logger.info("Data successfully saved to DuckDB.")
    except Exception as e:
        logger.error(f"Error saving to DuckDB: {e}")
        raise


def main():#Orchestrate the workflow.
    try:
        data = load_json_data(CONFIG["file_path"])
        save_cleaned_json(data, CONFIG["file_path"])
        df = create_dataframe(data)
        save_to_duckdb(df, CONFIG["duckdb_path"])
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()

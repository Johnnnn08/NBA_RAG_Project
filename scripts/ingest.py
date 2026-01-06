import psycopg2
from psycopg2.extras import execute_values
import pandas as pd

DB_CONFIG = {
    "dbname": "postgres",
    "user": "john",
    "password": "",
    "host": "localhost",
    "port": "5432"
}

def ingest_data():
    try:
        csv_path = "../data/cleaned_player_statistics.csv"
        df = pd.read_csv(csv_path)
        
        data_to_insert = df[['gameDateTimeEst', 'matchup', 'name', 'gameSummary', 'searchText']].values.tolist()

        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Batch Insert
        insert_query = """
            INSERT INTO nba_game_logs (game_date, matchup, player_name, stats_summary, search_text)
            VALUES %s
        """
        
        print(f"Starting ingestion of {len(data_to_insert)} rows...")
        execute_values(cur, insert_query, data_to_insert)
        
        conn.commit()
        print("Successfully ingested all rows into 'nba_game_logs'.")

    except Exception as e:
        print(f"Error during ingestion: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    ingest_data()
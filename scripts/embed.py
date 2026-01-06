import psycopg2
import ollama

DB_CONFIG = {
    "dbname": "postgres",
    "user": "john",
    "password": "",
    "host": "localhost",
    "port": "5432"
}

BATCH_SIZE = 50 

def embed_game_logs():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("Successfully connected to the database.")

        while True:
            # Fetch a batch of rows where embedding is NULL
            cur.execute(
                "SELECT id, stats_summary FROM nba_game_logs WHERE embedding IS NULL LIMIT %s;",
                (BATCH_SIZE,)
            )
            rows = cur.fetchall()

            if not rows:
                print("All rows have been successfully embedded!")
                break

            print(f"Processing batch of {len(rows)} rows...")

            for row_id, text in rows:
                try:
                    # Generate embedding using Ollama
                    response = ollama.embeddings(
                        model='nomic-embed-text',
                        prompt=text
                    )
                    embedding = response['embedding']

                    # Update the row with the new vector
                    cur.execute(
                        "UPDATE nba_game_logs SET embedding = %s WHERE id = %s;",
                        (embedding, row_id)
                    )
                except Exception as e:
                    print(f"Error embedding row ID {row_id}: {e}")
                    continue

            # Commit after every batch
            conn.commit()
            print(f"Batch completed and committed.")

    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    embed_game_logs()
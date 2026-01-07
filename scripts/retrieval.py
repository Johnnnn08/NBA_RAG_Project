import psycopg2
import ollama

DB_CONFIG = {
    "dbname": "postgres",
    "user": "john",
    "password": "",
    "host": "localhost",
    "port": "5432"
}

def retrieve_info(user_question):
    # Convert user_question into a vector
    response = ollama.embeddings(model='nomic-embed-text', prompt=f"{user_question}")
    query_vector = response['embedding']

    # Connect to Postgres
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Compute Cosine distance and retrieve top 50 similar summaries
    search_query = """
        SELECT stats_summary 
        FROM nba_game_logs 
        ORDER BY embedding <=> %s::vector 
        LIMIT 50;
    """
    
    cur.execute(search_query, (query_vector,))
    results = cur.fetchall()
    
    cur.close()
    conn.close()

    # Return the summaries as a single string for the LLM
    return [row[0] for row in results]

# --- Test It ---
if __name__ == "__main__":
    question = "How did lebron play in 2026? what are some of his stats"
    context = retrieve_info(question)
    
    print(f"\nQuestion: {question}")
    print("-" * 30)
    for i, summary in enumerate(context, 1):
        print(f"Result {i}: {summary}")
import psycopg2

# Establish a connection to your PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="john",
    password="",
    host="localhost", 
    port="5432" 
)

with open("create_nba_game_logs.sql", "r") as file:
    sql_script = file.read()

# Create a cursor object and execute the SQL
cur = conn.cursor()
cur.execute(sql_script)

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Database setup complete!")

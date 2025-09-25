import psycopg2

# Connect to your database
conn = psycopg2.connect(
    host="localhost",
    database="news",
    user="postgres",
    password="Komal@123",
    port="5432"
)

cur = conn.cursor()

def query(sql, params=None):
    """
    Execute SQL query safely.
    
    sql: SQL string with optional %s placeholders
    params: tuple of values to replace %s in SQL
    """
    if params:
        cur.execute(sql, params)  # safely pass parameters
    else:
        cur.execute(sql)

    # If it's a SELECT query, return the results
    if sql.strip().lower().startswith("select"):
        return cur.fetchall()
    else:
        conn.commit()
        return 0

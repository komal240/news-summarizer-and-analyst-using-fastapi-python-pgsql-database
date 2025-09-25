import psycopg2


conn=psycopg2.connect(
    host="ep-snowy-dawn-a1jislxp-pooler.ap-southeast-1.aws.neon.tech",
    database="neondb",
    user="neondb_owner",
    password="npg_hvlDiTps72Ve",
    sslmode="require"
)

cur=conn.cursor()




def query(sql, params):
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

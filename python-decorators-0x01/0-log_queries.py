import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries

 ef log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from args or kwargs
        query = kwargs.get('query')
        if not query and args:
            query = args[0]

        print(f"[LOG] Executing SQL Query: {query}")

        start_time = datetime.time()
        result = func(*args, **kwargs)
        end_time = datetime.time()

        duration = end_time - start_time
        print(f"[LOG] Execution Time: {duration:.4f} seconds")

        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")

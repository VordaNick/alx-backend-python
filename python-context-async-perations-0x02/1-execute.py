import sqlite3

# ✅ Custom context manager to execute a query
class ExecuteQuery:
    def __init__(self, db_file, query, params=None):
        self.db_file = db_file
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        print("[INFO] Connecting to database...")
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        print(f"[INFO] Executing query: {self.query} with params: {self.params}")
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results  # this is what you get as "as result"

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            print("[INFO] Database connection closed.")
        if exc_type:
            print(f"[ERROR] Exception occurred: {exc_type.__name__} - {exc_val}")
        return False  # Propagate exceptions if any

# ✅ Use the context manager
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("users.db", query, params) as result:
    for row in result:
        print(row)

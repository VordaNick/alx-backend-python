import sqlite3

# ✅ Custom context manager for database connection
class DatabaseConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        print("[INFO] Opening database connection...")
        self.conn = sqlite3.connect(self.db_file)
        return self.conn  # will be assigned to `as conn`

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            print("[INFO] Database connection closed.")
        if exc_type:
            print(f"[ERROR] Exception occurred: {exc_type.__name__} - {exc_val}")
        return False  # Don't suppress exceptions

# ✅ Using the context manager
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()

    for row in results:
        print(row)

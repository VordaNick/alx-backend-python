import sqlite3 
import functools

# ✅ Decorator to open and close DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # open connection
        try:
            # Pass connection as the first argument
            return func(conn, *args, **kwargs)
        finally:
            conn.close()  # always close the connection
    return wrapper

# ✅ Decorator to manage transactions: commit on success, rollback on error
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # success: commit the transaction
            return result
        except Exception as e:
            conn.rollback()  # failure: rollback changes
            print(f"[ERROR] Transaction rolled back: {e}")
            raise
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

#### ✅ Update user's email with automatic connection and transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')

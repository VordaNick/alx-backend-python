import sqlite3
import asyncio

# ✅ Helper to run a query asynchronously using a thread (since sqlite3 is blocking)
async def async_query(db, query, params=()):
    loop = asyncio.get_event_loop()
    def run_query():
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    return await loop.run_in_executor(None, run_query)

# ✅ Async function to fetch all users
async def async_fetch_users():
    print("[FETCH ALL USERS] Starting...")
    users = await async_query("users.db", "SELECT * FROM users")
    print("[FETCH ALL USERS] Completed.")
    return users

# ✅ Async function to fetch users older than 40
async def async_fetch_older_users():
    print("[FETCH OLDER USERS] Starting...")
    users = await async

import asyncio
import aiosqlite

# ✅ Async function to fetch all users
async def async_fetch_users():
    print("[ALL USERS] Fetching...")
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("[ALL USERS] Done.")
            return users

# ✅ Async function to fetch users older than 40
async def async_fetch_older_users():
    print("[OLDER USERS] Fetching...")
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            users = await cursor.fetchall()
            print("[OLDER USERS] Done.")
            return users

# ✅ Concurrent runner using asyncio.gather
async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_us

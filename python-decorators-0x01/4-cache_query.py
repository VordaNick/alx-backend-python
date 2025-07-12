import time
import sqlite3 
import functools

# Global cache dictionary
query_cache = {}

# ✅ Decorator to cache query results based on query string
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Get the SQL query string
        query = kwargs.get('query') or (args[0] if args else None)
        
        if query in query_cache:
            print("[CACHE HIT] Returning cached result for query.")
            return query_cache[query]
        
        print("[CACHE MISS] Executing and caching query.")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        ret

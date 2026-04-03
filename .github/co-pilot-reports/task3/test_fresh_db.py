from task3.database import ensure_database

status = ensure_database()
print(f"Status: {status['status']}")
print(f"Message: {status['message']}")
print(f"Pokemon Count: {status['details'].get('pokemon_count', 'N/A')}")
print(f"Action Taken: {status['details'].get('action', 'N/A')}")

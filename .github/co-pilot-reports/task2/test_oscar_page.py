"""Quick test for multi-page app integration"""
import sys
from pathlib import Path

# Test path resolution
task2_path = Path(__file__).parent.parent / "task2"
print(f"Task2 path: {task2_path}")
print(f"Task2 exists: {task2_path.exists()}")

db_path = task2_path / "oscars.db"
print(f"Database path: {db_path}")
print(f"Database exists: {db_path.exists()}")

# Test import
sys.path.insert(0, str(task2_path))

try:
    from database import setup_database, Person
    from pony.orm import db_session
    
    setup_database(str(db_path), create_db=False)
    print("✓ Database setup successful")
    
    with db_session:
        count = Person.select().count()
        print(f"✓ Found {count:,} persons in database")
        
        # Test search
        import database as db_module
        query = "SELECT name FROM persons WHERE LOWER(name) LIKE '%streep%' LIMIT 1"
        results = list(db_module.db.execute(query))
        if results:
            print(f"✓ Test search found: {results[0][0]}")
    
    print("\n✅ All tests passed! Oscar Actor Explorer page should work correctly.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

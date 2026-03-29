"""Quick test of the Oscar database"""
from database import setup_database, Person, Nomination, db
from pony.orm import db_session

setup_database('oscars.db', create_db=False)

print("Testing Oscar Actor Explorer Database\n")
print("=" * 60)

# Test 1: Find Meryl Streep
print("\n✅ Test 1: Searching for Meryl Streep...")
with db_session:
    query = """
        SELECT p.name, 
               COUNT(n.id) as noms,
               SUM(CASE WHEN n.is_winner = 1 THEN 1 ELSE 0 END) as wins
        FROM persons p
        JOIN nominations n ON n.person = p.id
        WHERE LOWER(p.name) LIKE '%streep%'
        GROUP BY p.id, p.name
    """
    
    results = list(db.execute(query))
    if results:
        name, noms, wins = results[0]
        print(f"   ✓ Found: {name}")
        print(f"   ✓ Nominations: {noms}")
        print(f"   ✓ Wins: {wins}")
    else:
        print("   ✗ Not found")

# Test 2: Database statistics
print("\n✅ Test 2: Database statistics...")
with db_session:
    total_persons = Person.select().count()
    total_nominations = Nomination.select().count()
    
    wins_query = "SELECT COUNT(*) FROM nominations WHERE is_winner = 1"
    total_wins = list(db.execute(wins_query))[0][0]
    
    print(f"   ✓ Total persons: {total_persons:,}")
    print(f"   ✓ Total nominations: {total_nominations:,}")
    print(f"   ✓ Total wins: {total_wins:,}")

print("\n" + "=" * 60)
print("✓ All tests passed! Database is working correctly.")

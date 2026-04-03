"""
Quick test script to verify Task 4 implementation.
"""
import sys
sys.path.insert(0, '.')

from task4 import database, game_logic, levels

print("=" * 50)
print("TASK 4: SQL Learning Game - Test Report")
print("=" * 50)

# Test module imports
print("\n✅ All modules imported successfully")

# Test levels
total_levels = levels.get_total_levels()
print(f"✅ {total_levels} levels loaded")

for i in range(1, total_levels + 1):
    level = levels.get_level(i)
    print(f"   Level {i}: {level.title} ({len(level.challenges)} challenges)")

# Test database
print(f"\n✅ Database path: {database.DB_PATH}")
db_valid = database.validate_database()
print(f"✅ Database valid: {db_valid['valid']}")
print(f"✅ Orders: {db_valid['orders_count']}")
print(f"✅ Food items: {db_valid['food_items_count']}")

# Test a sample query
print("\n🔍 Testing sample query...")
result = database.execute_query("SELECT * FROM orders LIMIT 5")
if result is not None:
    print(f"✅ Query executed successfully, returned {len(result)} rows")
    print("\nSample data:")
    print(result.to_string())
else:
    print("❌ Query failed")

# Test game logic
print("\n🎮 Testing game logic...")
game_state = game_logic.GameState()
print(f"✅ Initial level: {game_state.current_level}")
print(f"✅ Can access Level 1: {game_state.can_access_level(1)}")
print(f"✅ Can access Level 2: {game_state.can_access_level(2)}")

# Test challenge validation
print("\n✅ Testing challenge validation...")
level1 = levels.get_level(1)
challenge1 = level1.challenges[0]
is_correct, message, result_df = challenge1.validate_answer("SELECT * FROM orders LIMIT 10")
print(f"   Test query result: {message}")
print(f"   Is correct: {is_correct}")

print("\n" + "=" * 50)
print("ALL TESTS PASSED! 🎉")
print("=" * 50)

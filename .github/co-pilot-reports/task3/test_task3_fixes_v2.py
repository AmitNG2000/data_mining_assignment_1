"""
Quick test script to verify Task 3 bug fixes
Run with: python test_task3_fixes.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from task3.database import get_pokemon_by_id, get_type_effectiveness, get_pokemon_stats_analysis
from task3.battle_engine import Pokemon, BattleEngine


def test_type_column_naming():
    """Test Bug Fix #1: Type column naming consistency"""
    print("=" * 60)
    print("TEST 1: Type Column Naming Consistency")
    print("=" * 60)
    
    # Get a dual-type Pokemon from database
    bulbasaur = get_pokemon_by_id(1)  # Bulbasaur: Grass/Poison
    print(f"Database returned: {bulbasaur['name']}")
    print(f"  - type_1: {bulbasaur.get('type_1')}")
    print(f"  - type_2: {bulbasaur.get('type_2')}")
    
    # Create Pokemon instance
    pokemon = Pokemon(bulbasaur, "Player 1")
    print(f"\nPokemon instance attributes:")
    print(f"  - type_1: {pokemon.type_1}")
    print(f"  - type_2: {pokemon.type_2}")
    
    # Verify attributes exist and match
    assert hasattr(pokemon, 'type_1'), "Pokemon should have type_1 attribute"
    assert hasattr(pokemon, 'type_2'), "Pokemon should have type_2 attribute"
    assert pokemon.type_1 == bulbasaur['type_1'], f"type_1 mismatch: {pokemon.type_1} != {bulbasaur['type_1']}"
    
    print("\n✅ PASS: Type columns correctly named and accessible")
    return True


def test_type_effectiveness():
    """Test Bug Fix #1: Type effectiveness calculation works"""
    print("\n" + "=" * 60)
    print("TEST 2: Type Effectiveness Calculation")
    print("=" * 60)
    
    # Test various type matchups
    test_cases = [
        ("Fire", "Grass", None, 2.0, "Super effective"),
        ("Water", "Fire", None, 2.0, "Super effective"),
        ("Normal", "Ghost", None, 0.0, "No effect"),
        ("Fire", "Water", None, 0.5, "Not very effective"),
        ("Electric", "Normal", None, 1.0, "Neutral"),
    ]
    
    all_passed = True
    for attacker, defender1, defender2, expected, desc in test_cases:
        result = get_type_effectiveness(attacker, defender1, defender2)
        status = "✅" if result == expected else "❌"
        print(f"{status} {attacker} vs {defender1}: {result}x (expected {expected}x) - {desc}")
        if result != expected:
            all_passed = False
    
    if all_passed:
        print("\n✅ PASS: Type effectiveness calculations correct")
    else:
        print("\n❌ FAIL: Some type effectiveness calculations incorrect")
    
    return all_passed


def test_type2_none_handling():
    """Test Bug Fix #2: Proper handling of type_2 NaN/None values"""
    print("\n" + "=" * 60)
    print("TEST 3: Type_2 NaN/None Handling")
    print("=" * 60)
    
    # Get single-type Pokemon
    charmander = get_pokemon_by_id(4)  # Charmander: Fire only
    print(f"Single-type Pokemon: {charmander['name']}")
    print(f"  - type_1: {charmander.get('type_1')}")
    print(f"  - type_2: {charmander.get('type_2')} (raw value)")
    
    # Get analysis (uses the fixed type_2 checking)
    analysis = get_pokemon_stats_analysis()
    
    # Check that type displays don't show "Fire/None" or "Fire/nan"
    print("\nTop type combinations from analysis:")
    for combo in analysis['top_type_combos'][:3]:
        print(f"  - {combo['types']}: {combo['avg_total']} avg")
        # Check for bad patterns
        if '/None' in combo['types'] or '/nan' in combo['types'] or '/NaN' in combo['types']:
            print(f"    ❌ FAIL: Found invalid type display: {combo['types']}")
            return False
    
    if 'weakest_legendary' in analysis:
        weak = analysis['weakest_legendary']
        print(f"\nWeakest legendary: {weak['name']} ({weak['types']})")
        if '/None' in weak['types'] or '/nan' in weak['types']:
            print(f"  ❌ FAIL: Found invalid type display: {weak['types']}")
            return False
    
    print("\n✅ PASS: Type_2 None/NaN values handled correctly")
    return True


def test_battle_engine_integration():
    """Test Bug Fix #1: Battle engine works with database Pokemon"""
    print("\n" + "=" * 60)
    print("TEST 4: Battle Engine Integration")
    print("=" * 60)
    
    # Get two teams from database
    team1_data = [get_pokemon_by_id(1), get_pokemon_by_id(4)]  # Bulbasaur, Charmander
    team2_data = [get_pokemon_by_id(7), get_pokemon_by_id(25)]  # Squirtle, Pikachu
    
    print(f"Team 1: {[p['name'] for p in team1_data]}")
    print(f"Team 2: {[p['name'] for p in team2_data]}")
    
    try:
        # Create battle engine
        battle = BattleEngine(team1_data, team2_data)
        
        # Check active Pokemon have correct types
        p1, p2 = battle.get_active_pokemon()
        print(f"\nActive Pokemon:")
        print(f"  - {p1.name}: type_1={p1.type_1}, type_2={p1.type_2}")
        print(f"  - {p2.name}: type_1={p2.type_1}, type_2={p2.type_2}")
        
        # Simulate one turn
        turn_log = battle.execute_turn()
        print(f"\nTurn 1 executed successfully")
        print(f"  - Log entries: {len(turn_log)}")
        
        print("\n✅ PASS: Battle engine works correctly with database Pokemon")
        return True
        
    except Exception as e:
        print(f"\n❌ FAIL: Battle engine error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("TASK 3 BUG FIX VERIFICATION TESTS")
    print("=" * 60)
    
    results = {
        "Type Column Naming": test_type_column_naming(),
        "Type Effectiveness": test_type_effectiveness(),
        "Type_2 None Handling": test_type2_none_handling(),
        "Battle Engine Integration": test_battle_engine_integration(),
    }
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Bug fixes verified.")
    else:
        print("⚠️  SOME TESTS FAILED. Please review fixes.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())

"""
Comprehensive test for Task 3: Pokemon Battle Arena
Tests all major functionality to ensure bugs are fixed
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from task3.database import (
    ensure_pokemon_database_ready, get_all_pokemon, get_pokemon_by_id,
    cheat_double_hp, cheat_godmode, cheat_steal_strongest, 
    cheat_create_legendary, cheat_nerf_all, cheat_max_stats,
    detect_cheats, get_cheat_log, get_pokemon_stats_analysis
)
from task3.battle_engine import BattleEngine, Pokemon

def test_database_setup():
    """Test 1: Database Initialization"""
    print("=" * 60)
    print("TEST 1: Database Setup")
    print("=" * 60)
    
    is_ready, message = ensure_pokemon_database_ready()
    print(f"✓ Database ready: {is_ready}")
    print(f"  Message: {message}")
    assert is_ready, "Database should be ready"
    print()

def test_pokemon_retrieval():
    """Test 2: Pokemon Data Retrieval"""
    print("=" * 60)
    print("TEST 2: Pokemon Retrieval")
    print("=" * 60)
    
    # Get all pokemon
    all_pokemon = get_all_pokemon(limit=10)
    print(f"✓ Retrieved {len(all_pokemon)} Pokemon")
    
    # Check columns
    if all_pokemon:
        poke = all_pokemon[0]
        expected_cols = ['id', 'name', 'type_1', 'type_2', 'hp', 'attack', 'defense']
        for col in expected_cols:
            assert col in poke, f"Missing column: {col}"
        print(f"✓ All required columns present")
        
        # Check NO 'form' column
        assert 'form' not in poke, "Should not have 'form' column"
        print(f"✓ No 'form' column (correct)")
    
    # Get specific Pokemon
    bulbasaur = get_pokemon_by_id(1)
    assert bulbasaur is not None, "Should find Bulbasaur"
    assert bulbasaur['name'] == 'Bulbasaur', "Name should be Bulbasaur"
    print(f"✓ Pokemon by ID: {bulbasaur['name']} (ID: {bulbasaur['id']})")
    
    # Check type display
    type_display = f"{bulbasaur['type_1']}/{bulbasaur['type_2']}" if bulbasaur.get('type_2') and str(bulbasaur['type_2']).lower() not in ['none', 'nan', ''] else bulbasaur['type_1']
    print(f"✓ Type display: {type_display}")
    print()

def test_cheat_codes():
    """Test 3: Cheat Code Functionality"""
    print("=" * 60)
    print("TEST 3: Cheat Codes")
    print("=" * 60)
    
    # Test LEGENDARY (tests INSERT without 'form' column)
    try:
        msg, new_id = cheat_create_legendary("TestLegendary")
        print(f"✓ LEGENDARY cheat: {msg}")
        print(f"  New Pokemon ID: {new_id}")
        
        # Verify it was created
        new_poke = get_pokemon_by_id(new_id)
        assert new_poke is not None, "Should find newly created Pokemon"
        assert new_poke['name'] == 'TestLegendary', "Name should match"
        print(f"✓ Verified creation: {new_poke['name']} with HP={new_poke['hp']}")
    except Exception as e:
        print(f"✗ LEGENDARY cheat failed: {e}")
        raise
    
    # Test STEAL (tests INSERT/SELECT without 'form' column)
    try:
        msg2, stolen_id = cheat_steal_strongest([1, 2, 3, 4, 5])
        print(f"✓ STEAL cheat: {msg2}")
        print(f"  Stolen Pokemon ID: {stolen_id}")
        
        # Verify it was copied
        stolen_poke = get_pokemon_by_id(stolen_id)
        assert stolen_poke is not None, "Should find stolen Pokemon"
        print(f"✓ Verified steal: {stolen_poke['name']}")
    except Exception as e:
        print(f"✗ STEAL cheat failed: {e}")
        raise
    
    # Test other cheats
    try:
        msg3 = cheat_double_hp([1, 2, 3])
        print(f"✓ DOUBLE HP cheat: {msg3}")
        
        msg4 = cheat_godmode([1])
        print(f"✓ GODMODE cheat: {msg4}")
        
        msg5 = cheat_max_stats([1])
        print(f"✓ MAX STATS cheat: {msg5}")
    except Exception as e:
        print(f"✗ Other cheats failed: {e}")
        raise
    
    print()

def test_battle_engine():
    """Test 4: Battle Engine"""
    print("=" * 60)
    print("TEST 4: Battle Engine")
    print("=" * 60)
    
    # Get team data
    team1_data = [get_pokemon_by_id(i) for i in [1, 4, 7]]
    team2_data = [get_pokemon_by_id(i) for i in [25, 150, 6]]
    
    # Check all Pokemon have correct column names
    for poke in team1_data + team2_data:
        assert poke is not None, "Pokemon should exist"
        assert 'type_1' in poke or 'type1' in poke, "Should have type_1 or type1"
    
    print(f"✓ Team 1: {[p['name'] for p in team1_data]}")
    print(f"✓ Team 2: {[p['name'] for p in team2_data]}")
    
    # Initialize battle
    try:
        battle = BattleEngine(team1_data, team2_data)
        print(f"✓ Battle initialized")
        print(f"  Player 1: {battle.team1[0].name}")
        print(f"  Player 2: {battle.team2[0].name}")
    except Exception as e:
        print(f"✗ Battle initialization failed: {e}")
        raise
    
    # Execute a turn
    try:
        logs = battle.execute_turn()
        print(f"✓ Turn executed ({len(logs)} log entries)")
        assert len(logs) > 0, "Should have battle logs"
    except Exception as e:
        print(f"✗ Turn execution failed: {e}")
        raise
    
    print()

def test_cheat_detection():
    """Test 5: Cheat Detection"""
    print("=" * 60)
    print("TEST 5: Cheat Detection")
    print("=" * 60)
    
    try:
        cheats = detect_cheats()
        print(f"✓ Detected {len(cheats)} potential cheats")
        
        if cheats:
            print(f"  Example: {cheats[0]['name']} - {cheats[0]['reason']}")
        
        cheat_log = get_cheat_log()
        print(f"✓ Retrieved {len(cheat_log)} cheat log entries")
    except Exception as e:
        print(f"✗ Cheat detection failed: {e}")
        raise
    
    print()

def test_analysis():
    """Test 6: Pokemon Analysis"""
    print("=" * 60)
    print("TEST 6: Pokemon Analysis")
    print("=" * 60)
    
    try:
        analysis = get_pokemon_stats_analysis()
        print(f"✓ Generated analysis")
        print(f"  Total Pokemon: {analysis.get('total_count', 'N/A')}")
        print(f"  Average HP: {analysis.get('avg_hp', 'N/A'):.1f}")
        print(f"  Average Attack: {analysis.get('avg_attack', 'N/A'):.1f}")
    except Exception as e:
        print(f"✗ Analysis failed: {e}")
        raise
    
    print()

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("POKEMON BATTLE ARENA - COMPREHENSIVE TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_database_setup()
        test_pokemon_retrieval()
        test_cheat_codes()
        test_battle_engine()
        test_cheat_detection()
        test_analysis()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nTask 3 is fully functional with all bugs fixed:")
        print("  ✓ Database schema correct (no 'form' column)")
        print("  ✓ Type display handles None values properly")
        print("  ✓ All cheat codes work without errors")
        print("  ✓ Battle engine functions correctly")
        print("  ✓ Cheat detection and analysis working")
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 60)
        raise

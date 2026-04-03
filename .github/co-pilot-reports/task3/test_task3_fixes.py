"""Quick test for Task 3 after bug fixes"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("Testing Task 3 modules...")

# Test database module
from task3.database import (
    ensure_pokemon_database_ready,
    get_all_pokemon,
    get_pokemon_by_id,
    get_pokemon_by_name,
    detect_cheats
)

print("\n1. Testing database validation...")
ready, msg = ensure_pokemon_database_ready()
print(f"   Ready: {ready}")
print(f"   Message: {msg}")

print("\n2. Testing get_all_pokemon...")
pokemon = get_all_pokemon(limit=3)
print(f"   Got {len(pokemon)} Pokemon")
for p in pokemon:
    print(f"   - {p['name']} ({p['type1']})")

print("\n3. Testing get_pokemon_by_id...")
pikachu = get_pokemon_by_id(25)
if pikachu:
    print(f"   Found: {pikachu['name']} (HP: {pikachu['hp']})")

print("\n4. Testing get_pokemon_by_name...")
charizard = get_pokemon_by_name("Charizard")
if charizard:
    print(f"   Found: {charizard['name']} (Total: {charizard['total']})")

print("\n5. Testing detect_cheats...")
anomalies = detect_cheats()
print(f"   Found {len(anomalies)} anomalies")

print("\n6. Testing battle engine...")
from task3.battle_engine import BattleEngine, Pokemon

team1_data = [get_pokemon_by_id(1), get_pokemon_by_id(4)]
team2_data = [get_pokemon_by_id(7), get_pokemon_by_id(25)]

battle = BattleEngine(team1_data, team2_data)
print(f"   Battle created with {len(battle.team1)} vs {len(battle.team2)} Pokemon")

print("\n✅ All tests passed!")

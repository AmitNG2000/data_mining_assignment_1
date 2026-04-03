from task3 import get_all_pokemon, get_pokemon_by_name

# Test loading all Pokemon
pokemon_list = get_all_pokemon()
print(f"Total Pokemon loaded: {len(pokemon_list)}")

# Test getting specific Pokemon
pikachu = get_pokemon_by_name("Pikachu")
if pikachu:
    print(f"\nPikachu stats:")
    print(f"  HP: {pikachu['hp']}")
    print(f"  Attack: {pikachu['attack']}")
    print(f"  Defense: {pikachu['defense']}")
    print(f"  Speed: {pikachu['speed']}")
    print(f"  Type: {pikachu['type1']}/{pikachu['type2']}")

# Test getting first few Pokemon
print("\nFirst 5 Pokemon:")
for p in pokemon_list[:5]:
    print(f"  {p['name']} - {p['type1']}/{p['type2']} - Total: {p['total']}")

print("\nDatabase test successful!")

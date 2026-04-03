# Task 3: Pokémon Battle Arena ⚔️

## Overview
A turn-based battle game powered by a database, where type effectiveness plays a key role in combat. All Pokémon stats are stored in an SQLite database, and players can use real SQL queries as cheat codes. Each action is tracked with a log database.


**Note**: See the [main README](../README.md) for installation instructions and more detailes.

## Features

### Team Selection
- Browse and select 1-3 Pokémon from a database of 800+ Pokémon.
- All stats loaded from SQLite database.
- View detailed stats: HP, Attack, Defense, Speed

### Battle System
- **Turn-based combat** 
- **Damage calculation**: `(Attack * Power / Defense) * Type_Effectiveness * Random(0.85-1.0)`
- **Type effectiveness system** from database.
- **HP bars** with color coded health indicators.
- **Battle log** showing detailed turn-by-turn actions.
- **Auto-battle** mode for quick simulations.

### Cheat Code System

All cheat codes execute **real SQL operations** on the database:

| Cheat Code | Effect | SQL Operation |
|------------|--------|---------------|
| `UPUPDOWNDOWN` | Double HP | `UPDATE pokemon SET hp = hp * 2` |
| `GODMODE` | Defense/Sp.Def = 999 | `UPDATE pokemon SET defense = 999, sp_def = 999` |
| `MAXPOWER` | All stats = 255 | `UPDATE pokemon SET hp=255, attack=255, ...` |
| `STEAL` | Copy strongest Pokémon | `INSERT INTO pokemon SELECT ...` |
| `LEGENDARY` | Create custom OP Pokémon | `INSERT INTO pokemon VALUES (...)` |
| `NERF` | Reduce opponent stats by 50% | `UPDATE pokemon SET ... * 0.5` |

### Cheat Detection & Audit

SQL-based anomaly detection:
- Impossible stats (> 255)
- GODMODE signature (Defense = 999)
- Custom Pokémon (is_custom = 1)
- Complete cheat log with timestamps

### Statistical Analysis

Pattern discovery from Pokémon dataset:
1. **Most Overpowered Type Combinations** 
2. **Power Generations Analysis** across generations
3. **Weakest Legendary Pokémon**


## Technology Stack

### Database: SQLite3
**Why SQLite?**
- Lightweight and file-based (no server setup required).
- Good for dataset size
- Built-in Python support

### Data Processing: Pandas + Raw SQL
**Hybrid approach:**
- **Read operations (SELECT)**: Use `pd.read_sql_query()` for clean data retrieval and analysis.

**Benefits:**
- More Pythonic and readable code for queries.
- Easier data manipulation with pandas.
- Better Streamlit integration (native DataFrame display).
- Reliable transactions for database modifications.


## Database Schema

### Core Tables

#### 1. **pokemon**
Main table storing all Pokémon stats from CSV.

```sql
CREATE TABLE pokemon (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type_1 TEXT NOT NULL,
    type_2 TEXT,
    hp INTEGER NOT NULL,
    attack INTEGER NOT NULL,
    defense INTEGER NOT NULL,
    sp_atk INTEGER NOT NULL,
    sp_def INTEGER NOT NULL,
    speed INTEGER NOT NULL,
    total INTEGER,
    generation INTEGER,
    legendary INTEGER,
    is_custom INTEGER DEFAULT 0  -- Tracks cheated/custom Pokémon
);
```

**Key Points:**
- `type_2` can be NULL for single-type Pokémon
- `total` is sum of all base stats (HP + ATK + DEF + SP.ATK + SP.DEF + SPD)
- `is_custom = 1` marks Pokémon created by cheats (STEAL, LEGENDARY)

#### 2. **type_effectiveness**
Stores type matchup multipliers for damage calculation.

```sql
CREATE TABLE type_effectiveness (
    attacker_type TEXT NOT NULL,
    defender_type TEXT NOT NULL,
    multiplier REAL NOT NULL,
    PRIMARY KEY (attacker_type, defender_type)
);
```

**Examples:**
- `('Fire', 'Grass', 2.0)` - Fire is super effective against Grass
- `('Fire', 'Water', 0.5)` - Fire is not very effective against Water
- `('Electric', 'Ground', 0.0)` - Electric has no effect on Ground

**Coverage:** 100+ type matchup rules

#### 3. **cheat_log**
Audit trail for all cheat code usage.

```sql
CREATE TABLE cheat_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cheat_code TEXT NOT NULL,
    pokemon_affected TEXT,
    description TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Usage:**
Every cheat execution logs:
- Which cheat was used
- Which Pokémon were affected
- What changes were made
- When it happened

#### 4. **battle_history**
Optional table for tracking battle outcomes.

```sql
CREATE TABLE battle_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    winner TEXT NOT NULL,
    player1_team TEXT,
    player2_team TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```


### Dataset Details

- **Source**: [Pokémon with Stats (Kaggle)](https://www.kaggle.com/datasets/abcsds/pokemon).  
  The `#` column was renamed to `id`, and a `legendary` column was added with values of 0.
- **Size**: 721 original Pokémon (+ custom from cheats).
- **Generations**: 1-6
- **Columns**: 13 (id, name, type_1, type_2, total, hp, attack, defense, sp_atk, sp_def, speed, generation, legendary).


## Battle Mechanics

### Turn Order
- Faster Pokémon attacks first each turn.

### Damage Calculation
```python
Base_Damage = (Attack * 50 / Defense) * 0.4
Type_Multiplier = get_type_effectiveness(attacker_type, defender_type_1, defender_type_2)
Random_Factor = random.uniform(0.85, 1.0)
Final_Damage = int(Base_Damage * Type_Multiplier * Random_Factor)
```

### Type Effectiveness (Dual-Type)
Multipliers stack for dual-type Pokémon.  
Examples:
- Water vs Fire/Rock: 2.0 × 2.0 = 4x damage
- Grass vs Fire/Flying: 0.5 × 0.5 = 0.25x damage

### Win Condition
Battle ends when all Pokémon on one team have HP ≤ 0.


## Cheat Detection Queries

The app uses SQL queries to detect abnormal stats and modifications:

```sql
-- Detect impossible stats (natural max is 255)
SELECT name, hp, attack, defense, sp_atk, sp_def, speed
FROM pokemon
WHERE hp > 255 OR attack > 255 OR defense > 255
   OR sp_atk > 255 OR sp_def > 255 OR speed > 255;

-- Detect GODMODE signature
SELECT name, defense, sp_def 
FROM pokemon
WHERE defense = 999 OR sp_def = 999;

-- Find custom/stolen Pokémon
SELECT name, total, is_custom 
FROM pokemon 
WHERE is_custom = 1;

-- View complete cheat log
SELECT * FROM cheat_log 
ORDER BY timestamp DESC;
```



## Interesting Findings

### 1. Type Combination Power Rankings

**Top 5 Most Overpowered Type Combinations** (min 3 Pokémon):
1. **Dragon/Ice** - Avg Total: 686.67
   - Example: Kyurem (660), Kyurem-Black (700), Kyurem-White (700)
2. **Dragon/Psychic** - Avg Total: 650.00
   - Example: Latios (600), Latias (600), Mega Latios (700)
3. **Dragon/Flying** - Avg Total: 641.67
   - Example: Dragonite (600), Salamence (600), Rayquaza (680)

**Finding:** Dragon-type combinations dominate the power rankings, appearing in all top 5 slots.

### 2. Power Creep Analysis

Average total stats by generation:

| Generation | Count | Avg Total | Avg HP | Avg Attack | Avg Speed |
|------------|-------|-----------|--------|------------|-----------|
| 1 | 151 | 425.4 | 68.2 | 77.5 | 66.8 |
| 2 | 100 | 414.8 | 66.1 | 72.4 | 62.1 |
| 3 | 135 | 420.3 | 68.8 | 73.9 | 64.5 |
| 4 | 107 | 452.1 | 73.4 | 81.2 | 70.3 |
| 5 | 156 | 475.2 | 77.1 | 86.5 | 74.8 |
| 6 | 72 | 489.7 | 78.9 | 89.3 | 77.2 |

**Evidence of power creep:** 
- Stats increase by ~10-15 points per generation
- Generation 6 Pokémon are 15% stronger than Generation 1 on average
- Most dramatic jump between Gen 3 → Gen 4 (+31.8 total)

### 3. Weakest Legendary Pokémon

**Articuno** (Generation 1) - Ice/Flying type
- **Total Stats:** 580
- **Context:** Barely above the legendary threshold (600).
- **Comparison:** 41 non-legendary Pokémon have higher total stats.

**Why interesting:** Part of the iconic legendary bird trio but has the lowest stats among all legendary Pokémon, suggesting early game design didn't emphasize "legendary = overpowered".


## How It Works

### Battle Flow
1. User selects 1-3 Pokémon for each team from database.
2. Battle engine initializes with Pokémon data from database.
3. Each turn:
   - Speed determines turn order
   - Attacker's type vs defender's types queried from `type_effectiveness` table
   - Damage calculated and applied.
   - Switch to next Pokémon if current faints.
4. Battle ends when one team has no Pokémon left.

### Cheat System Flow
1. User enters cheat code in Cheat Codes tab
2. Code executes SQL UPDATE/INSERT query on database
3. Changes logged to `cheat_log` table
4. Modified Pokémon stats persist in database
5. Detection queries can identify abnormal values

### Database Auto-Initialization
- On page load, app checks if `pokemon.db` exists.
- If missing/corrupted, automatically creates from `pokemon.csv`.
- Creates all 4 tables with proper schema.
- Populates `type_effectiveness` with 100+ matchup rules.


## File Structure

```
task3/
├── database.py           # Database operations, cheat codes, analysis
├── battle_engine.py      # Battle mechanics and damage calculation  
├── pokemon.csv           # Pokémon dataset (721 entries)
└── pokemon.db            # SQLite database (auto-generated)
```

**Note:** All Pokémon stats are loaded from database at runtime. Cheats modify the actual database (use "Reset Database" button to restore original state).
- Cheat log table tracks all modifications.
"""
Database module for Pokémon Battle Arena
Handles all database operations including setup, queries, and cheat codes
"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import os
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
project_root_str = str(PROJECT_ROOT)
if project_root_str in sys.path:
    sys.path.remove(project_root_str)
sys.path.insert(0, project_root_str)

from utils import ensure_database_ready, get_connection as _base_get_connection, create_database


def get_connection(db_path: str | Path) -> sqlite3.Connection:
    """Task 3 connection wrapper with pragmatic lock handling for Streamlit reruns."""
    conn = _base_get_connection(db_path)
    conn.execute("PRAGMA busy_timeout = 30000")
    try:
        conn.execute("PRAGMA journal_mode = WAL")
    except sqlite3.Error:
        # Fallback silently if WAL cannot be enabled in current environment.
        pass
    return conn

DB_PATH = Path(__file__).parent / "pokemon.db"
CSV_PATH = Path(__file__).parent / "pokemon.csv"
TABLE_NAME = "pokemon"


# Non-neutral type interactions (multiplier != 1.0).
_TYPE_EFFECTIVENESS_ROWS = [
    ("Normal", "Rock", 0.5), ("Normal", "Ghost", 0.0), ("Normal", "Steel", 0.5),
    ("Fire", "Fire", 0.5), ("Fire", "Water", 0.5), ("Fire", "Grass", 2.0), ("Fire", "Ice", 2.0),
    ("Fire", "Bug", 2.0), ("Fire", "Rock", 0.5), ("Fire", "Dragon", 0.5), ("Fire", "Steel", 2.0),
    ("Water", "Fire", 2.0), ("Water", "Water", 0.5), ("Water", "Grass", 0.5), ("Water", "Ground", 2.0),
    ("Water", "Rock", 2.0), ("Water", "Dragon", 0.5),
    ("Electric", "Water", 2.0), ("Electric", "Electric", 0.5), ("Electric", "Grass", 0.5),
    ("Electric", "Ground", 0.0), ("Electric", "Flying", 2.0), ("Electric", "Dragon", 0.5),
    ("Grass", "Fire", 0.5), ("Grass", "Water", 2.0), ("Grass", "Grass", 0.5), ("Grass", "Poison", 0.5),
    ("Grass", "Ground", 2.0), ("Grass", "Flying", 0.5), ("Grass", "Bug", 0.5), ("Grass", "Rock", 2.0),
    ("Grass", "Dragon", 0.5), ("Grass", "Steel", 0.5),
    ("Ice", "Fire", 0.5), ("Ice", "Water", 0.5), ("Ice", "Grass", 2.0), ("Ice", "Ice", 0.5),
    ("Ice", "Ground", 2.0), ("Ice", "Flying", 2.0), ("Ice", "Dragon", 2.0), ("Ice", "Steel", 0.5),
    ("Fighting", "Normal", 2.0), ("Fighting", "Ice", 2.0), ("Fighting", "Poison", 0.5), ("Fighting", "Flying", 0.5),
    ("Fighting", "Psychic", 0.5), ("Fighting", "Bug", 0.5), ("Fighting", "Rock", 2.0), ("Fighting", "Ghost", 0.0),
    ("Fighting", "Dark", 2.0), ("Fighting", "Steel", 2.0), ("Fighting", "Fairy", 0.5),
    ("Poison", "Grass", 2.0), ("Poison", "Poison", 0.5), ("Poison", "Ground", 0.5), ("Poison", "Rock", 0.5),
    ("Poison", "Ghost", 0.5), ("Poison", "Steel", 0.0), ("Poison", "Fairy", 2.0),
    ("Ground", "Fire", 2.0), ("Ground", "Electric", 2.0), ("Ground", "Grass", 0.5), ("Ground", "Poison", 2.0),
    ("Ground", "Flying", 0.0), ("Ground", "Bug", 0.5), ("Ground", "Rock", 2.0), ("Ground", "Steel", 2.0),
    ("Flying", "Electric", 0.5), ("Flying", "Grass", 2.0), ("Flying", "Fighting", 2.0), ("Flying", "Bug", 2.0),
    ("Flying", "Rock", 0.5), ("Flying", "Steel", 0.5),
    ("Psychic", "Fighting", 2.0), ("Psychic", "Poison", 2.0), ("Psychic", "Psychic", 0.5),
    ("Psychic", "Dark", 0.0), ("Psychic", "Steel", 0.5),
    ("Bug", "Fire", 0.5), ("Bug", "Grass", 2.0), ("Bug", "Fighting", 0.5), ("Bug", "Poison", 0.5),
    ("Bug", "Flying", 0.5), ("Bug", "Psychic", 2.0), ("Bug", "Ghost", 0.5), ("Bug", "Dark", 2.0),
    ("Bug", "Steel", 0.5), ("Bug", "Fairy", 0.5),
    ("Rock", "Fire", 2.0), ("Rock", "Ice", 2.0), ("Rock", "Fighting", 0.5), ("Rock", "Ground", 0.5),
    ("Rock", "Flying", 2.0), ("Rock", "Bug", 2.0), ("Rock", "Steel", 0.5),
    ("Ghost", "Normal", 0.0), ("Ghost", "Psychic", 2.0), ("Ghost", "Ghost", 2.0), ("Ghost", "Dark", 0.5),
    ("Dragon", "Dragon", 2.0), ("Dragon", "Steel", 0.5), ("Dragon", "Fairy", 0.0),
    ("Dark", "Fighting", 0.5), ("Dark", "Psychic", 2.0), ("Dark", "Ghost", 2.0), ("Dark", "Dark", 0.5), ("Dark", "Fairy", 0.5),
    ("Steel", "Fire", 0.5), ("Steel", "Water", 0.5), ("Steel", "Electric", 0.5), ("Steel", "Ice", 2.0),
    ("Steel", "Rock", 2.0), ("Steel", "Steel", 0.5), ("Steel", "Fairy", 2.0),
    ("Fairy", "Fire", 0.5), ("Fairy", "Fighting", 2.0), ("Fairy", "Poison", 0.5), ("Fairy", "Dragon", 2.0),
    ("Fairy", "Dark", 2.0), ("Fairy", "Steel", 0.5),
]


def _normalize_type_name(type_name: Optional[str]) -> Optional[str]:
    """Normalize type names coming from DB/CSV values."""
    if type_name is None or pd.isna(type_name):
        return None
    cleaned = str(type_name).strip()
    return cleaned if cleaned else None


def _ensure_task3_tables() -> None:
    """Ensure Task 3 auxiliary tables and seed data exist."""
    conn = get_connection(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
        pokemon_columns = {row[1] for row in cursor.fetchall()}
        if "is_custom" not in pokemon_columns:
            cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN is_custom INTEGER DEFAULT 0")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS type_effectiveness (
                attacker_type TEXT NOT NULL,
                defender_type TEXT NOT NULL,
                multiplier REAL NOT NULL,
                PRIMARY KEY (attacker_type, defender_type)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS battle_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                winner TEXT NOT NULL,
                player1_team TEXT,
                player2_team TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cheat_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cheat_code TEXT NOT NULL,
                pokemon_affected TEXT,
                description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute("SELECT COUNT(*) FROM type_effectiveness")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                """
                INSERT OR REPLACE INTO type_effectiveness (attacker_type, defender_type, multiplier)
                VALUES (?, ?, ?)
                """,
                _TYPE_EFFECTIVENESS_ROWS,
            )

        conn.commit()
    finally:
        conn.close()


def ensure_pokemon_database_ready() -> Tuple[bool, str]:
    """Ensure the SQLite database and required table exist."""
    is_ready, message = ensure_database_ready(db_path=DB_PATH, csv_path=CSV_PATH, table_name=TABLE_NAME)
    _ensure_task3_tables()
    return is_ready, f"{message} Task 3 tables verified."


def get_all_pokemon(limit: int = None) -> List[Dict]:
    """Get all Pokémon from database using pandas (excludes custom/cheated Pokemon)"""
    conn = get_connection(DB_PATH)
    
    query = f"""
        SELECT id, name, type_1, type_2, hp, attack, defense, 
               sp_atk, sp_def, speed, total, generation, legendary
        FROM {TABLE_NAME}
        WHERE id IS NOT NULL AND is_custom = 0
        ORDER BY id
    """
    
    if limit:
        query += f" LIMIT {limit}"
    
    # Use pandas to read SQL query
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Convert to list of dictionaries
    return df.to_dict('records')


def get_pokemon_by_id(pokemon_id: int) -> Optional[Dict]:
    """Get a specific Pokémon by ID using pandas"""
    conn = get_connection(DB_PATH)
    
    # Read pokemon table into DataFrame
    df = pd.read_sql_query(f"""
        SELECT id, name, type_1, type_2, hp, attack, defense,
               sp_atk, sp_def, speed, total, generation, legendary
        FROM {TABLE_NAME}
        WHERE id = ?
    """, conn, params=(pokemon_id,))
    
    conn.close()
    
    if len(df) > 0:
        return df.iloc[0].to_dict()
    return None


def get_pokemon_by_name(name: str) -> Optional[Dict]:
    """Get a specific Pokémon by name using pandas"""
    conn = get_connection(DB_PATH)
    
    # Read all pokemon (case-insensitive search)
    df = pd.read_sql_query(f"""
        SELECT id, name, type_1, type_2, hp, attack, defense,
               sp_atk, sp_def, speed, total, generation, legendary
        FROM {TABLE_NAME}
        WHERE LOWER(name) = LOWER(?)
    """, conn, params=(name,))
    
    conn.close()
    
    if len(df) > 0:
        return df.iloc[0].to_dict()
    return None


def get_type_effectiveness(attacker_type: str, defender_type_1: str, defender_type_2: str = None) -> float:
    """Calculate type effectiveness multiplier"""
    attacker_type = _normalize_type_name(attacker_type)
    defender_type_1 = _normalize_type_name(defender_type_1)
    defender_type_2 = _normalize_type_name(defender_type_2)

    if not attacker_type or not defender_type_1:
        return 1.0

    conn = get_connection(DB_PATH)
    cursor = conn.cursor()
    
    multiplier = 1.0

    try:
        # Check against first type
        cursor.execute("""
            SELECT multiplier FROM type_effectiveness
            WHERE attacker_type = ? AND defender_type = ?
        """, (attacker_type, defender_type_1))

        result = cursor.fetchone()
        if result:
            multiplier *= result[0]

        # Check against second type if it exists
        if defender_type_2:
            cursor.execute("""
                SELECT multiplier FROM type_effectiveness
                WHERE attacker_type = ? AND defender_type = ?
            """, (attacker_type, defender_type_2))

            result = cursor.fetchone()
            if result:
                multiplier *= result[0]
    except sqlite3.Error:
        # Keep battles playable even if DB is temporarily inconsistent.
        multiplier = 1.0
    finally:
        conn.close()

    return multiplier


def log_battle(winner: str, player1_team: List[str], player2_team: List[str]):
    """Log battle result to database"""
    conn = get_connection(DB_PATH)
    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO battle_history (winner, player1_team, player2_team)
            VALUES (?, ?, ?)
        """, (winner, ','.join(player1_team), ','.join(player2_team)))

        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()


def log_cheat(cheat_code: str, pokemon_affected: str, description: str):
    """Log cheat code usage"""
    conn = get_connection(DB_PATH)
    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO cheat_log (cheat_code, pokemon_affected, description)
            VALUES (?, ?, ?)
        """, (cheat_code, pokemon_affected, description))

        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()


def _log_cheat_with_cursor(cursor: sqlite3.Cursor, cheat_code: str, pokemon_affected: str, description: str):
    """Log cheat usage using an existing transaction to avoid DB lock contention."""
    cursor.execute(
        """
        INSERT INTO cheat_log (cheat_code, pokemon_affected, description)
        VALUES (?, ?, ?)
        """,
        (cheat_code, pokemon_affected, description),
    )


# ============== CHEAT CODES ==============

def cheat_double_hp(pokemon_ids: List[int]) -> str:
    """UPUPDOWNDOWN - Double HP for specified Pokémon"""
    conn = get_connection(DB_PATH)
    try:
        cursor = conn.cursor()

        affected = []
        for pid in pokemon_ids:
            cursor.execute("SELECT name, hp FROM pokemon WHERE id = ?", (pid,))
            pokemon_row = cursor.fetchone()
            cursor.execute("""
                UPDATE pokemon
                SET hp = hp * 2
                WHERE id = ?
            """, (pid,))

            if pokemon_row:
                name, old_hp = pokemon_row
                affected.append(name)
                _log_cheat_with_cursor(cursor, 'UPUPDOWNDOWN', name, f"Doubled HP to {old_hp * 2}")

        conn.commit()
        return f"✨ Cheat activated! HP doubled for: {', '.join(affected)}"
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()


def cheat_godmode(pokemon_ids: List[int]) -> str:
    """GODMODE - Set Defense and Sp.Def to 999"""
    conn = get_connection(DB_PATH)
    try:
        cursor = conn.cursor()

        affected = []
        for pid in pokemon_ids:
            cursor.execute("SELECT name FROM pokemon WHERE id = ?", (pid,))
            pokemon_row = cursor.fetchone()
            cursor.execute("""
                UPDATE pokemon
                SET defense = 999, sp_def = 999
                WHERE id = ?
            """, (pid,))

            if pokemon_row:
                name = pokemon_row[0]
                affected.append(name)
                _log_cheat_with_cursor(cursor, 'GODMODE', name, "Set Defense and Sp.Def to 999")

        conn.commit()
        return f"🛡️ GOD MODE activated! Defense = 999 for: {', '.join(affected)}"
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()



def cheat_steal_strongest(player_team: List[int]) -> Tuple[str, Optional[int]]:
    """STEAL - Copy opponent's strongest Pokémon to your team"""
    conn = get_connection(DB_PATH)
    cursor = conn.cursor()

    try:
        if player_team:
            placeholders = ",".join(["?"] * len(player_team))
            query = f"""
                SELECT id, name, total
                FROM {TABLE_NAME}
                WHERE id NOT IN ({placeholders})
                  AND is_custom = 0
                ORDER BY total DESC
                LIMIT 1
            """
            cursor.execute(query, player_team)
        else:
            query = f"""
                SELECT id, name, total
                FROM {TABLE_NAME}
                WHERE is_custom = 0
                ORDER BY total DESC
                LIMIT 1
            """
            cursor.execute(query)

        strongest = cursor.fetchone()

        if strongest is None:
            return "❌ No Pokémon available to steal!", None

        pokemon_id, name, total = strongest

        cursor.execute(f"""
            INSERT INTO {TABLE_NAME}
            (name, type_1, type_2, total, hp, attack, defense,
             sp_atk, sp_def, speed, generation, legendary, is_custom)
            SELECT name, type_1, type_2, total, hp, attack, defense,
                   sp_atk, sp_def, speed, generation, legendary, 1
            FROM {TABLE_NAME}
            WHERE id = ?
        """, (pokemon_id,))

        new_id = cursor.lastrowid

        _log_cheat_with_cursor(cursor, "STEAL", name, f"Stole {name} (Total: {total})")

        conn.commit()
        return f"🎯 STEAL successful! Added {name} to your team!", new_id

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()


def cheat_create_legendary(name: str = "HACKER") -> Tuple[str, int]:
    """LEGENDARY - Create custom overpowered Pokémon"""
    conn = get_connection(DB_PATH)
    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO pokemon 
            (name, type_1, type_2, total, hp, attack, defense,
             sp_atk, sp_def, speed, generation, legendary, is_custom)
            VALUES (?, 'Dragon', 'Psychic', 999, 255, 255, 255, 255, 255, 255, 0, 1, 1)
        """, (name,))

        new_id = cursor.lastrowid

        _log_cheat_with_cursor(cursor, 'LEGENDARY', name, "Created overpowered legendary Pokémon")

        conn.commit()
        return f"⚡ LEGENDARY created! {name} has joined the battle with maxed stats!", new_id
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()


def cheat_nerf_all(exclude_ids: List[int]) -> str:
    """NERF - Reduce all other Pokémon stats by 50%"""
    conn = get_connection(DB_PATH)
    try:
        cursor = conn.cursor()

        placeholders = ','.join(['?'] * len(exclude_ids))

        cursor.execute(f"""
            UPDATE pokemon
            SET hp = CAST(hp * 0.5 AS INTEGER),
                attack = CAST(attack * 0.5 AS INTEGER),
                defense = CAST(defense * 0.5 AS INTEGER),
                sp_atk = CAST(sp_atk * 0.5 AS INTEGER),
                sp_def = CAST(sp_def * 0.5 AS INTEGER),
                speed = CAST(speed * 0.5 AS INTEGER),
                total = CAST(total * 0.5 AS INTEGER)
            WHERE id NOT IN ({placeholders})
            AND is_custom = 0
        """, exclude_ids)

        rows_affected = cursor.rowcount

        _log_cheat_with_cursor(cursor, 'NERF', 'ALL_OTHERS', f"Reduced stats by 50% for {rows_affected} Pokémon")

        conn.commit()
        return f"💥 NERF applied! {rows_affected} opponent Pokémon weakened by 50%!"
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()


def cheat_max_stats(pokemon_ids: List[int]) -> str:
    """MAXPOWER - Set all stats to maximum (255)"""
    conn = get_connection(DB_PATH)
    try:
        cursor = conn.cursor()

        affected = []
        for pid in pokemon_ids:
            cursor.execute("SELECT name FROM pokemon WHERE id = ?", (pid,))
            pokemon_row = cursor.fetchone()
            cursor.execute("""
                UPDATE pokemon
                SET hp = 255, attack = 255, defense = 255,
                    sp_atk = 255, sp_def = 255, speed = 255,
                    total = 1530
                WHERE id = ?
            """, (pid,))

            if pokemon_row:
                name = pokemon_row[0]
                affected.append(name)
                _log_cheat_with_cursor(cursor, 'MAXPOWER', name, "Set all stats to 255")

        conn.commit()
        return f"💪 MAX POWER! All stats = 255 for: {', '.join(affected)}"
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()


# ============== CHEAT DETECTION ==============

def detect_cheats() -> List[Dict]:
    """Detect potential cheats by analyzing abnormal stats using pandas"""
    conn = get_connection(DB_PATH)
    
    anomalies = []
    
    # Read pokemon data into DataFrame
    df = pd.read_sql_query("""
        SELECT name, hp, attack, defense, sp_atk, sp_def, speed, total, is_custom
        FROM pokemon
    """, conn)
    
    conn.close()
    
    # Check for impossible stats (> 255) using pandas
    impossible_stats = df[
        (df['hp'] > 255) | (df['attack'] > 255) | (df['defense'] > 255) |
        (df['sp_atk'] > 255) | (df['sp_def'] > 255) | (df['speed'] > 255)
    ]
    
    for _, row in impossible_stats.iterrows():
        anomalies.append({
            'pokemon': row['name'],
            'type': 'IMPOSSIBLE_STATS',
            'details': f"Stats exceed natural maximum: HP={row['hp']}, ATK={row['attack']}, DEF={row['defense']}"
        })
    
    # Check for custom Pokémon
    custom_pokemon = df[df['is_custom'] == 1]
    
    for _, row in custom_pokemon.iterrows():
        anomalies.append({
            'pokemon': row['name'],
            'type': 'CUSTOM_POKEMON',
            'details': f"Non-original Pokémon detected (Total: {row['total']})"
        })
    
    # Check for Defense = 999 (GODMODE signature)
    godmode_pokemon = df[(df['defense'] == 999) | (df['sp_def'] == 999)]
    
    for _, row in godmode_pokemon.iterrows():
        anomalies.append({
            'pokemon': row['name'],
            'type': 'GODMODE_DETECTED',
            'details': f"Suspicious defense values: DEF={row['defense']}, SP.DEF={row['sp_def']}"
        })
    
    return anomalies


def get_cheat_log() -> List[Dict]:
    """Get all logged cheats using pandas"""
    conn = get_connection(DB_PATH)
    
    df = pd.read_sql_query("""
        SELECT cheat_code, pokemon_affected, description, timestamp
        FROM cheat_log
        ORDER BY timestamp DESC
    """, conn)
    
    conn.close()
    
    return df.to_dict('records')


def reset_database():
    """Reset database to original state (remove all cheats)"""
    if DB_PATH.exists():
        os.remove(DB_PATH)
    create_database(csv_path=CSV_PATH, db_path=DB_PATH, table_name=TABLE_NAME)
    _ensure_task3_tables()
    return "✅ Database reset successfully! All cheats removed."


def get_pokemon_stats_analysis() -> Dict:
    """Analyze Pokémon dataset for interesting insights using pandas"""
    conn = get_connection(DB_PATH)
    
    # Read pokemon data into DataFrame
    df = pd.read_sql_query(f"""
        SELECT type_1, type_2, total, hp, attack, defense, sp_atk, sp_def, speed,
               generation, name, legendary, is_custom
        FROM {TABLE_NAME}
        WHERE is_custom = 0
    """, conn)
    
    conn.close()
    
    analysis = {}
    
    # Most overpowered type combination using pandas groupby
    type_combos = df.groupby(['type_1', 'type_2']).agg({
        'total': ['count', 'mean', 'max']
    }).reset_index()
    
    # Flatten column names
    type_combos.columns = ['type_1', 'type_2', 'count', 'avg_total', 'max_total']
    
    # Filter for at least 3 Pokémon and sort by avg_total
    type_combos = type_combos[type_combos['count'] >= 3].sort_values('avg_total', ascending=False).head(5)
    
    analysis['top_type_combos'] = [
        {
            'types': f"{row['type_1']}/{row['type_2']}" if pd.notna(row['type_2']) and str(row['type_2']).strip() and str(row['type_2']).lower() != 'none' else row['type_1'],
            'count': int(row['count']),
            'avg_total': round(row['avg_total'], 2),
            'max_total': int(row['max_total'])
        }
        for _, row in type_combos.iterrows()
    ]
    
    # Power creep by generation using pandas groupby
    gen_stats = df.groupby('generation').agg({
        'total': ['count', 'mean'],
        'hp': 'mean',
        'attack': 'mean',
        'speed': 'mean'
    }).reset_index()
    
    # Flatten column names
    gen_stats.columns = ['generation', 'count', 'avg_total', 'avg_hp', 'avg_attack', 'avg_speed']
    
    analysis['generation_stats'] = [
        {
            'generation': int(row['generation']),
            'count': int(row['count']),
            'avg_total': round(row['avg_total'], 2),
            'avg_hp': round(row['avg_hp'], 2),
            'avg_attack': round(row['avg_attack'], 2),
            'avg_speed': round(row['avg_speed'], 2)
        }
        for _, row in gen_stats.iterrows()
    ]
    
    # Weakest legendary using pandas filtering and sorting
    legendaries = df[df['legendary'] == 1].sort_values('total')
    
    if len(legendaries) > 0:
        weakest = legendaries.iloc[0]
        analysis['weakest_legendary'] = {
            'name': weakest['name'],
            'total': int(weakest['total']),
            'types': f"{weakest['type_1']}/{weakest['type_2']}" if pd.notna(weakest['type_2']) and str(weakest['type_2']).strip() and str(weakest['type_2']).lower() != 'none' else weakest['type_1'],
            'generation': int(weakest['generation'])
        }
    
    return analysis

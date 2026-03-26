"""
Database setup and loading script for Baby Names Explorer.
Loads NationalNames.csv into SQLite with proper schema and indexes.
"""
import sqlite3
import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DB_PATH = BASE_DIR / 'babynames.db'
CSV_PATH = PROJECT_ROOT / 'data' / 'task1' / 'NationalNames.csv'

def create_database():
    """Create SQLite database and load data from CSV."""
    print("Starting database setup...")
    
    # Remove existing database
    if os.path.exists(DB_PATH):
        print(f"Removing existing database: {DB_PATH}")
        os.remove(DB_PATH)
    
    # Connect to database
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print(f"Loading CSV from: {CSV_PATH}")
    print("This may take a moment for 1.8M rows...")
    
    # Load CSV with pandas
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df):,} rows from CSV")
    print(f"Columns: {list(df.columns)}")
    
    # Create table with proper schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS names (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            year INTEGER NOT NULL,
            gender TEXT NOT NULL,
            count INTEGER NOT NULL
        )
    ''')
    
    # Load data into SQLite using pandas to_sql
    # Note: Using to_sql with if_exists='append' since we created the table already
    df.columns = [c.lower() for c in df.columns]  # Normalize column names
    df.to_sql('names', conn, if_exists='append', index=False)
    
    print(f"✓ Loaded {len(df):,} rows into 'names' table")
    
    # Create indexes
    print("\nCreating indexes...")
    
    # Index 1: (name, year) - Optimizes name lookup across years
    # Justification: Primary use case is showing popularity of specific names over time
    # This index allows fast retrieval of all years for a given name
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_name_year ON names(name, year)')
    print("✓ Created index on (name, year) - optimizes name popularity queries")
    
    # Index 2: (year, gender) - Optimizes year-based aggregations by gender
    # Justification: Needed for calculating total births per year/gender for percentage calculations
    # Also speeds up year range queries with gender filtering
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_year_gender ON names(year, gender)')
    print("✓ Created index on (year, gender) - optimizes yearly aggregations")
    
    # Verify indexes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='names'")
    indexes = cursor.fetchall()
    print(f"\nVerified indexes: {[idx[0] for idx in indexes]}")
    
    # Show some statistics
    cursor.execute("SELECT COUNT(*) FROM names")
    total_rows = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT name) FROM names")
    unique_names = cursor.fetchone()[0]
    
    cursor.execute("SELECT MIN(year), MAX(year) FROM names")
    min_year, max_year = cursor.fetchone()
    
    print(f"\nDatabase Statistics:")
    print(f"  Total records: {total_rows:,}")
    print(f"  Unique names: {unique_names:,}")
    print(f"  Year range: {min_year}-{max_year}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Database created successfully: {DB_PATH}")
    print("\nIndex Justifications:")
    print("1. (name, year): Speeds up queries like 'SELECT * FROM names WHERE name=? ORDER BY year'")
    print("   - Used for name popularity over time feature (primary use case)")
    print("2. (year, gender): Speeds up queries like 'SELECT year, SUM(count) FROM names WHERE year BETWEEN ? AND ? GROUP BY year, gender'")
    print("   - Used for calculating yearly totals needed for percentage calculations")

if __name__ == '__main__':
    create_database()

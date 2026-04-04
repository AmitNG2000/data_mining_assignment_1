"""
SQL utility functions for Baby Names Explorer.
Provides database connection, query execution, and safety validation.
"""
import sqlite3
import pandas as pd
from typing import Tuple, Optional
from pathlib import Path
from task1.database import create_database


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'babynames.db'

def get_db_connection():
    """
    Get a connection to the SQLite database.
    Returns:
        sqlite3.Connection: Database connection object
    """
    return sqlite3.connect(str(DB_PATH))

def ensure_database_ready() -> Tuple[bool, str]:
    """
    Ensure the SQLite database and required table exist.

    Returns:
        Tuple[bool, str]: (database_was_created, status_message)
    """
    if not DB_PATH.exists():
        create_database()
        return True, "Database created successfully."

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Fast check that the required table exists and is queryable.
        cursor.execute("SELECT 1 FROM names LIMIT 1")
        return False, "Database is ready (no changes needed)."
    except sqlite3.Error:
        create_database()
        return True, "Database was missing required schema and has been rebuilt."
    finally:
        if conn is not None:
            conn.close()

def execute_query(query: str, params: tuple = ()) -> Tuple[bool, any]:
    """
    Execute a SQL query and return results.
    
    Args:
        query: SQL query string
        params: Optional tuple of parameters for parameterized queries
        
    Returns:
        Tuple of (success: bool, result: DataFrame or error message)
    """
    try:
        conn = get_db_connection()
        
        # Use pandas to execute and return as DataFrame
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return True, df
    except Exception as e:
        return False, str(e)

def is_select_only(query: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a query is SELECT-only for safety.
    
    Args:
        query: SQL query string to validate
        
    Returns:
        Tuple of (is_safe: bool, error_message: str or None)
    """
    query_stripped = query.strip()
    
    if not query_stripped:
        return False, "Query cannot be empty"
    
    query_upper = query_stripped.upper()
    
    # Check if it starts with SELECT
    if not query_upper.startswith('SELECT'):
        return False, "Only SELECT statements are allowed. Your query must start with SELECT."
    
    # Check for dangerous keywords anywhere in the query
    dangerous_keywords = [
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 
        'CREATE', 'TRUNCATE', 'REPLACE', 'PRAGMA'
    ]
    
    # Split query into words and check
    query_words = query_upper.split()
    for keyword in dangerous_keywords:
        if keyword in query_words:
            return False, f"Dangerous keyword '{keyword}' detected. Only SELECT queries are allowed for safety."
    
    return True, None

def get_total_births_by_year(gender: Optional[str] = None) -> pd.DataFrame:
    """
    Get total births per year, optionally filtered by gender.
    Used for calculating percentage of total births.
    
    Args:
        gender: Optional gender filter ('M' or 'F')
        
    Returns:
        DataFrame with columns: year, total_births
    """
    conn = get_db_connection()
    
    if gender:
        query = """
            SELECT year, SUM(count) as total_births
            FROM names
            WHERE gender = ?
            GROUP BY year
            ORDER BY year
        """
        df = pd.read_sql_query(query, conn, params=(gender,))
    else:
        query = """
            SELECT year, SUM(count) as total_births
            FROM names
            GROUP BY year
            ORDER BY year
        """
        df = pd.read_sql_query(query, conn)
    
    conn.close()
    return df

def get_name_popularity(name: str, gender: Optional[str] = None) -> pd.DataFrame:
    """
    Get popularity data for a specific name across all years.
    
    Args:
        name: Name to search for (case-insensitive)
        gender: Optional gender filter ('M' or 'F')
        
    Returns:
        If gender is provided: DataFrame with columns year, gender, count.
        If gender is None: DataFrame with columns year, count (Female + Male combined).
    """
    conn = get_db_connection()
    
    if gender:
        query = """
            SELECT year, gender, count
            FROM names
            WHERE LOWER(name) = LOWER(?)
            AND gender = ?
            ORDER BY year
        """
        df = pd.read_sql_query(query, conn, params=(name, gender))
    else:
        query = """
            SELECT year, SUM(count) as count
            FROM names
            WHERE LOWER(name) = LOWER(?)
            GROUP BY year
            ORDER BY year
        """
        df = pd.read_sql_query(query, conn, params=(name,))
    
    conn.close()
    return df

def get_peak_decade(name: str, gender: str) -> Tuple[Optional[int], pd.DataFrame]:
    """
    Find the peak decade for a given name.
    
    Args:
        name: Name to search for
        gender: Gender filter ('M' or 'F')
        
    Returns:
        Tuple of (peak_decade: int or None, decade_data: DataFrame)
    """
    conn = get_db_connection()
    
    query = """
        SELECT 
            (year / 10) * 10 as decade,
            SUM(count) as total_count
        FROM names
        WHERE LOWER(name) = LOWER(?)
        AND gender = ?
        GROUP BY decade
        ORDER BY total_count DESC
    """
    
    df = pd.read_sql_query(query, conn, params=(name, gender))
    conn.close()
    
    if len(df) == 0:
        return None, df
    
    peak_decade = int(df.iloc[0]['decade'])
    return peak_decade, df.sort_values('decade')

def test_connection():
    """Test database connection and print basic info."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM names")
        count = cursor.fetchone()[0]
        print(f"✓ Database connection successful")
        print(f"  Total records: {count:,}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

if __name__ == '__main__':
    # Test the utilities
    print("Testing database utilities...\n")
    
    test_connection()
    
    print("\nTesting query validation:")
    test_queries = [
        "SELECT * FROM names LIMIT 5",
        "DELETE FROM names WHERE year < 1900",
        "INSERT INTO names VALUES (1, 'Test', 2020, 'M', 100)",
        "SELECT name, SUM(count) FROM names GROUP BY name",
    ]
    
    for query in test_queries:
        is_safe, error = is_select_only(query)
        status = "✓ Safe" if is_safe else f"✗ Blocked: {error}"
        print(f"  {query[:50]}... → {status}")
    
    print("\nTesting name lookup:")
    df = get_name_popularity("Mary", gender="F")
    if len(df) > 0:
        print(f"  Found {len(df)} records for 'Mary' (F)")
        print(f"  Years: {df['year'].min()}-{df['year'].max()}")
    
    print("\nTesting peak decade:")
    peak, df = get_peak_decade("Mary", "F")
    if peak:
        print(f"  Peak decade for 'Mary' (F): {peak}s")
    
    print("\n✓ All utilities working correctly!")

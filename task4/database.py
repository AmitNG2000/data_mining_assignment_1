"""
Database setup and management for SQL Learning Game.
Handles loading CSV data, creating helper tables, and database resets.
"""
import sqlite3
import pandas as pd
import os
from pathlib import Path


# Constants
TASK4_DIR = Path(__file__).parent
CSV_PATH = TASK4_DIR / "restaurant_orders.csv"
DB_PATH = TASK4_DIR / "restaurant.db"


def get_db_connection():
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allow column access by name
    return conn


def initialize_database(force_reset=False):
    """
    Initialize the database from CSV and create helper tables.
    
    Args:
        force_reset: If True, drop existing tables and recreate from scratch
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if CSV exists
        if not CSV_PATH.exists():
            raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")
        
        # Load CSV data
        df = pd.read_csv(CSV_PATH)
        
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Drop existing tables if force reset
        if force_reset:
            cursor.execute("DROP TABLE IF EXISTS orders")
            cursor.execute("DROP TABLE IF EXISTS food_items")
        
        # Create orders table with proper schema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                customer_name TEXT NOT NULL,
                food_item TEXT NOT NULL,
                category TEXT NOT NULL CHECK (category IN ('Main', 'Dessert', 'Starter')),
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                price REAL NOT NULL CHECK (price >= 0),
                payment_method TEXT NOT NULL CHECK (payment_method IN ('Cash', 'Debit Card', 'Credit Card', 'Online Payment')),
                order_time TEXT NOT NULL
            )
        """)
        
        # Load data into orders table
        df.columns = ['order_id', 'customer_name', 'food_item', 'category', 'quantity', 'price', 'payment_method', 'order_time']
        df.to_sql('orders', conn, if_exists='replace', index=False)
        
        # Create food_items helper table for JOIN exercises (Level 4)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_items (
                food_item TEXT PRIMARY KEY,
                cost_to_make REAL NOT NULL CHECK (cost_to_make >= 0),
                profit_margin REAL NOT NULL
            )
        """)
        
        # Populate food_items with realistic cost data
        food_costs = [
            ('Pizza', 3.50, 0.65),
            ('Burger', 4.00, 0.60),
            ('Pasta', 2.50, 0.70),
            ('Salad', 2.00, 0.75),
            ('Soup', 1.50, 0.80),
            ('Fries', 1.00, 0.75),
            ('Cake', 3.00, 0.70),
            ('Brownie', 2.00, 0.75),
            ('Ice Cream', 1.50, 0.70)
        ]
        
        cursor.executemany(
            "INSERT OR REPLACE INTO food_items (food_item, cost_to_make, profit_margin) VALUES (?, ?, ?)",
            food_costs
        )
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database initialized successfully: {DB_PATH}")
        print(f"   - Loaded {len(df)} orders from CSV")
        print(f"   - Created {len(food_costs)} food items for JOIN exercises")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False


def reset_database():
    """
    Reset the database to its original state by reinitializing from CSV.
    Useful when players break the database or want to retry.
    
    Returns:
        bool: True if reset successful
    """
    print("🔄 Resetting database to original state...")
    return initialize_database(force_reset=True)


def validate_database():
    """
    Validate that database has correct schema and data.
    
    Returns:
        dict: Validation results with status and messages
    """
    results = {
        'valid': False,
        'orders_count': 0,
        'food_items_count': 0,
        'messages': []
    }
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check orders table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
        if not cursor.fetchone():
            results['messages'].append("❌ 'orders' table not found")
            conn.close()
            return results
        
        # Check food_items table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='food_items'")
        if not cursor.fetchone():
            results['messages'].append("❌ 'food_items' table not found")
            conn.close()
            return results
        
        # Count rows
        cursor.execute("SELECT COUNT(*) FROM orders")
        results['orders_count'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM food_items")
        results['food_items_count'] = cursor.fetchone()[0]
        
        # Validate row counts
        if results['orders_count'] < 100:
            results['messages'].append(f"⚠️ Only {results['orders_count']} orders found (expected ~500)")
        else:
            results['messages'].append(f"✅ {results['orders_count']} orders loaded")
        
        if results['food_items_count'] < 5:
            results['messages'].append(f"⚠️ Only {results['food_items_count']} food items found")
        else:
            results['messages'].append(f"✅ {results['food_items_count']} food items configured")
        
        results['valid'] = results['orders_count'] > 0 and results['food_items_count'] > 0
        
        conn.close()
        
    except Exception as e:
        results['messages'].append(f"❌ Validation error: {e}")
    
    return results


def execute_query(query, params=None):
    """
    Execute a SQL query safely and return results as a pandas DataFrame.
    
    Args:
        query: SQL query string
        params: Optional tuple of query parameters for parameterized queries
    
    Returns:
        DataFrame: Query results, or None if error
    """
    try:
        conn = get_db_connection()
        
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        return df
        
    except Exception as e:
        print(f"Query error: {e}")
        return None


def execute_write_query(query, params=None):
    """
    Execute an INSERT, UPDATE, or DELETE query.
    Used for Level 5 sabotage challenges.
    
    Args:
        query: SQL query string
        params: Optional tuple of query parameters
    
    Returns:
        tuple: (success: bool, message: str, rows_affected: int)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return (True, f"Query executed successfully. {rows_affected} row(s) affected.", rows_affected)
        
    except Exception as e:
        return (False, f"Query error: {str(e)}", 0)


def get_table_info(table_name):
    """
    Get column information for a table.
    Useful for showing table schema to learners.
    
    Args:
        table_name: Name of the table
    
    Returns:
        list: List of (column_name, type, nullable) tuples
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"PRAGMA table_info({table_name})")
        info = cursor.fetchall()
        
        conn.close()
        
        return [(row[1], row[2], not row[3]) for row in info]
        
    except Exception as e:
        print(f"Error getting table info: {e}")
        return []


# Initialize database on module import if it doesn't exist
if not DB_PATH.exists():
    print("📦 Database not found. Initializing for first time...")
    initialize_database()

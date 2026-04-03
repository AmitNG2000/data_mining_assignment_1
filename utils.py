"""
Ensure the SQLite database and required table exist.
"""

import re
import sqlite3
from pathlib import Path
from typing import Tuple
import pandas as pd


def get_connection(db_path: str | Path) -> sqlite3.Connection:
    """Get database connection."""
    return sqlite3.connect(db_path)


def ensure_database_ready(
    db_path: str | Path,
    csv_path: str | Path,
    table_name: str | None = None
) -> Tuple[bool, str]:
    """
    Ensure the SQLite database and required table exist.

    Returns:
        Tuple[bool, str]: (database_is_ready, status_message)
    """
    csv_path = Path(csv_path)
    db_path = Path(db_path)

    if table_name is None:
        table_name = csv_path.stem

    if not db_path.exists():
        create_database(csv_path=csv_path, db_path=db_path, table_name=table_name)
        return True, "Database created successfully."

    conn = None
    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (table_name,)
        )
        table = cursor.fetchone()

        if table is None:
            conn.close()
            conn = None
            create_database(csv_path=csv_path, db_path=db_path, table_name=table_name)
            return True, f"Table '{table_name}' was missing and the database was rebuilt."

        return True, "Database is ready (no changes needed)."

    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database check failed: {e}")

    finally:
        if conn is not None:
            conn.close()


def create_database(
    csv_path: str | Path,
    db_path: str | Path | None = None,
    table_name: str | None = None
) -> None:
    """
    Create SQLite database and load data from CSV.

    Args:
        csv_path: Path to the CSV file to load.
        db_path: Path to the SQLite database file.
                 If None, it will be created with the same name as the CSV
                 but with a .db extension.
        table_name: Name of the table to create.
                    If None, it will be derived from the CSV file name.
    """
    csv_path = Path(csv_path)

    if db_path is None:
        db_path = csv_path.with_suffix(".db")
    else:
        db_path = Path(db_path)

    if table_name is None:
        table_name = csv_path.stem

    df = pd.read_csv(csv_path)

    # Normalize column names
    df.columns = normalize_column_names(df.columns)

    conn = get_connection(db_path)
    try:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    finally:
        conn.close()

    print(f"Created DB: {db_path}")
    print(f"Table name: {table_name}")


def normalize_column_names(columns):
    cleaned = []
    for col in columns:
        col = col.lower().strip()
        col = re.sub(r"[^a-z0-9]+", "_", col)
        col = re.sub(r"_+", "_", col).strip("_")
        
            
        cleaned.append(col)
    
    return cleaned
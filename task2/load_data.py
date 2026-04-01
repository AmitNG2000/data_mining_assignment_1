"""
Data loader script for Oscar Awards dataset
Loads data from CSV into SQLite using PonyORM
"""
from pathlib import Path

import pandas as pd

from task2.database import (
        setup_database, db, Person, Film, Category, Nomination,
        get_or_create_person, get_or_create_film, get_or_create_category
    )

from pony.orm import db_session, commit
import sys


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DB_NAME = 'oscars.db'
DB_PATH = BASE_DIR / DB_NAME
CSV_PATH = PROJECT_ROOT / 'task2' / 'oscar_awards_full_data.csv'


def clean_name(name):
    """Clean person/film name"""
    if pd.isna(name):
        return None
    return str(name).strip()


def parse_winner(value):
    """Parse winner column to boolean"""
    if pd.isna(value):
        return False
    if str(value).strip().lower() == 'true':
        return True
    return False


def load_oscar_data(csv_path = CSV_PATH, db_path = DB_PATH):
    """
    Load Oscar awards data from CSV into database
    
    Args:
        csv_path: Path to oscar_awards_full_data.csv
        db_path: Path to SQLite database file
    """
    csv_path = str(csv_path)
    db_path = str(db_path)

    print(f"Loading data from {csv_path}...")
    
    # Read CSV with tab separator
    df = pd.read_csv(csv_path, sep='\t', on_bad_lines='skip')
    print(f"Loaded {len(df)} rows from CSV")
    
    # Setup database
    setup_database(db_path, create_db=True)
    
    # Load data in batches for better performance
    batch_size = 500
    total_rows = len(df)
    
    with db_session:
        for idx, row in df.iterrows():
            # Progress indicator
            if (idx + 1) % batch_size == 0:
                commit()
                print(f"Processed {idx + 1}/{total_rows} rows ({((idx+1)/total_rows*100):.1f}%)")
            
            # Extract data from row
            ceremony = int(row['Ceremony']) if not pd.isna(row['Ceremony']) else 0
            year = clean_name(row['Year'])
            class_name = clean_name(row['Class'])
            category_name = clean_name(row['Category'])
            canonical_category = clean_name(row['CanonicalCategory'])
            
            person_name = clean_name(row['Name'])
            if not person_name:
                continue  # Skip rows without person name
            
            person_imdb = clean_name(row['NomineeIds'])
            
            film_title = clean_name(row['Film'])
            film_imdb = clean_name(row['FilmId'])
            
            is_winner = parse_winner(row['Winner'])
            detail = clean_name(row['Detail'])
            note = clean_name(row['Note'])
            multifilm = parse_winner(row['MultifilmNomination'])
            
            # Get or create entities
            person = get_or_create_person(person_name, person_imdb)
            category = get_or_create_category(category_name, class_name, canonical_category)
            
            # Film is optional
            film = None
            if film_title:
                film = get_or_create_film(film_title, film_imdb, year)
            
            # Create nomination
            nomination = Nomination(
                ceremony=ceremony,
                year=year,
                person=person,
                film=film,
                category=category,
                is_winner=is_winner,
                detail=detail,
                note=note,
                multifilm_nomination=multifilm
            )
        
        # Final commit
        commit()
    
    # Print statistics
    with db_session:
        total_persons = Person.select().count()
        total_films = Film.select().count()
        total_categories = Category.select().count()
        total_nominations = Nomination.select().count()
        
        print(f"\n✓ Data loading complete!")
        print(f"  Persons: {total_persons:,}")
        print(f"  Films: {total_films:,}")
        print(f"  Categories: {total_categories:,}")
        print(f"  Nominations: {total_nominations:,}")


if __name__ == "__main__":
    csv_path = "../data/task2/oscar_awards_full_data.csv"
    db_path = "oscars.db"
    
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    if len(sys.argv) > 2:
        db_path = sys.argv[2]
    
    load_oscar_data(csv_path, db_path)

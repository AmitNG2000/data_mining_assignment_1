"""
Oscar Awards Database ORM using PonyORM
"""
from pathlib import Path
from pony.orm import Database, Required, Optional, Set, PrimaryKey, db_session, select
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DB_NAME = 'oscars.db'
DB_PATH = BASE_DIR / DB_NAME
CSV_PATH = PROJECT_ROOT / 'task2' / 'oscar_awards_full_data.csv'

db = Database()


class Person(db.Entity):
    """Represents an actor, actress, or director nominated for an Oscar"""
    _table_ = 'persons'
    
    id = PrimaryKey(int, auto=True)
    name = Required(str, index=True)
    imdb_id = Optional(str)  # IMDB nominee ID (e.g., nm0001932)
    
    nominations = Set('Nomination')
    
    def __repr__(self):
        return f"Person(name='{self.name}')"


class Film(db.Entity):
    """Represents a film nominated for an Oscar"""
    _table_ = 'films'
    
    id = PrimaryKey(int, auto=True)
    title = Required(str, index=True)
    imdb_id = Optional(str)  # IMDB film ID (e.g., tt0019217)
    year = Optional(str)  # Year can be like "1927/28"
    
    nominations = Set('Nomination')
    
    def __repr__(self):
        return f"Film(title='{self.title}', year='{self.year}')"


class Category(db.Entity):
    """Represents an Oscar award category"""
    _table_ = 'categories'
    
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)  # e.g., "ACTOR IN A LEADING ROLE"
    class_name = Optional(str)  # e.g., "Acting"
    canonical_category = Optional(str)  # e.g., "ACTOR"
    
    nominations = Set('Nomination')
    
    def __repr__(self):
        return f"Category(name='{self.name}')"


class Nomination(db.Entity):
    """Represents a single Oscar nomination"""
    _table_ = 'nominations'
    
    id = PrimaryKey(int, auto=True)
    ceremony = Required(int)  # Ceremony number (1, 2, 3, ...)
    year = Required(str)  # Year like "1927/28"
    
    person = Required(Person)
    film = Optional(Film)  # Optional because some categories don't have films
    category = Required(Category)
    
    is_winner = Required(bool, default=False)
    
    # Additional details
    detail = Optional(str, nullable=True)  # Additional detail about the nomination
    note = Optional(str, nullable=True)
    multifilm_nomination = Required(bool, default=False)
    
    def __repr__(self):
        win_str = "WON" if self.is_winner else "NOMINATED"
        return f"Nomination({self.person.name}, {self.category.name}, {self.year}, {win_str})"


def setup_database(filename=DB_NAME, create_db=True):
    """
    Set up the database connection and create tables
    
    Args:
        filename: SQLite database filename
        create_db: Whether to create the database if it doesn't exist
    """
    # Streamlit reruns can call setup multiple times in one process.
    # Bind and map only once to avoid Pony's "already bound" error.
    if db.provider is None:
        db.bind(provider='sqlite', filename=str(filename), create_db=create_db)

    if db.schema is None:
        db.generate_mapping(create_tables=True)

    return db


def get_or_create_person(name, imdb_id=None):
    """Get existing person or create new one"""
    if not name:
        return None
        
    # Clean imdb_id - convert empty string to None
    if imdb_id == '' or imdb_id == 'None':
        imdb_id = None
        
    if imdb_id:
        person = Person.get(imdb_id=imdb_id)
        if person:
            return person
    
    person = Person.get(name=name)
    if person:
        if imdb_id and not person.imdb_id:
            person.imdb_id = imdb_id
        return person
    
    # Create new person, only pass imdb_id if it's not None
    if imdb_id:
        return Person(name=name, imdb_id=imdb_id)
    else:
        return Person(name=name)


def get_or_create_film(title, imdb_id=None, year=None):
    """Get existing film or create new one"""
    if not title:
        return None
        
    # Clean imdb_id - convert empty string to None
    if imdb_id == '' or imdb_id == 'None':
        imdb_id = None
    if year == '' or year == 'None':
        year = None
        
    if imdb_id:
        film = Film.get(imdb_id=imdb_id)
        if film:
            return film
    
    film = Film.get(title=title, year=year)
    if film:
        if imdb_id and not film.imdb_id:
            film.imdb_id = imdb_id
        return film
    
    # Create new film, only pass optional fields if not None
    kwargs = {'title': title}
    if imdb_id:
        kwargs['imdb_id'] = imdb_id
    if year:
        kwargs['year'] = year
    return Film(**kwargs)


def get_or_create_category(name, class_name=None, canonical_category=None):
    """Get existing category or create new one"""
    category = Category.get(name=name)
    if category:
        return category
    
    return Category(name=name, class_name=class_name, canonical_category=canonical_category)


if __name__ == "__main__":
    # Test the database setup
    setup_database('test_oscars.db')
    
    with db_session:
        # Create test data
        person = Person(name="Test Actor", imdb_id="nm0000001")
        category = Category(name="ACTOR IN A LEADING ROLE", class_name="Acting")
        film = Film(title="Test Movie", imdb_id="tt0000001", year="2020")
        nomination = Nomination(
            ceremony=92,
            year="2020",
            person=person,
            film=film,
            category=category,
            is_winner=True
        )
        
        # Immediate queries in same session
        print(f"Created person: {person.name}")
        print(f"Created category: {category.name}")
        print(f"Created film: {film.title}")
        print(f"Created nomination: ceremony {nomination.ceremony}, winner={nomination.is_winner}")
        
        total_persons = Person.select().count()
        total_noms = Nomination.select().count()
        print(f"\nTotal persons: {total_persons}")
        print(f"Total nominations: {total_noms}")
    
    print("✓ Database schema test successful!")

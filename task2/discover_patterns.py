"""
Pattern Discovery for Oscar Awards
Find interesting patterns in the Oscar database
"""
import sys
import io
# Fix Windows encoding for emojis
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from database import setup_database, db, Person, Film, Category, Nomination
from pony.orm import db_session
import pandas as pd

# Setup database
setup_database('oscars.db', create_db=False)

print("=" * 80)
print("OSCAR AWARDS PATTERN DISCOVERY")
print("=" * 80)

# Pattern 1: Actors with Most Nominations but Zero Wins
print("\n📊 PATTERN 1: Most Nominations Without a Win")
print("-" * 80)

with db_session:
    # Use direct SQL to avoid lambda expression issues
    query = """
        SELECT 
            p.id,
            p.name,
            COUNT(n.id) as total_noms,
            SUM(CASE WHEN n.is_winner = 1 THEN 1 ELSE 0 END) as total_wins
        FROM persons p
        JOIN nominations n ON n.person = p.id
        GROUP BY p.id, p.name
        HAVING total_noms >= 3 AND total_wins = 0
        ORDER BY total_noms DESC
        LIMIT 10
    """
    
    results = list(db.execute(query))
    no_win_stats = []
    
    for row in results:
        person_id, name, total_noms, total_wins = row
        
        # Get categories and years - use string interpolation
        cat_query = f"""
            SELECT DISTINCT c.name, n.year
            FROM nominations n
            JOIN categories c ON n.category = c.id
            WHERE n.person = {person_id}
            ORDER BY n.year
        """
        
        cat_results = list(db.execute(cat_query))
        categories = []
        years = []
        for cat_row in cat_results:
            if cat_row[0] not in categories:
                categories.append(cat_row[0])
            if cat_row[1] not in years:
                years.append(cat_row[1])
        
        no_win_stats.append({
            'Name': name,
            'Nominations': int(total_noms),
            'Categories': ', '.join(categories)[:50],
            'Years': f"{years[0]} - {years[-1]}" if len(years) > 1 else years[0]
        })
    
    df = pd.DataFrame(no_win_stats)
    print(df.to_string(index=False))
    
    print(f"\n💡 Interpretation: These {len(no_win_stats)} actors/actresses have been nominated")
    print("   multiple times but have never won. This shows the competitive nature")
    print("   of certain categories and how some performers are consistently recognized")
    print("   but face tough competition.")

# Pattern 2: Longest Gap Between First Nomination and First Win
print("\n\n📊 PATTERN 2: Longest Wait from First Nomination to First Win")
print("-" * 80)

with db_session:
    query = """
        WITH person_stats AS (
            SELECT 
                p.id as person_id,
                p.name,
                MIN(CASE WHEN n.is_winner = 0 THEN n.ceremony ELSE NULL END) as first_nom_ceremony,
                MIN(n.ceremony) as absolute_first,
                MIN(CASE WHEN n.is_winner = 1 THEN n.ceremony ELSE NULL END) as first_win_ceremony,
                COUNT(CASE WHEN n.is_winner = 1 THEN 1 END) as total_wins
            FROM persons p
            JOIN nominations n ON n.person = p.id
            GROUP BY p.id, p.name
            HAVING total_wins > 0
        )
        SELECT 
            person_id,
            name,
            absolute_first,
            first_win_ceremony,
            (first_win_ceremony - absolute_first) as gap,
            total_wins
        FROM person_stats
        WHERE gap > 0
        ORDER BY gap DESC
        LIMIT 10
    """
    
    results = list(db.execute(query))
    wait_stats = []
    
    for row in results:
        person_id, name, first_nom, first_win, gap, total_wins = row
        
        # Get details of first nomination and first win
        first_nom_query = f"""
            SELECT n.year, c.name
            FROM nominations n
            JOIN categories c ON n.category = c.id
            WHERE n.person = {person_id} AND n.ceremony = {first_nom}
            LIMIT 1
        """
        first_nom_details = list(db.execute(first_nom_query))
        first_nom_details = first_nom_details[0] if first_nom_details else None
        
        first_win_query = f"""
            SELECT n.year, c.name
            FROM nominations n
            JOIN categories c ON n.category = c.id
            WHERE n.person = {person_id} AND n.ceremony = {first_win} AND n.is_winner = 1
            LIMIT 1
        """
        first_win_details = list(db.execute(first_win_query))
        first_win_details = first_win_details[0] if first_win_details else None
        
        wait_stats.append({
            'Name': name,
            'First Nomination': f"{first_nom_details[0]} ({first_nom_details[1][:30]})" if first_nom_details else f"Ceremony {first_nom}",
            'First Win': f"{first_win_details[0]} ({first_win_details[1][:30]})" if first_win_details else f"Ceremony {first_win}",
            'Ceremonies Gap': int(gap),
            'Total Wins': int(total_wins)
        })
    
    df = pd.DataFrame(wait_stats)
    print(df.to_string(index=False))
    
    print(f"\n💡 Interpretation: These individuals waited the longest between their first")
    print("   nomination and eventual win. This demonstrates perseverance and shows that")
    print("   talent is eventually recognized, even if it takes multiple ceremonies.")

# Pattern 3: People Nominated in Multiple Different Classes
print("\n\n📊 PATTERN 3: Multi-Talented (Nominated Across Different Classes)")
print("-" * 80)

with db_session:
    query = """
        SELECT 
            p.id as person_id,
            p.name,
            COUNT(DISTINCT c.class_name) as num_classes,
            COUNT(DISTINCT c.canonical_category) as num_categories,
            COUNT(n.id) as total_noms,
            SUM(CASE WHEN n.is_winner = 1 THEN 1 ELSE 0 END) as total_wins,
            GROUP_CONCAT(DISTINCT c.class_name) as classes
        FROM persons p
        JOIN nominations n ON n.person = p.id
        JOIN categories c ON n.category = c.id
        WHERE c.class_name IS NOT NULL
        GROUP BY p.id, p.name
        HAVING num_classes >= 2
        ORDER BY num_categories DESC, total_noms DESC
        LIMIT 15
    """
    
    results = list(db.execute(query))
    multi_class_stats = []
    
    for row in results:
        person_id, name, num_classes, num_categories, total_noms, total_wins, classes = row
        
        multi_class_stats.append({
            'Name': name,
            'Classes': classes if classes else 'N/A',
            'Different Categories': int(num_categories),
            'Total Nominations': int(total_noms),
            'Total Wins': int(total_wins)
        })
    
    df = pd.DataFrame(multi_class_stats)
    print(df.to_string(index=False))
    
    print(f"\n💡 Interpretation: These individuals have been nominated across multiple")
    print("   classes (e.g., Acting, Directing, Production), demonstrating exceptional")
    print("   versatility in the film industry. Directors who also act, actors who")
    print("   produce, etc. represent the multi-talented renaissance artists of cinema.")

# Additional Pattern 4: Category with Most Unique Winners (Hardest to Predict)
print("\n\n📊 BONUS PATTERN: Most Competitive Categories (Unique Winners vs Nominations)")
print("-" * 80)

with db_session:
    query = """
        SELECT 
            c.id as category_id,
            c.name,
            COUNT(n.id) as total_noms,
            COUNT(DISTINCT n.person) as unique_nominees,
            COUNT(DISTINCT CASE WHEN n.is_winner = 1 THEN n.person END) as unique_winners,
            COUNT(DISTINCT n.ceremony) as total_ceremonies
        FROM categories c
        JOIN nominations n ON n.category = c.id
        GROUP BY c.id, c.name
        HAVING total_noms >= 20
        ORDER BY (CAST(unique_winners AS FLOAT) / unique_nominees) ASC
        LIMIT 10
    """
    
    results = list(db.execute(query))
    category_stats = []
    
    for row in results:
        cat_id, name, total_noms, unique_nominees, unique_winners, total_ceremonies = row
        
        win_concentration = (unique_winners / unique_nominees * 100) if unique_nominees > 0 else 0
        
        category_stats.append({
            'Category': name[:40],
            'Total Nominations': int(total_noms),
            'Unique Nominees': int(unique_nominees),
            'Unique Winners': int(unique_winners),
            'Win Concentration': f"{win_concentration:.1f}%",
            'Ceremonies': int(total_ceremonies)
        })
    
    df = pd.DataFrame(category_stats)
    print(df.to_string(index=False))
    
    print(f"\n💡 Interpretation: Categories with lower 'Win Concentration' have many unique")
    print("   winners relative to their nominees, making them harder to predict. Categories")
    print("   with higher concentration often have repeat winners or dominant performers.")

print("\n" + "=" * 80)
print("Pattern discovery complete!")
print("=" * 80)

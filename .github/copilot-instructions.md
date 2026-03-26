# Copilot Instructions: Data Mining Assignment 1

## Project Overview

This is a university data mining course assignment focused on SQL, ORMs, and interactive data analysis applications. The project consists of 4 tasks:

1. **Baby Names Explorer** - SQLite-based interactive name popularity analysis
2. **Oscar Actor Explorer** - ORM-based (PonyORM/SQLAlchemy/Peewee) actor profile app with Wikipedia integration
3. **Pokémon Battle Arena** - Database-driven battle game with cheat code system
4. **SQL Learning Game** - Interactive platform teaching SQL to beginners

## Key Assignment Requirements

### LLM Usage Policy
- **Code**: LLM assistance is explicitly encouraged for code generation
- **Explanations**: Each task requires a written explanation **without LLM assistance** covering:
  - What was built and how it works
  - Technology/library choices and rationale
  - Challenges encountered and solutions
- **Understanding**: The student must be able to explain the solution in person

### Submission Requirements
Each task needs:
- Deployed app (Streamlit Cloud/HuggingFace Spaces/etc.) OR notebook OR screen recording
- Written report (PDF/markdown, 1-2 pages) with personal explanations and findings
- Code in repository with README and screenshots

## Database & Schema Conventions

### Task 1: Baby Names (SQLite)
- **Required**: Use `sqlite3` Python package (raw SQL)
- **Schema**: `NationalNames.csv` → SQLite table with columns: `Id`, `Name`, `Year`, `Gender`, `Count`
- **Indexes**: Must create at least 2 indexes with justification (explain which queries they optimize)
- **Safety**: Only allow SELECT statements in custom query panel

### Task 2: Oscar Actors (ORM Required)
- **Required**: Use PonyORM, SQLAlchemy, or Peewee - **NO raw SQL**
- **Schema**: Define proper entity/model classes with types, relationships, constraints
- **External API**: Integrate Wikipedia API or `wikipedia` Python package for live data

### Task 3: Pokémon (SQLite or ORM)
- **Required**: All Pokémon stats from database - no hardcoded values
- **Schema**: Core table with Name, Type1, Type2, HP, Attack, Defense, Sp.Atk, Sp.Def, Speed, Generation, Legendary
- **Cheat System**: Each cheat must execute real SQL/ORM write operations (INSERT/UPDATE/DELETE), not just in-memory changes
- **Audit Trail**: Must be able to detect cheats via SQL queries (e.g., stats exceeding natural maximums)

## Technology Stack Recommendations

### Interactive Apps
Choose one framework per task:
- Streamlit (recommended for rapid prototyping and deployment)
- Gradio (good for ML-style interfaces)
- Panel (Holoviz ecosystem integration)
- Dash (Plotly-based, more customizable)
- ipywidgets (Jupyter notebook integration)

### ORM Options (Task 2)
- **PonyORM**: Pythonic, generator-based queries, built-in ER diagram
- **SQLAlchemy**: Industry standard, most powerful, steeper learning curve
- **Peewee**: Lightweight, Django-inspired, simple API

### Visualization
- Plotly Express (interactive charts for Streamlit/Dash)
- Matplotlib/Seaborn (static plots)
- Altair (declarative visualization, works well with Streamlit)

## Running the Project

### Python Version
Python 3.14.2 (use `py` launcher on Windows)

### Database Access
```python
import sqlite3

# Connect to database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Execute queries
cursor.execute("SELECT ...")
results = cursor.fetchall()

# Always close
conn.close()
```

### PDF Extraction
To read `HW1_instructions.pdf`:
```bash
py -m pip install pypdf
py extract_pdf.py
```

## Data Files

- **NationalNames.csv**: ~1.8M rows of US baby name data (Id, Name, Year, Gender, Count)
- **HW1_instructions.pdf**: Full assignment requirements (use `extract_pdf.py` to read)

## Task-Specific Guidelines

### Task 1: Baby Names
**Required Features:**
- Name popularity over time (line charts)
- Toggle between raw count and percentage of total births
- Custom SQL query panel with 3+ pre-built examples
- Safety validation (SELECT-only)
- One additional creative visualization
- Report 3 interesting patterns with queries and interpretation

**Index Strategy Examples:**
- Index on `(Name, Year)` → speeds up name lookup across years
- Index on `(Year, Gender)` → optimizes year-based aggregations by gender

### Task 2: Oscar Actors
**Required Features:**
- Actor profile card combining:
  - Dataset: nominations, wins, categories, years active, films
  - Wikipedia: biography, birth date, photo
  - Computed: win rate, comparison to average, years to first win
- Handle edge cases: not found, ambiguous matches, zero wins

**Pattern Discovery Examples:**
- Most nominations without wins
- Longest gap between first nomination and first win
- Directors also nominated as actors

### Task 3: Pokémon Battle
**Required Features:**
- Team selection (1-3 Pokémon from database)
- Battle mechanics from database stats (Speed → turn order, Attack/Defense → damage)
- Type effectiveness system (stored in database)
- Battle log with detailed turn info
- Win condition (HP ≤ 0)

**Cheat Code Requirements:**
- Each cheat = real database modification
- Examples: UPUPDOWNDOWN (double HP), GODMODE (999 Defense), STEAL (copy opponent Pokémon)
- Must include audit query to detect cheating

### Task 4: SQL Learning Game
**Required Features:**
- Real SQLite database with preloaded dataset
- Interactive SQL input that executes real queries
- 5+ progressive levels (SELECT * → WHERE → ORDER BY → GROUP BY → JOIN)
- Helpful feedback system (not just "incorrect")
- Progress tracking

**Creativity Points:**
- Story-driven gameplay (detective, wizard, space explorer)
- Gamification (points, badges, leaderboard)
- Visual query explanations
- AI-powered hints
- Multiplayer/competitive modes

## Common Patterns

### SQL Safety Validation
```python
def is_select_only(query: str) -> bool:
    """Only allow SELECT statements, block INSERT/UPDATE/DELETE/DROP"""
    query_upper = query.strip().upper()
    dangerous_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE']
    return query_upper.startswith('SELECT') and not any(kw in query_upper.split() for kw in dangerous_keywords)
```

### ORM Entity Example (PonyORM)
```python
from pony.orm import Database, Required, Optional, Set

db = Database()

class Actor(db.Entity):
    name = Required(str, index=True)
    nominations = Set('Nomination')
    wins = Set('Win')
    
db.bind(provider='sqlite', filename='oscars.db', create_db=True)
db.generate_mapping(create_tables=True)
```

### Streamlit Deployment
```bash
# requirements.txt must include all dependencies
streamlit run app.py

# Deploy to Streamlit Cloud (push to GitHub first)
# Visit share.streamlit.io
```

## Testing & Validation

### Check Database Integrity
```python
# Verify all Pokémon stats come from database, not hardcoded
cursor.execute("SELECT * FROM pokemon WHERE name = ?", (pokemon_name,))
stats = cursor.fetchone()  # Must exist for all Pokémon used
```

### Validate SQL Safety
```python
# Test that dangerous queries are blocked
dangerous_queries = [
    "DROP TABLE users",
    "DELETE FROM names",
    "INSERT INTO names VALUES (...)"
]
# All should return error messages, not execute
```

## Anti-Patterns to Avoid

❌ Hardcoding Pokémon stats in Python dictionaries instead of reading from database  
❌ Using raw SQL for Task 2 (ORM required)  
❌ Not handling edge cases (actor not found, ambiguous Wikipedia results)  
❌ Allowing SQL injection or non-SELECT queries in custom query panels  
❌ Creating cheat codes that only modify Python variables, not the database  
❌ Writing the assignment explanations with LLM (must be in your own words)

## Explanation Writing Tips

When writing task explanations (without LLM):
1. **What you built**: Describe the app features and user flow
2. **Technology choices**: Why you picked Streamlit over Dash, or SQLAlchemy over PonyORM
3. **Challenges & solutions**: Real problems you encountered (e.g., "Wikipedia API returned ambiguous results for 'Michael Jordan' - solved by adding disambiguation logic")
4. **Personal insights**: What you learned, what surprised you in the data

## Resources

- SQLite documentation: https://www.sqlite.org/docs.html
- Streamlit docs: https://docs.streamlit.io
- PonyORM docs: https://docs.ponyorm.org
- Wikipedia API: https://pypi.org/project/wikipedia/

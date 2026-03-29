# Task 2: Oscar Actor Explorer 🎬

## Overview
An interactive web application that explores Oscar nominations and wins, combining database-driven insights with live Wikipedia data. Built with PonyORM, Streamlit, and the Wikipedia API.

**Live App:** [View on Streamlit Cloud](#) _(Link after deployment)_

## Features

### ✨ Actor Profile Search
- Search by actor/actress name with fuzzy matching
- Click example names for quick access
- Comprehensive profile cards with:
  - **Database Stats**: Nominations, wins, win rate, categories, years active
  - **Wikipedia Integration**: Biography, photo, birth date
  - **Computed Metrics**: Win rate comparison, years to first win
  
### 💡 "Did You Know?" Auto-Facts
Automatically generates interesting facts for each actor:
- Percentile ranking among all nominees
- Win rate comparisons
- Career span highlights
- Recognition of rare achievements (first-time wins, long waits, etc.)

### 📊 Pattern Discovery
Three major patterns discovered in Oscar history:
1. **Most Nominations Without a Win** - Competitive categories analysis
2. **Longest Wait from Nomination to Win** - Perseverance stories
3. **Multi-Talented Individuals** - Cross-category nominations
4. **BONUS: Most Competitive Categories** - Predictability analysis

## Technology Stack

### ORM: PonyORM
**Why PonyORM?**
- Pythonic query syntax with generator expressions
- Cleaner code than raw SQL while maintaining ORM benefits
- Built-in debugging and query optimization
- Easier to learn than SQLAlchemy for this use case
- Good performance for datasets of this size (~12K nominations)

**Alternatives Considered:**
- SQLAlchemy: More powerful but steeper learning curve, overkill for this project
- Peewee: Simpler but less feature-rich, missing some query optimization features

### Framework: Streamlit
- Rapid prototyping for data apps
- Built-in widgets and layouts
- Easy deployment to Streamlit Cloud
- Already familiar from Task 1

### External API: Wikipedia Python Package
- Simple, well-documented API
- Handles search, summaries, and images automatically
- Built-in disambiguation handling

## Database Schema

### Entities
1. **Person** - `id`, `name`, `imdb_id`
2. **Film** - `id`, `title`, `imdb_id`, `year`
3. **Category** - `id`, `name`, `class_name`, `canonical_category`
4. **Nomination** - `id`, `ceremony`, `year`, `person`, `film`, `category`, `is_winner`, `detail`, `note`, `multifilm_nomination`

### Relationships
- `Person.nominations` → `Set[Nomination]`
- `Film.nominations` → `Set[Nomination]`
- `Category.nominations` → `Set[Nomination]`
- `Nomination.person` → `Person` (many-to-one)
- `Nomination.film` → `Optional[Film]` (many-to-one)
- `Nomination.category` → `Category` (many-to-one)

## Setup Instructions

### Prerequisites
- Python 3.8+ (tested on Python 3.14)
- pip package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd task2

# Install dependencies
pip install pony wikipedia streamlit pandas

# Load data into database (first time only)
python load_data.py

# Run the Streamlit app
streamlit run app.py
```

### Dataset
- **Source**: `../data/task2/oscar_awards_full_data.csv`
- **Size**: 12,014 nominations
- **Format**: Tab-separated CSV
- **Columns**: Ceremony, Year, Class, Category, Name, Film, Winner, etc.

## Usage

### Running Locally
```bash
streamlit run app.py
```
The app will open in your default browser at `http://localhost:8501`

### Using the App
1. Enter an actor name in the sidebar search box
2. Click "Search" or select an example name
3. View the comprehensive profile including:
   - "Did You Know?" fun facts
   - Oscar statistics
   - Wikipedia biography
   - Complete list of films and nominations

### Running Pattern Discovery
```bash
python discover_patterns.py
```
Outputs 4 patterns with interpretations to the console.

## Key Files

- `app.py` - Main Streamlit application
- `database.py` - PonyORM entity definitions and schema
- `load_data.py` - CSV data loader
- `discover_patterns.py` - Pattern discovery analysis
- `oscars.db` - SQLite database (generated after loading data)
- `README.md` - This file

## Challenges & Solutions

### Challenge 1: Python 3.14 Compatibility
**Problem**: PonyORM's lambda-based query syntax failed with Python 3.14 due to new bytecode operations (`LOAD_FAST_BORROW`).

**Solution**: Switched to direct SQL queries using `db.execute()` for pattern discovery. This actually improved performance and made queries more explicit. For the app, used simpler ORM queries without complex lambda expressions.

### Challenge 2: Name Matching
**Problem**: Actor names vary in format (e.g., "Streep, Meryl" vs "Meryl Streep") and Wikipedia searches can return ambiguous results.

**Solution**: 
- Database: Fuzzy matching with case-insensitive substring search
- Wikipedia: Try "(actor)" suffix on disambiguation errors, graceful fallback handling

### Challenge 3: Optional Fields and NULL Values
**Problem**: PonyORM's `Optional` fields still rejected `None` values without explicit `nullable=True`.

**Solution**: Updated entity definitions with `nullable=True` for truly optional fields like `detail`, `note`, `imdb_id`.

### Challenge 4: Unicode Emojis on Windows
**Problem**: Console output with emojis crashed on Windows with cp1252 encoding.

**Solution**: Wrapped stdout with UTF-8 encoding:
```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## Interesting Findings

### Pattern 1: Most Nominations Without a Win
- **Top**: Alex North (14 nominations, 0 wins - music composer)
- **Insight**: Demonstrates extreme competition in technical categories
- **Notable**: Glenn Close (8 nominations, 0 wins) - highest among actors

### Pattern 2: Longest Wait to Win
- **Top**: Brazil (62 ceremonies from 1962 to 2024!)
- **Actors**: Henry Fonda (41 ceremonies), Debbie Reynolds (51 ceremonies)
- **Insight**: Talent recognized eventually, but timing and luck matter

### Pattern 3: Multi-Talented
- **Top**: Kenneth Branagh (Acting, Directing, Writing nominations)
- **Studios**: MGM, Paramount had nominations across 10+ categories
- **Insight**: True renaissance artists of cinema are rare

### Bonus: Most Competitive Categories
- **Least Predictable**: Music (Drama Picture) - 6.7% win concentration
- **Most Predictable**: Writing categories tend toward repeat winners
- **Insight**: Technical categories have more variety in winners

## Statistics
- **6,582 unique persons** in Oscar history
- **5,194 unique films** nominated
- **109 different categories** over time
- **10,829 valid nominations** loaded (some excluded for missing data)
- **Win rate**: ~15% average across all nominees

## Future Enhancements
- Add historical trends visualization (nominations per decade)
- Implement category-specific comparisons
- Add film-centric search (instead of just actors)
- Include age at first nomination/win data
- Create interactive network graph of collaborations

## License
Educational project for Data Mining course - not for commercial use.

## Author
Created for Data Mining Assignment 1, Task 2
Course: The Art of Analyzing Big Data - The Data Scientist's Toolbox

---

**Note**: This README explains the technical implementation. A separate report with personal insights (without LLM assistance) is included in the submission as required by the assignment guidelines.

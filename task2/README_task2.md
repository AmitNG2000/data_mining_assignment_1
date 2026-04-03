# Task 2: Oscar Actor Explorer 🎬

## Overview
An interactive web application that explores Oscar nominations and wins, combining insights with Wikipedia data. Built with PonyORM, Streamlit, and the Wikipedia API.


**Note**: See the [main README](../README.md) for installation instructions and more detailes.


## Features

### Actor Profile Search + Interesting Finds
- Search by actor/actress name
- Click example names for quick access
- Comprehensive profile cards with:
  - **Database Stats**: Nominations, wins, win rate, categories, years active
  - **Wikipedia Integration**: Biography and photo
  - **Computed Metrics**: Win rate comparison, years to first win
  
### Did You Know?
Automatically generates interesting facts for each actor:
- Percentile ranking among all nominees
- Win rate comparisons
- Career span 
- Recognition of rare achievements

### Pattern Discovery
Patterns discovered in Oscar history:
1. **Most Nominations Without a Win**
2. **Longest Wait from Nomination to Win**
3. **Multi Category Individuals**
4. **Most Competitive Categories** 


## Technology Stack

### ORM: PonyORM
**Why PonyORM?**
- Clean and simple.
- Easy to learn. 
- Good integration with `Pytone` and `streamlit`.
- Good performance for datasets of this size.

**Alternatives Considered:**
- SQLAlchemy: More powerful but steeper learning curve, overkill for this project
- Peewee: Simpler but less feature-rich, missing some query optimization features


### External API: Wikipedia Python Package
- Simple, well-documented API
- Handles search, summaries, and images automatically


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



### Dataset
- **Source**: `oscar_awards_full_data.csv`
- **Size**: 12,014 nominations
- **Format**: Tab-separated CSV
- **Columns**: Ceremony, Year, Class, Category, Name, Film, Winner, etc.
# Task 1: Baby Names Explorer 👶

An interactive web application for exploring US baby name trends from 1880-2014.

> **Note**: This task is part of a multi-page Streamlit app. See the [main README](../README.md) for installation instructions.

## Quick Start

From the project root:
```bash
# One-time setup: Create database
cd task1
python database.py
cd ..

# Run the multi-page app
streamlit run app.py
```

Then navigate to **"Baby Names Explorer"** in the sidebar.

---

### 📈 Name Popularity Over Time
- Search for one or multiple names (comma-separated)
- Interactive line charts showing popularity trends
- Toggle between raw counts and percentage of total births
- Filter by gender (Male, Female, or Both)
- Summary statistics for each name

### 🔍 Custom SQL Query Panel
- Write and execute custom SELECT queries
- Built-in safety validation (only SELECT statements allowed)
- 3 pre-built example queries:
  - Top 10 names in 2010
  - Gender-neutral names (similar counts for M/F)
  - Names that disappeared after 1950
- Auto-visualization of query results (bar/line charts)
- Interactive result tables

### 🏆 Your Name's Peak Decade
- Find when a specific name was most popular
- Decade-by-decade bar chart with peak highlighted
- Detailed statistics and rankings
- Total counts across all decades

## Technology Stack

- **Framework**: Streamlit (multi-page app)
- **Database**: SQLite3
- **Visualization**: Plotly Express
- **Data Processing**: Pandas
- **Python**: 3.14.2

---

## Database Schema

**Table: names**
- `id` (INTEGER) - Primary key
- `name` (TEXT) - Baby name
- `year` (INTEGER) - Year of birth
- `gender` (TEXT) - 'M' or 'F'
- `count` (INTEGER) - Number of babies with that name

**Indexes:**
1. `idx_name_year` on (name, year) - Optimizes name lookup across years
2. `idx_year_gender` on (year, gender) - Speeds up yearly aggregations

**Justification:**
- The (name, year) index speeds up queries like "SELECT * FROM names WHERE name=? ORDER BY year" which is used for the name popularity feature (primary use case)
- The (year, gender) index speeds up queries like "SELECT year, SUM(count) FROM names GROUP BY year, gender" which is needed for calculating yearly totals for percentage calculations

## Dataset

- **Source**: NationalNames.csv
- **Records**: 1,825,433 rows
- **Unique Names**: 93,889
- **Year Range**: 1880-2014
- **Columns**: Id, Name, Year, Gender, Count

## Installation & Setup

> **Installation instructions are in the [main README](../README.md)**. All dependencies are installed from the root `requirements.txt`.

### Database Setup (One-Time)

```bash
cd task1
python database.py
cd ..
```

This will:
- Load 1,825,433 rows from NationalNames.csv into SQLite
- Create proper schema with indexes
- Display statistics about the loaded data

Expected output:
```
✓ Loaded 1,825,433 rows into 'names' table
✓ Created index on (name, year)
✓ Created index on (year, gender)
```

### Run the App

From the project root:
```bash
streamlit run app.py
```

Navigate to **"Baby Names Explorer"** in the sidebar.

---

## Project Structure (Task 1)

```
task1/
├── database.py              # Database setup and CSV loading
├── utils.py                 # SQL utility functions
├── discover_patterns.py     # Pattern discovery analysis
├── babynames.db            # SQLite database (created by database.py)
└── README.md               # This file

pages/
└── 1_👶_Baby_Names_Explorer.py  # Main Streamlit page (in root/pages/)

Root:
└── app.py                   # Multi-page app entry point
```

---

## Features

## Usage Examples

### Example 1: Compare Popular Names
1. Navigate to "Name Popularity Over Time"
2. Enter: `Mary, Emma, Sophia`
3. Select gender filter
4. Toggle "Show as percentage" to see relative popularity

### Example 2: Find Gender-Neutral Names
1. Navigate to "Custom SQL Queries"
2. Click "Gender-Neutral Names" button
3. Execute the pre-built query
4. See names used for both boys and girls

### Example 3: Discover Your Name's Peak
1. Navigate to "Your Name's Peak Decade"
2. Enter your name (e.g., "Amit")
3. Select gender
4. Click "Find Peak Decade"
5. View decade-by-decade breakdown

## SQL Safety

The app implements strict SQL safety validation:
- ✅ Only SELECT statements allowed
- ❌ Blocks INSERT, UPDATE, DELETE, DROP, ALTER, CREATE
- ❌ Blocks PRAGMA and other dangerous commands
- Uses parameterized queries to prevent SQL injection

## Screenshots

### Name Popularity Feature
![Name Popularity](screenshots/name_popularity.png)
*Track multiple names over time with interactive charts*

### SQL Query Panel
![SQL Queries](screenshots/sql_panel.png)
*Run custom queries with built-in safety*

### Peak Decade Feature
![Peak Decade](screenshots/peak_decade.png)
*Discover when a name was most popular*

## Assignment Notes

**Task 1.1 - Data Loading & Schema Design (5pt)**
- ✅ CSV loaded into SQLite with proper schema
- ✅ 2 indexes created with justifications

**Task 1.2 - Interactive Name Explorer App (15pt)**
- ✅ Name popularity over time with line chart
- ✅ Toggle between count and percentage
- ✅ Custom SQL query panel with safety
- ✅ 3 pre-built example queries
- ✅ Additional visualization: "Your Name's Peak Decade"

**Task 1.3 - Pattern Discovery (10pt)**
- See `report.md` for 3 interesting patterns discovered

## Deployment

This task is part of a multi-page app. Deploy the entire project:

### Option 1: Streamlit Cloud (Recommended)
1. Push code to GitHub repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy the `app.py` file (root level)
5. Share public URL

### Option 2: Local Hosting
From project root:
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---
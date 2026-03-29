# Task 1: Baby Names Explorer 👶

An interactive web application for exploring US baby name trends from 1880-2014.

**Note**: See the [main README](../README.md) for installation instructions and more detailes.

## Quick Start

Install dependencies from the root `requirements.txt`.

From the project root:
```bash
# Run the multi-page app
streamlit run app.py
```

In the web browser, navigate to **"Baby Names Explorer"** in the sidebar.


Then navigate to **"Baby Names Explorer"** in the sidebar.

## Overview
This application loads, presents, and analyzes U.S. baby name data using the [US Baby Names dataset](https://www.kaggle.com/datasets/kaggle/us-baby-names). It provides tools for exploring naming trends over time, comparing name popularity, and gaining insights into patterns in naming.

## Feachers:


### Name Popularity Over Time
- Search for one or multiple names (comma-separated).
- Line charts showing popularity trends.
- Raw counts and percentage of total births.
- Filter by gender: Male, Female, or Both (sum).
- Summary statistics for each name.

### Custom SQL Query Panel
- Write and execute custom SELECT queries.
- Built-in safety validation (only SELECT statements allowed).
- 3 pre-built example queries:
  - Top 10 names in 2010
  - Gender-neutral names (similar counts for M/F)
  - Names that disappeared after 1950
- Auto-visualization of query results (bar/line charts).

### Your Name's Peak Decade
- Find when a specific name was most popular (recommended: see if your name is popular!).
- Decade-by-decade bar chart.
- Statistics and rankings.

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

**Indexes Justifications:**
- The (name, year) index speeds up queries like `SELECT * FROM names WHERE name=? ORDER BY year` which is used for the name popularity feature. The index enables the database to quickly find all rows for a given name already sorted by year, avoiding a full table scan and additional sorting.
- The (year, gender) index speeds up queries like `SELECT year, SUM(count) FROM names GROUP BY year, gender` which is needed for calculating yearly totals and percentage calculations. The index enables the database to efficiently group and aggregate rows by year and gender, speeding up calculations of yearly totals and percentages without scanning the entire table.



## Project Structure (Task 1)

```
task1/
├── database.py                  # Database setup and CSV loading
├── utils.py                     # SQL utility functions
├── discover_patterns.py         # Pattern discovery analysis
├── babynames.db                 # SQLite database (created automtecly by database.py)
└── README_task1.md              # An explanation of the task 1.

pages/
└── 1_👶_Baby_Names_Explorer.py  # Main Streamlit page of task 1.

Root:
└── app.py                        # Multi-page app entry point.
```
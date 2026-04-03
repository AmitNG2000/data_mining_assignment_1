# Task 4: SQL Learning Game - Restaurant Sabotage Edition 🎮

## Overview

An interactive, story-driven game that teaches SQL to complete beginners through a restaurant management scenario with a plot twist!

**Story Arc:**
1. **Levels 1-4:** You're a restaurant owner learning SQL to understand your business
2. **Plot Twist:** Your mean uncle steals the restaurant!
3. **Level 5:** Sabotage the database to ruin his analysis and win back the restaurant!

## Features

### Educational Content
- 5 progressive levels teaching core SQL concepts.
- 21 total challenges with increasing difficulty.
- Real SQLite database with 500+ restaurant orders.
- Immediate query execution and validation.
- Integrated SQL cheatsheet reference.

### Gamification
- Story-driven narrative with emoji-rich presentation.
- Progress tracking across all levels.
- Balloons and celebrations on challenge completion.
- 😈 Unique "sabotage" mechanic in final level.

## Technology Stack
- SQLite database.
- Pandas for data Processing and sql queries.
- Streamlit for the application and visualization.

## SQL Concepts Taught
- Level 1: SELECT & WHERE (5 challenges)
- Level 2: ORDER BY & LIMIT (4 challenges)
- Level 3: GROUP BY & Aggregations (5 challenges)
- Level 4: JOIN (3 challenges)
- Level 5: INSERT & UPDATE (4 challenges)


## Database Schema

### `orders` Table
```sql
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    food_item TEXT NOT NULL,
    category TEXT CHECK (category IN ('Main', 'Dessert', 'Starter')),
    quantity INTEGER CHECK (quantity > 0),
    price REAL CHECK (price >= 0),
    payment_method TEXT CHECK (payment_method IN ('Cash', 'Debit Card', 'Credit Card', 'Online Payment')),
    order_time TEXT NOT NULL
)
```

### `food_items` Table (for JOIN exercises)
```sql
CREATE TABLE food_items (
    food_item TEXT PRIMARY KEY,
    cost_to_make REAL CHECK (cost_to_make >= 0),
    profit_margin REAL
)
```

**Sample Data:**
- 500 restaurant orders
- 9 menu items with cost data
- Categories: Main, Dessert, Starter
- Payment methods: Cash, Credit Card, Debit Card, Online Payment
- Timestamps from 2025

## Project Structure

```
task4/
├── __init__.py              # Package initialization
├── database.py              # SQLite setup, CSV loading, reset functions
├── game_logic.py            # Level/Challenge classes, validation logic
├── levels.py                # All 5 level definitions with challenges
├── ui_components.py         # Streamlit UI rendering functions
├── restaurant_orders.csv    # Original data (500 orders)
└── restaurant.db            # Generated SQLite database (auto-created, gitignored)

pages/
└── 4_🎮_SQL_Learning_Game.py  # Main Streamlit page
```


### Technology Choices

**Streamlit**: 
- Rapid prototyping
- Built-in session state management
- Easy DataFrame display
- Native multi-page support

**SQLite via sqlite3**:
- Lightweight, no server needed
- Standard Python library
- Easy integration with Streamlit.


**Pandas**:
- Easy CSV loading.
- Strong data manipulation capabilities.
- Good  integration with SQLite and Streamlit.
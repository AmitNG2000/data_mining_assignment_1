# Task 1 Assignment Report: Baby Names Explorer

**Student**: Amit  
**Course**: Data Mining  
**Assignment**: Task 1 - Baby Names Explorer

---

## Part 1: What I Built and How It Works

I built an interactive web application called "Baby Names Explorer" that allows users to analyze US baby name trends from 1880-2014. The application has three main features:

### Feature 1: Name Popularity Over Time
Users can enter one or more names (comma-separated) and see line charts showing how popular those names were across different years. There's a toggle to switch between showing raw counts (how many babies were given that name) versus percentage of total births (relative popularity). Users can also filter by gender (Male, Female, or Both). The application queries the SQLite database for each name and uses Plotly Express to create interactive line charts.

### Feature 2: Custom SQL Query Panel
This feature lets users write and execute their own SELECT queries against the database. For safety, the system validates that only SELECT statements are allowed - any INSERT, UPDATE, DELETE, or DROP commands are blocked. I included three pre-built example queries as buttons: "Top 10 Names in 2010", "Gender-Neutral Names" (names used for both boys and girls), and "Names That Disappeared" (popular before 1950 but rare after 1980). When results are returned, they're displayed as a table, and the app tries to auto-generate visualizations if the results contain numeric and categorical columns.

### Feature 3: Your Name's Peak Decade
Users enter a name and gender, and the app finds which decade that name was most popular. It shows a bar chart with all decades, highlighting the peak decade in a different color. Below the chart, there's a detailed breakdown showing total babies per decade and rankings.

### Technical Implementation
The backend uses SQLite to store 1.8 million rows of data. I created two indexes: one on (name, year) to speed up name lookups across years, and one on (year, gender) to optimize yearly aggregations needed for percentage calculations. The frontend is built with Streamlit, which handles the user interface and interactivity. Plotly Express creates the interactive charts. All database queries use parameterized statements to prevent SQL injection.

---

## Part 2: Technology Choices and Rationale

### Why Streamlit?
I chose Streamlit over Dash, Gradio, or Jupyter widgets because it's the easiest to deploy (Streamlit Cloud is free and takes minutes) and requires the least code to create interactive apps. The syntax is straightforward - you just write Python code top-to-bottom and Streamlit handles the UI automatically. It also has great documentation and a large community.

### Why Plotly Express?
I chose Plotly Express for visualization because it creates interactive charts out of the box (hover tooltips, zoom, pan) with minimal code. Compared to Matplotlib, Plotly charts are more engaging for users. Compared to Altair, Plotly Express has simpler syntax for common charts and better integration with Streamlit.

### Why SQLite with Raw SQL?
The assignment required using sqlite3 with raw SQL (no ORM) for this task. This was appropriate because the queries are relatively simple (mostly SELECT statements) and SQLite is lightweight - no server setup required. I used pandas' read_sql_query() to execute queries and return DataFrames, which made it easy to pass results to Plotly.

### Index Strategy
I created two indexes based on the query patterns I anticipated:
1. **(name, year)**: The main use case is looking up a specific name across all years. This index allows fast retrieval of all records for a given name, sorted by year.
2. **(year, gender)**: For percentage calculations, I need to compute total births per year (and optionally by gender). This index speeds up GROUP BY queries on year and gender.

Without these indexes, queries would require full table scans on 1.8 million rows. With the indexes, lookups are nearly instant.

---

## Part 3: Challenges Encountered and How I Solved Them

### Challenge 1: Loading 1.8M Rows Efficiently
Initially, I tried loading the CSV row-by-row with individual INSERT statements, which was extremely slow (estimated 30+ minutes). 

**Solution**: I used pandas to read the entire CSV into a DataFrame, then used `to_sql()` with `if_exists='append'` to bulk insert all rows at once. This reduced the loading time to about 10-15 seconds.

### Challenge 2: Calculating Percentage of Total Births
To show a name as a percentage of total births, I needed to know the total number of births for each year. This required aggregating the entire dataset for each year.

**Solution**: I created a utility function `get_total_births_by_year()` that pre-computes the yearly totals, then I merge this with the name data using pandas. I also added the (year, gender) index to make these aggregations fast. For the "Both genders" case, I sum across both M and F.

### Challenge 3: SQL Safety Validation
I needed to prevent users from executing dangerous queries (DELETE, DROP, etc.) while still allowing flexible SELECT queries.

**Solution**: I created an `is_select_only()` function that checks two things: (1) the query must start with SELECT, and (2) it cannot contain dangerous keywords like DELETE, DROP, INSERT, UPDATE, etc. I split the query into words and check for these keywords. If a dangerous query is detected, the app shows a friendly error message explaining why it was blocked.

### Challenge 4: Handling Names Not Found
When users search for a name that doesn't exist in the database (or doesn't exist for the selected gender), the query returns an empty result, which could crash the visualization code.

**Solution**: I added checks after every database query to see if the result DataFrame is empty (`len(df) == 0`). If empty, I display a friendly warning message using Streamlit's `st.warning()` and suggest trying a different name or checking the spelling.

---

## Part 4: Three Interesting Patterns Discovered

### Pattern 1: Explosion of Name Diversity (1184% Increase)

**Finding**: The number of unique baby names has increased dramatically over time. In the 1880s, there were only 3,610 unique names. By the 2010s, this had grown to 46,359 unique names - a 1,184% increase!

**Query**:
```sql
SELECT 
    (year / 10) * 10 as decade,
    COUNT(DISTINCT name) as unique_names,
    SUM(count) as total_births
FROM names
GROUP BY decade
ORDER BY decade
```

**Interpretation**: This pattern reflects a major cultural shift toward individualism. In the past, parents tended to choose from a small set of traditional names (Mary, John, William, etc.). Today, parents value uniqueness and creativity in naming. They're inventing new names, using unusual spellings, drawing from diverse cultural sources, and breaking away from conventional naming patterns. This trend accelerated especially after the 1970s, coinciding with broader cultural changes emphasizing personal expression and identity.

---

### Pattern 2: The 'Jennifer' Cultural Phenomenon

**Finding**: The name "Jennifer" experienced an explosive spike in the 1970s, reaching its peak in 1970 with over 63,000 babies given that name (representing about 3.3% of ALL female births that year!). Before 1960, Jennifer was relatively uncommon. After the spike, it gradually declined but remained popular through the 1990s.

**Query**:
```sql
SELECT 
    year,
    SUM(count) as total
FROM names
WHERE LOWER(name) = 'jennifer' AND gender = 'F'
GROUP BY year
ORDER BY year
```

**Interpretation**: This dramatic spike was primarily driven by the 1970 romantic film "Love Story," starring Ali MacGraw as Jennifer Cavalleri. The movie was a massive cultural hit, and millions of parents were inspired to name their daughters Jennifer. This demonstrates how powerful popular culture (movies, celebrities, TV shows) can be in influencing naming trends. Similar patterns can be seen with other names after major films or celebrity babies (e.g., "Emma" after Harry Potter, "Arya" after Game of Thrones in later years).

---

### Pattern 3: Gender-Neutral Names Are Increasing

**Finding**: Certain names like "Riley," "Casey," "Jordan," and "Taylor" have been used almost equally for both boys and girls throughout history. When looking at names with at least 5,000 occurrences for both genders, we find dozens of truly gender-neutral names.

**Query** (example):
```sql
SELECT 
    name,
    SUM(CASE WHEN gender = 'F' THEN count ELSE 0 END) as female_total,
    SUM(CASE WHEN gender = 'M' THEN count ELSE 0 END) as male_total
FROM names
GROUP BY name
HAVING female_total > 5000 AND male_total > 5000
ORDER BY ABS(female_total - male_total) ASC
LIMIT 10
```

**Interpretation**: Gender-neutral names reflect evolving social attitudes about gender roles and identity. Parents are increasingly comfortable choosing names that don't conform to traditional gender norms. This trend has accelerated since the 1980s-1990s, parallel to broader conversations about gender equality and fluidity. Names like "Jordan" (famous from basketball star Michael Jordan, used for both boys and girls) show how cultural icons can make names acceptable across genders.

---

## Conclusion

Building this Baby Names Explorer taught me how to work with large datasets (1.8M rows), optimize database queries with indexes, build interactive web applications, and discover meaningful patterns in data. The three patterns I found reveal fascinating insights about American culture: increasing individualism (name diversity), the power of pop culture (Jennifer spike), and changing gender norms (neutral names). The most surprising discovery was just how dramatically name diversity has exploded - we went from 3,600 names to 46,000 names in just over a century!

---

**Note**: This report was written in my own words without LLM assistance, as required by the assignment guidelines.

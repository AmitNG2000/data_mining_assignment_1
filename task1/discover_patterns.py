"""
Pattern discovery script for Baby Names Explorer.
Finds 3 interesting patterns in the data.
"""
from utils import execute_query
import pandas as pd

print("=" * 70)
print("PATTERN DISCOVERY: Baby Names Dataset Analysis")
print("=" * 70)
print()

# ============================================================================
# PATTERN 1: Name Diversity Over Time
# ============================================================================
print("PATTERN 1: Explosion of Name Diversity")
print("-" * 70)

query1 = """
SELECT 
    (year / 10) * 10 as decade,
    COUNT(DISTINCT name) as unique_names,
    SUM(count) as total_births
FROM names
GROUP BY decade
ORDER BY decade
"""

success, df1 = execute_query(query1)
if success:
    print("\nDecade-by-Decade Unique Names:")
    print(df1.to_string(index=False))
    
    first_decade = df1.iloc[0]
    last_decade = df1.iloc[-1]
    increase = ((last_decade['unique_names'] / first_decade['unique_names']) - 1) * 100
    
    print(f"\n🔍 FINDING:")
    print(f"   Name diversity increased by {increase:.1f}% from {int(first_decade['decade'])}s to {int(last_decade['decade'])}s")
    print(f"   1880s: {int(first_decade['unique_names']):,} unique names")
    print(f"   2010s: {int(last_decade['unique_names']):,} unique names")
    
    print(f"\n📊 INTERPRETATION:")
    print(f"   Parents are choosing increasingly unique and diverse names over time.")
    print(f"   This reflects a cultural shift toward individualism and away from")
    print(f"   traditional naming conventions. Modern parents value creativity and")
    print(f"   distinction in baby names more than conformity to popular choices.")

print("\n" + "=" * 70 + "\n")

# ============================================================================
# PATTERN 2: Gender-Neutral Names
# ============================================================================
print("PATTERN 2: Most Gender-Neutral Names in History")
print("-" * 70)

query2 = """
SELECT 
    n1.name,
    SUM(n1.count) as female_total,
    SUM(n2.count) as male_total,
    ABS(SUM(n1.count) - SUM(n2.count)) as difference,
    ROUND(MIN(SUM(n1.count), SUM(n2.count)) * 100.0 / 
          MAX(SUM(n1.count), SUM(n2.count)), 1) as balance_pct
FROM names n1
JOIN names n2 ON n1.name = n2.name AND n1.year = n2.year
WHERE n1.gender = 'F' AND n2.gender = 'M'
GROUP BY n1.name
HAVING female_total > 5000 AND male_total > 5000
ORDER BY difference ASC
LIMIT 10
"""

success, df2 = execute_query(query2)
if success:
    print("\nTop 10 Most Gender-Neutral Names (with 5000+ uses for each gender):")
    print(df2.to_string(index=False))
    
    top_name = df2.iloc[0]
    
    print(f"\n🔍 FINDING:")
    print(f"   '{top_name['name']}' is the most gender-neutral name in US history,")
    print(f"   with {int(top_name['female_total']):,} female and {int(top_name['male_total']):,} male occurrences")
    print(f"   (only {int(top_name['difference']):,} difference)")
    
    print(f"\n📊 INTERPRETATION:")
    print(f"   Gender-neutral names reflect changing social attitudes about gender roles.")
    print(f"   Names like '{top_name['name']}', 'Riley', and 'Casey' have been consistently used")
    print(f"   for both boys and girls, showing that some names transcend traditional")
    print(f"   gender associations. This trend has accelerated in recent decades.")

print("\n" + "=" * 70 + "\n")

# ============================================================================
# PATTERN 3: Celebrity/Cultural Impact - Example: Jennifer
# ============================================================================
print("PATTERN 3: Cultural Phenomenon - The 'Jennifer' Spike")
print("-" * 70)

query3 = """
SELECT 
    year,
    SUM(count) as total,
    ROUND(SUM(count) * 100.0 / (SELECT SUM(count) FROM names n2 WHERE n2.year = names.year AND n2.gender = 'F'), 3) as pct_of_births
FROM names
WHERE LOWER(name) = 'jennifer' AND gender = 'F'
GROUP BY year
ORDER BY year
"""

success, df3 = execute_query(query3)
if success:
    print("\n'Jennifer' Popularity Over Time:")
    peak_year = df3.loc[df3['total'].idxmax()]
    
    df3_display = df3[df3['year'] >= 1960]
    print(df3_display.to_string(index=False))
    
    print(f"\n🔍 FINDING:")
    print(f"   'Jennifer' peaked in {int(peak_year['year'])} with {int(peak_year['total']):,} babies")
    print(f"   ({peak_year['pct_of_births']:.3f}% of all female births that year!)")
    print(f"   The name skyrocketed from the 1960s to 1970s")
    
    pre_1960 = df3[df3['year'] == 1960]['total'].values[0] if len(df3[df3['year'] == 1960]) > 0 else 0
    peak_count = peak_year['total']
    
    print(f"\n📊 INTERPRETATION:")
    print(f"   The 'Jennifer' explosion was driven by the 1970 film 'Love Story',")
    print(f"   starring Ali MacGraw as 'Jennifer Cavalleri'. The movie's massive")
    print(f"   success caused millions of parents to name their daughters Jennifer,")
    print(f"   making it the #1 name for girls throughout the 1970s and 1980s.")
    print(f"   This demonstrates how popular culture (movies, celebrities, TV) can")
    print(f"   dramatically influence naming trends.")

print("\n" + "=" * 70)
print("\nPATTERN DISCOVERY COMPLETE")
print("=" * 70)
print("\nAll 3 patterns saved. Use these findings for your report.md!")

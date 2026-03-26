"""
Baby Names Explorer - Interactive Streamlit App
Task 1: Data Mining Assignment

Features:
1. Name Popularity Over Time - Line chart with count/percentage toggle
2. Custom SQL Query Panel - Safe query execution with examples
3. Your Name's Peak Decade - Find when a name was most popular
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os

# Add task1 directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'task1'))

from utils import (
    get_name_popularity, 
    get_total_births_by_year, 
    execute_query, 
    is_select_only,
    get_peak_decade
)

# Page configuration
st.set_page_config(
    page_title="Baby Names Explorer",
    page_icon="👶",
    layout="wide"
)

# Title and description
st.title("👶 Baby Names Explorer")
st.markdown("""
Explore US baby name trends from 1880-2014 using interactive visualizations and custom SQL queries.
Dataset: 1.8M records from NationalNames.csv
""")

# Sidebar navigation
st.sidebar.title("Navigation")
feature = st.sidebar.radio(
    "Choose a feature:",
    ["📈 Name Popularity Over Time", "🔍 Custom SQL Queries", "🏆 Your Name's Peak Decade"]
)

# st.sidebar.markdown("---")
# st.sidebar.markdown("**About**")
# st.sidebar.info("Built with Streamlit, SQLite, and Plotly Express for Data Mining Assignment 1")

# ============================================================================
# FEATURE 1: Name Popularity Over Time
# ============================================================================
if feature == "📈 Name Popularity Over Time":
    st.header("📈 Name Popularity Over Time")
    st.markdown("Enter one or more names (comma-separated) to see their popularity trends.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        names_input = st.text_input(
            "Name(s)", 
            value="Mary, John, Emma",
            help="Enter multiple names separated by commas"
        )
    
    with col2:
        gender_filter = st.selectbox("Gender", ["Both (sum)", "Female", "Male"])
    
    # Toggle between count and percentage
    show_percentage = st.checkbox(
        "Show as percentage of total births", 
        value=False,
        help="Display relative popularity instead of raw counts"
    )
    
    if names_input:
        names = [name.strip() for name in names_input.split(',') if name.strip()]
        
        if len(names) > 0:
            # Map gender selection
            gender_map = {"Female": "F", "Male": "M", "Both (sum)": None}
            selected_gender = gender_map[gender_filter]
            
            # Collect data for all names
            all_data = []
            
            for name in names:
                df = get_name_popularity(name, gender=selected_gender)
                
                if len(df) > 0:
                    df['name'] = name
                    all_data.append(df)
                else:
                    st.warning(f"No data found for '{name}' with gender filter: {gender_filter}")
            
            if all_data:
                # Combine all data
                combined_df = pd.concat(all_data, ignore_index=True)
                
                # If showing percentage, calculate it
                if show_percentage:
                    # Get total births by year
                    if selected_gender:
                        totals_df = get_total_births_by_year(gender=selected_gender)
                    else:
                        # For "Both", need to sum across all records for each name/year
                        totals_df = get_total_births_by_year()
                    
                    # Merge with totals
                    combined_df = combined_df.merge(totals_df, on='year', how='left')
                    combined_df['percentage'] = (combined_df['count'] / combined_df['total_births']) * 100
                    y_column = 'percentage'
                    y_label = 'Percentage of Total Births (%)'
                    hover_data = {'count': True, 'percentage': ':.4f'}
                else:
                    y_column = 'count'
                    y_label = 'Number of Babies'
                    hover_data = {'count': True}
                
                # Create line chart
                fig = px.line(
                    combined_df,
                    x='year',
                    y=y_column,
                    color='name',
                    title=f"Name Popularity: {', '.join(names)}",
                    labels={'year': 'Year', y_column: y_label, 'name': 'Name'},
                    hover_data=hover_data
                )
                
                fig.update_layout(
                    hovermode='x unified',
                    height=500,
                    xaxis_title="Year",
                    yaxis_title=y_label
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show summary statistics
                st.subheader("Summary Statistics")
                cols = st.columns(len(names))
                
                for idx, name in enumerate(names):
                    name_data = combined_df[combined_df['name'] == name]
                    if len(name_data) > 0:
                        with cols[idx]:
                            st.metric(
                                f"{name}",
                                f"{name_data['count'].sum():,} total",
                                f"{name_data['year'].min()}-{name_data['year'].max()}"
                            )

# ============================================================================
# FEATURE 2: Custom SQL Query Panel
# ============================================================================
elif feature == "🔍 Custom SQL Queries":
    st.header("🔍 Custom SQL Query Panel")
    st.markdown("Run custom SELECT queries against the baby names database.")
    
    # Pre-built example queries
    st.subheader("📝 Example Queries")
    
    col1, col2, col3 = st.columns(3)
    
    example_queries = {
        "Top 10 Names in 2010": """SELECT name, gender, SUM(count) as total
FROM names
WHERE year = 2010
GROUP BY name, gender
ORDER BY total DESC
LIMIT 10""",
        
        "Gender-Neutral Names": """SELECT 
    n1.name,
    n1.count as female_count,
    n2.count as male_count,
    n1.year
FROM names n1
JOIN names n2 ON n1.name = n2.name AND n1.year = n2.year
WHERE n1.gender = 'F' AND n2.gender = 'M'
AND ABS(n1.count - n2.count) < 100
AND n1.year = 2000
ORDER BY n1.count DESC
LIMIT 10""",
        
        "Names That Disappeared": """SELECT 
    name,
    SUM(CASE WHEN year < 1950 THEN count ELSE 0 END) as before_1950,
    SUM(CASE WHEN year > 1980 THEN count ELSE 0 END) as after_1980
FROM names
GROUP BY name
HAVING before_1950 > 10000 AND after_1980 < 100
ORDER BY before_1950 DESC
LIMIT 10"""
    }
    
    selected_example = None
    
    with col1:
        if st.button("📊 Top 10 Names in 2010"):
            selected_example = "Top 10 Names in 2010"
    
    with col2:
        if st.button("⚖️ Gender-Neutral Names"):
            selected_example = "Gender-Neutral Names"
    
    with col3:
        if st.button("📉 Names That Disappeared"):
            selected_example = "Names That Disappeared"
    
    # SQL input area
    st.subheader("✍️ Write Your Query")
    
    default_query = example_queries.get(selected_example, "SELECT * FROM names LIMIT 10")
    
    query = st.text_area(
        "SQL Query",
        value=default_query,
        height=150,
        help="Only SELECT statements are allowed for safety"
    )
    
    if st.button("🚀 Execute Query", type="primary"):
        # Validate query safety
        is_safe, error_msg = is_select_only(query)
        
        if not is_safe:
            st.error(f"🚫 Query Blocked: {error_msg}")
            st.info("💡 Only SELECT statements are allowed. Please remove any INSERT, UPDATE, DELETE, DROP, or other modification commands.")
        else:
            # Execute query
            with st.spinner("Executing query..."):
                success, result = execute_query(query)
            
            if success:
                st.success(f"✓ Query executed successfully! ({len(result)} rows returned)")
                
                # Display results as table
                st.subheader("📋 Results")
                st.dataframe(result, use_container_width=True)
                
                # Try to auto-generate a chart if applicable
                if len(result) > 0:
                    numeric_cols = result.select_dtypes(include=['number']).columns.tolist()
                    categorical_cols = result.select_dtypes(include=['object']).columns.tolist()
                    
                    # If we have at least one numeric and one categorical column, offer visualization
                    if len(numeric_cols) > 0 and len(categorical_cols) > 0:
                        st.subheader("📊 Visualization")
                        
                        chart_col1, chart_col2 = st.columns(2)
                        with chart_col1:
                            x_col = st.selectbox("X-axis", categorical_cols + numeric_cols, key="x_axis")
                        with chart_col2:
                            y_col = st.selectbox("Y-axis", numeric_cols, key="y_axis")
                        
                        chart_type = st.radio("Chart Type", ["Bar", "Line"], horizontal=True)
                        
                        if chart_type == "Bar":
                            fig = px.bar(result, x=x_col, y=y_col, title="Query Results Visualization")
                        else:
                            fig = px.line(result, x=x_col, y=y_col, title="Query Results Visualization")
                        
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"❌ Query Error: {result}")
                st.info("💡 Check your SQL syntax and make sure the table/column names are correct.")

# ============================================================================
# FEATURE 3: Your Name's Peak Decade
# ============================================================================
elif feature == "🏆 Your Name's Peak Decade":
    st.header("🏆 Your Name's Peak Decade")
    st.markdown("Discover when your name was most popular!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_name = st.text_input("Enter a name", value="Emma")
    
    with col2:
        search_gender = st.selectbox("Gender", ["Female", "Male"], key="peak_gender")
    
    if st.button("🔍 Find Peak Decade", type="primary"):
        gender_code = "F" if search_gender == "Female" else "M"
        
        with st.spinner(f"Analyzing popularity of '{search_name}'..."):
            peak_decade, decade_data = get_peak_decade(search_name, gender_code)
        
        if peak_decade is None:
            st.warning(f"😕 No data found for '{search_name}' ({search_gender})")
            st.info("Try a different name or check the spelling. The dataset covers US baby names from 1880-2014.")
        else:
            st.success(f"✨ Peak decade for '{search_name}' ({search_gender}): **{peak_decade}s**")
            
            # Create decade labels
            decade_data['decade_label'] = decade_data['decade'].astype(str) + "s"
            
            # Highlight peak decade
            decade_data['is_peak'] = decade_data['decade'] == peak_decade
            decade_data['color'] = decade_data['is_peak'].map({True: 'Peak Decade', False: 'Other'})
            
            # Create bar chart
            fig = px.bar(
                decade_data,
                x='decade_label',
                y='total_count',
                title=f"Popularity of '{search_name}' by Decade",
                labels={'decade_label': 'Decade', 'total_count': 'Total Babies'},
                color='color',
                color_discrete_map={'Peak Decade': '#FF6B6B', 'Other': '#4ECDC4'}
            )
            
            fig.update_layout(
                showlegend=True,
                height=400,
                xaxis_title="Decade",
                yaxis_title="Total Babies"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show detailed statistics
            st.subheader("📊 Decade-by-Decade Breakdown")
            
            # Add rank column
            decade_data['rank'] = decade_data['total_count'].rank(ascending=False, method='min').astype(int)
            
            display_df = decade_data[['decade_label', 'total_count', 'rank']].copy()
            display_df.columns = ['Decade', 'Total Babies', 'Rank']
            display_df = display_df.sort_values('Rank')
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Peak decade stats
            peak_row = decade_data[decade_data['decade'] == peak_decade].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Peak Decade", f"{peak_decade}s")
            with col2:
                st.metric("Babies in Peak Decade", f"{int(peak_row['total_count']):,}")
            with col3:
                st.metric("Total Across All Decades", f"{int(decade_data['total_count'].sum()):,}")

# Footer
st.markdown("---")
st.markdown("""
**Data Source**: NationalNames.csv (US Baby Names 1880-2014)  
**Database**: SQLite with optimized indexes on (name, year) and (year, gender)  
**Task**: Data Mining Assignment 1 - Baby Names Explorer
""")

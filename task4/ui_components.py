"""
UI components for SQL Learning Game.
Streamlit-based rendering functions for story, challenges, and progress tracking.
"""
import streamlit as st
import pandas as pd
from task4.game_logic import Level, Challenge


def render_story_panel(text: str, emoji: str = "📖"):
    """
    Render an animated story panel with emoji and styled text.
    
    Args:
        text: Story text (supports markdown)
        emoji: Emoji to display prominently
    """
    with st.container():
        st.markdown(f"# {emoji}")
        st.markdown(text)
        st.markdown("---")


def render_sql_input(challenge_id: str, key_suffix: str = ""):
    """
    Render a SQL code editor input field.
    
    Args:
        challenge_id: Unique ID for the challenge
        key_suffix: Optional suffix for the input key (for multiple inputs)
    
    Returns:
        str: The SQL query entered by user
    """
    query = st.text_area(
        "✍️ Your SQL Query:",
        height=150,
        placeholder="Type your SQL query here...",
        key=f"sql_input_{challenge_id}{key_suffix}",
        help="Write your SQL query and click Submit to check your answer!"
    )
    return query


def render_query_results(df: pd.DataFrame, success: bool = True):
    """
    Render query results in a formatted table.
    
    Args:
        df: Result DataFrame
        success: Whether the query was successful
    """
    if df is None:
        return
    
    if df.empty:
        st.info("🔍 Query executed successfully, but returned no results.")
        return
    
    row_count = len(df)
    
    if success:
        st.success(f"✅ Query returned {row_count} row(s)")
    else:
        st.warning(f"⚠️ Query returned {row_count} row(s), but it doesn't match the expected result")
    
    # Show results in a table
    st.dataframe(df, use_container_width=True, height=min(400, (row_count + 1) * 35 + 50))


def render_challenge(level: Level, challenge_index: int, challenge: Challenge, game_state):
    """
    Render a complete challenge UI with input, submit, and feedback.
    
    Args:
        level: The current Level object
        challenge_index: Index of this challenge in the level
        challenge: The Challenge object
        game_state: Current GameState object
    """
    challenge_id = f"L{level.number}_C{challenge_index + 1}"
    
    # Check if already completed
    is_completed = challenge_index in game_state.level_progress.get(level.number, [])
    
    # Challenge header
    st.markdown(f"### Challenge {challenge_index + 1} of {len(level.challenges)}")
    
    if is_completed:
        st.success("✅ **Completed!** You can retry or move to the next challenge.")
    
    # Challenge question
    st.markdown(challenge.question)
    
    # SQL input
    query = render_sql_input(challenge_id)
    
    # Buttons in columns
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        submit_button = st.button("🚀 Submit Query", key=f"submit_{challenge_id}", type="primary")
    
    with col2:
        hint_button = st.button("💡 Get Hint", key=f"hint_{challenge_id}")
    
    with col3:
        if challenge.expected_query:
            show_solution = st.button("👀 Show Solution", key=f"solution_{challenge_id}")
        else:
            show_solution = False
    
    with col4:
        # Next challenge button (always available)
        if challenge_index < len(level.challenges) - 1:
            next_button = st.button("➡️ Next Challenge", key=f"next_{challenge_id}")
        else:
            next_button = False
    
    # Handle hint button
    if hint_button:
        attempts = game_state.get_attempts(challenge_id)
        hint = challenge.get_hint(attempts + 1)
        st.info(hint)
    
    # Handle show solution button
    if show_solution:
        with st.expander("📝 Example Solution", expanded=True):
            st.code(challenge.expected_query, language="sql")
            st.caption("Try to understand WHY this query works, not just copy it! 😊")
    
    # Handle next challenge button
    if next_button:
        return "next_challenge"
    
    # Handle submit button
    if submit_button:
        if not query or not query.strip():
            st.error("❌ Please enter a SQL query before submitting!")
            return False
        
        # Increment attempt counter
        game_state.increment_attempt(challenge_id)
        
        # Validate the answer
        is_correct, message, result_df = challenge.validate_answer(query)
        
        if is_correct:
            st.success(message)
            
            # Show results if available
            if result_df is not None:
                render_query_results(result_df, success=True)
            
            # Mark as complete
            if not is_completed:
                game_state.mark_challenge_complete(level.number, challenge_index)
                st.balloons()
                st.info("🎉 Challenge complete! Click 'Next Challenge' to continue or try another approach!")
            
            return True
        else:
            st.error(message)
            
            # Show results if available (to help debug)
            if result_df is not None:
                render_query_results(result_df, success=False)
                
                # Show expected result hint after 2 attempts
                attempts = game_state.get_attempts(challenge_id)
                if attempts >= 2 and challenge.expected_result is not None:
                    with st.expander("🎯 Expected Result Preview (click to expand)"):
                        st.caption("Your query should return something like this:")
                        st.dataframe(challenge.expected_result.head(10), use_container_width=True)
            
            return False
    
    return None


def render_progress_tracker(game_state, total_levels: int):
    """
    Render a visual progress tracker showing completed levels.
    
    Args:
        game_state: Current GameState object
        total_levels: Total number of levels
    """
    st.sidebar.markdown("## 📊 Your Progress")
    
    progress_pct = game_state.get_overall_progress(total_levels)
    st.sidebar.progress(progress_pct / 100.0)
    st.sidebar.caption(f"{len(game_state.completed_levels)} of {total_levels} levels complete ({progress_pct:.0f}%)")
    
    st.sidebar.markdown("---")
    
    # Level status
    for level_num in range(1, total_levels + 1):
        if level_num in game_state.completed_levels:
            st.sidebar.markdown(f"✅ **Level {level_num}** - Complete")
        elif level_num == game_state.current_level:
            completed_challenges = game_state.level_progress.get(level_num, [])
            st.sidebar.markdown(f"🎯 **Level {level_num}** - In Progress ({len(completed_challenges)} challenges)")
        elif game_state.can_access_level(level_num):
            st.sidebar.markdown(f"🔓 **Level {level_num}** - Available")
        else:
            st.sidebar.markdown(f"🔒 **Level {level_num}** - Locked")


def render_level_navigation(game_state, total_levels: int, all_levels):
    """
    Render level navigation buttons in sidebar with challenge selection.
    
    Args:
        game_state: Current GameState object
        total_levels: Total number of levels
        all_levels: List of all Level objects
    """
    st.sidebar.markdown("## 🗺️ Navigation")
    
    # Level selection
    for level_num in range(1, total_levels + 1):
        level = all_levels[level_num - 1]
        
        # Level button
        if st.sidebar.button(
            f"Level {level_num}: {level.title[:20]}...", 
            key=f"nav_level_{level_num}",
            disabled=(level_num == game_state.current_level),
            use_container_width=True
        ):
            game_state.current_level = level_num
            if 'current_challenge_idx' not in st.session_state:
                st.session_state.current_challenge_idx = 0
            st.session_state.current_challenge_idx = 0
            st.rerun()
        
        # Show challenge selection for current level
        if level_num == game_state.current_level:
            completed_in_level = game_state.level_progress.get(level_num, [])
            for ch_idx in range(len(level.challenges)):
                status_emoji = "✅" if ch_idx in completed_in_level else "⭕"
                challenge_text = f"  {status_emoji} Challenge {ch_idx + 1}"
                
                current_ch_idx = st.session_state.get('current_challenge_idx', 0)
                if st.sidebar.button(
                    challenge_text,
                    key=f"nav_ch_{level_num}_{ch_idx}",
                    disabled=(ch_idx == current_ch_idx),
                    use_container_width=True
                ):
                    st.session_state.current_challenge_idx = ch_idx
                    st.rerun()


def render_database_schema():
    """Render a helpful database schema reference."""
    with st.expander("📚 Database Schema Reference", expanded=False):
        st.markdown("""
        ### 📋 `orders` Table
        
        | Column | Type | Description |
        |--------|------|-------------|
        | order_id | INTEGER | Unique order number |
        | customer_name | TEXT | Customer who ordered |
        | food_item | TEXT | Menu item (Pizza, Burger, etc.) |
        | category | TEXT | Main, Dessert, or Starter |
        | quantity | INTEGER | How many items |
        | price | REAL | Price per item ($) |
        | payment_method | TEXT | Cash, Credit Card, Debit Card, Online Payment |
        | order_time | TEXT | When ordered (timestamp) |
        
        ### 🍕 `food_items` Table (for JOIN exercises)
        
        | Column | Type | Description |
        |--------|------|-------------|
        | food_item | TEXT | Menu item name |
        | cost_to_make | REAL | Cost to prepare ($) |
        | profit_margin | REAL | Profit ratio (0-1) |
        
        ---
        
        **💡 Quick Tips:**
        - Use `SELECT *` to see all columns
        - Use `LIMIT 10` to see first 10 rows
        - Strings need single quotes: `'Pizza'`
        - Numbers don't need quotes: `5`, `12.50`
        """)


def render_sql_cheatsheet():
    """Render a SQL cheatsheet in the sidebar."""
    with st.sidebar.expander("📖 SQL Cheatsheet"):
        st.markdown("""
        **Basic Query Structure:**
        ```sql
        SELECT columns
        FROM table
        WHERE condition
        ORDER BY column
        LIMIT number
        ```
        
        **Common Commands:**
        - `SELECT *` - All columns
        - `SELECT col1, col2` - Specific columns
        - `WHERE price > 10` - Filter rows
        - `AND` / `OR` - Combine conditions
        - `ORDER BY col DESC` - Sort (DESC = high to low)
        - `LIMIT 5` - First 5 results
        
        **Aggregations:**
        - `COUNT(*)` - Count rows
        - `SUM(column)` - Add up values
        - `AVG(column)` - Average
        - `MAX(column)` - Maximum
        - `MIN(column)` - Minimum
        - `GROUP BY column` - Group for aggregation
        
        **JOIN:**
        ```sql
        SELECT *
        FROM table1
        JOIN table2 ON table1.col = table2.col
        ```
        
        **Modify Data:**
        - `INSERT INTO table VALUES (...)`
        - `UPDATE table SET col = value WHERE condition`
        """)


def render_victory_screen():
    """Render the final victory screen after completing all levels."""
    st.balloons()
    
    st.markdown("""
    # 🎉 CONGRATULATIONS! 🎉
    
    ## You've Completed the SQL Learning Game! 🎓
    
    You've mastered:
    - ✅ **SELECT & WHERE** - View and filter data
    - ✅ **ORDER BY & LIMIT** - Sort and limit results
    - ✅ **GROUP BY & Aggregations** - Calculate totals, averages, counts
    - ✅ **JOIN** - Combine multiple tables
    - ✅ **INSERT & UPDATE** - Modify data (for good or evil! 😈)
    
    ---
    
    ## 🎭 The End... Or Is It?
    
    Your uncle, thoroughly confused by the sabotaged data, has given you back the restaurant!
    
    **Uncle:** *"This makes no sense! Desserts cost $2000?! We sold 10,000 pizzas?! 
    I don't understand this newfangled technology! You can have it back!"* 🏳️
    
    **You:** *"Thanks, Uncle! I learned a lot about SQL... and revenge!"* 😏
    
    ---
    
    ## 🚀 What's Next?
    
    You're now ready to:
    - Query real databases at work or school
    - Analyze business data
    - Build data-driven applications
    - Get certified in SQL
    - Become a data analyst, data scientist, or database administrator!
    
    ---
    
    ## 📚 Want to Learn More?
    
    - [SQLBolt](https://sqlbolt.com/) - Interactive SQL lessons
    - [SQLZoo](https://sqlzoo.net/) - More SQL practice
    - [Mode SQL Tutorial](https://mode.com/sql-tutorial/) - Advanced SQL
    - [LeetCode SQL Problems](https://leetcode.com/problemset/database/) - Challenge yourself!
    
    ---
    
    ### Thank you for playing! 🎮
    
    *Made with ❤️ for HW1 - Data Mining Course*
    """)
    
    # Offer to reset
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Play Again", type="primary", use_container_width=True):
            # Reset game state
            st.session_state.game_state.reset()
            # Reset database
            from task4.database import reset_database
            reset_database()
            st.rerun()


def render_level_complete_transition(level: Level):
    """
    Render a transition screen between levels.
    
    Args:
        level: The level that was just completed
    """
    st.success(f"🎊 Level {level.number} Complete!")
    
    if level.story_outro:
        st.markdown(level.story_outro)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➡️ Continue to Next Level", type="primary", use_container_width=True):
            return True
    
    return False

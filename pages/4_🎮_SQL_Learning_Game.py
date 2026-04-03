"""
Task 4: SQL Learning Game - Restaurant Sabotage Edition
An interactive story-driven game teaching SQL to complete beginners.

Story: You're a restaurant owner learning SQL to understand your business.
Plot twist: Your mean uncle steals the restaurant!
Your revenge: Sabotage the database to ruin his analysis!
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from task4.database import initialize_database, reset_database, validate_database
from task4.game_logic import GameState
from task4.levels import get_level, get_total_levels, ALL_LEVELS, LEVEL_IMAGES
from task4.ui_components import (
    render_story_panel,
    render_challenge,
    render_progress_tracker,
    render_level_navigation,
    render_database_schema,
    render_sql_cheatsheet,
    render_victory_screen,
    render_level_complete_transition
)

# Page config
st.set_page_config(
    page_title="SQL Learning Game",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stButton > button {
        width: 100%;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database on first load
if 'db_initialized' not in st.session_state:
    with st.spinner("🔧 Initializing database..."):
        success = initialize_database()
        if success:
            st.session_state.db_initialized = True
        else:
            st.error("❌ Failed to initialize database. Please refresh the page.")
            st.stop()

# Initialize game state
if 'game_state' not in st.session_state:
    st.session_state.game_state = GameState()

if 'viewing_story' not in st.session_state:
    st.session_state.viewing_story = True

if 'level_intro_shown' not in st.session_state:
    st.session_state.level_intro_shown = {}

# Get current game state
game_state = st.session_state.game_state
total_levels = get_total_levels()
current_level = get_level(game_state.current_level)

# Sidebar
st.sidebar.title("🎮 SQL Learning Game")
st.sidebar.markdown("*Restaurant Sabotage Edition*")
st.sidebar.markdown("---")

# Progress tracker
render_progress_tracker(game_state, total_levels)

# Level navigation with challenge selection
render_level_navigation(game_state, total_levels, ALL_LEVELS)

st.sidebar.markdown("---")

# SQL Cheatsheet
render_sql_cheatsheet()

# Reset button
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Game & Database", help="Start over from Level 1"):
    with st.spinner("Resetting..."):
        game_state.reset()
        reset_database()
        st.session_state.level_intro_shown = {}
        st.session_state.viewing_story = True
    st.sidebar.success("✅ Game reset!")
    st.rerun()

# Main content area
st.title("🎮 SQL Learning Game")
st.markdown("### 🍽️ Restaurant Sabotage Edition")

# Teaser for Level 5
if game_state.current_level < 5:
    st.info("💡 **Hint:** There's a special surprise waiting for you in Level 5... 😈")

# Check if all levels complete
if len(game_state.completed_levels) == total_levels:
    render_victory_screen()
    st.stop()

# Check if current level is valid
if not current_level:
    st.error(f"❌ Level {game_state.current_level} not found!")
    st.stop()

# Show level title with small header image
level_image = LEVEL_IMAGES.get(current_level.number)
if level_image:
    st.image(level_image, width=300)

st.markdown(f"# {current_level.title}")
st.markdown(f"**Level {current_level.number} of {total_levels}**")

# Check if level intro has been shown
level_key = f"level_{current_level.number}"
if level_key not in st.session_state.level_intro_shown:
    st.session_state.level_intro_shown[level_key] = False

# Show story intro if not yet shown or if viewing_story flag is set
if not st.session_state.level_intro_shown[level_key] or st.session_state.viewing_story:
    # Get image for current level
    level_image = LEVEL_IMAGES.get(current_level.number)
    render_story_panel(current_level.story_intro, "📖")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➡️ Start Challenges", type="primary", use_container_width=True, key="start_challenges"):
            st.session_state.level_intro_shown[level_key] = True
            st.session_state.viewing_story = False
            st.rerun()
    
    st.stop()

# Show database schema reference
render_database_schema()

st.markdown("---")

# Initialize or get current challenge index
if 'current_challenge_idx' not in st.session_state:
    st.session_state.current_challenge_idx = 0

current_challenge_idx = st.session_state.current_challenge_idx
completed_challenges = game_state.level_progress.get(current_level.number, [])

# Check if level is complete
if current_challenge_idx >= len(current_level.challenges):
    # Level complete! Show outro and transition
    st.success(f"🎊 **Level {current_level.number} Complete!**")
    
    if current_level.story_outro:
        render_story_panel(current_level.story_outro, "🎉")
    
    # Mark level as complete
    game_state.mark_level_complete(current_level.number)
    
    # Check if this was the last level
    if current_level.number == total_levels:
        st.info("🏆 You've completed all levels! Scroll up to see your victory screen!")
    else:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➡️ Continue to Next Level", type="primary", use_container_width=True, key="next_level"):
                game_state.current_level += 1
                st.session_state.viewing_story = True
                st.rerun()
    
    st.stop()

# Show current challenge
st.markdown(f"## 🎯 Challenge {current_challenge_idx + 1} of {len(current_level.challenges)}")

challenge = current_level.challenges[current_challenge_idx]
result = render_challenge(current_level, current_challenge_idx, challenge, game_state)

# Handle next challenge navigation
if result == "next_challenge":
    st.session_state.current_challenge_idx = current_challenge_idx + 1
    st.rerun()

# Show completed challenges count
if completed_challenges:
    st.markdown("---")
    st.info(f"✅ You've completed {len(completed_challenges)} of {len(current_level.challenges)} challenges in this level!")

# Navigation buttons at bottom
st.markdown("---")
nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    if current_challenge_idx > 0:
        if st.button("⬅️ Previous Challenge", use_container_width=True):
            st.session_state.current_challenge_idx = current_challenge_idx - 1
            st.rerun()

with nav_col2:
    if current_challenge_idx < len(current_level.challenges) - 1:
        if st.button("➡️ Next Challenge", key="bottom_next", use_container_width=True):
            st.session_state.current_challenge_idx = current_challenge_idx + 1
            st.rerun()
    elif current_level.number < total_levels:
        if st.button("🎯 Go to Next Level", use_container_width=True, type="primary"):
            game_state.current_level += 1
            st.session_state.current_challenge_idx = 0
            st.session_state.viewing_story = True
            st.rerun()

with nav_col3:
    if st.button("🔄 Restart Level", use_container_width=True):
        st.session_state.current_challenge_idx = 0
        st.rerun()

# Debug info (only in development)
if st.sidebar.checkbox("🔧 Show Debug Info", value=False):
    st.sidebar.markdown("### Debug Info")
    st.sidebar.json({
        "current_level": game_state.current_level,
        "completed_levels": game_state.completed_levels,
        "level_progress": game_state.level_progress,
        "current_challenge": current_challenge_idx,
        "attempt_counts": game_state.attempt_counts
    })

# Footer
st.markdown("---")
st.caption("🎓 Task 4: SQL Learning Game | Made for HW1 - Data Mining Course")

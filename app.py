"""
Data Mining Assignment 1 - Main Application
Multi-page Streamlit app for all tasks.

Navigate between tasks using the sidebar.
"""
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Data Mining Assignment 1",
    page_icon="📊",
    layout="wide"
)

# Main page
st.title("📊 Data Mining Assignment 1")
st.markdown("By Amit Ner Gaon")

st.markdown("---")

st.markdown("""
## Welcome to the Data Mining Assignment Hub

This is a multi-page Streamlit application containing all tasks for Assignment 1.

### 📋 Assignment Tasks

**Task 1: Baby Names Explorer** 👶
- Interactive exploration of US baby name trends (1880-2014)
- SQLite database with 1.8M records
- Name popularity charts, custom SQL queries, peak decade finder

**Task 2: Oscar Actor Explorer** 🎬 *(Coming Soon)*
- ORM-based actor profile app
- Wikipedia integration
- Nomination and win analysis

**Task 3: Pokémon Battle Arena** ⚔️
- Database-driven battle game with 1025+ Pokémon
- 6 cheat codes with SQL operations (UPDATE/INSERT)
- Type effectiveness system and cheat detection

**Task 4: SQL Learning Game** 🎮 *(Coming Soon)*
- Interactive SQL tutorial
- Progressive challenges
- Gamified learning experience

### 🚀 Getting Started

Use the **sidebar navigation** (←) to switch between tasks.

Each task is a separate page with its own features and documentation.

### 💡 About This Project

This project demonstrates:
- SQLite database design and optimization
- Interactive web applications with Streamlit
- Data visualization with Plotly
- SQL query safety and validation
- ORM patterns (Tasks 2-3)
- Educational game design (Task 4)

### 📚 Technologies Used

- **Framework**: Streamlit (multi-page apps)
- **Database**: SQLite3 + ORMs (PonyORM/SQLAlchemy/Peewee)
- **Visualization**: Plotly Express
- **Data Processing**: Pandas
- **APIs**: Wikipedia API (Task 2)
""")

st.markdown("---")

st.markdown("""
### 📖 Documentation

- **Setup Instructions**: See [README.md](README.md) in the repository
- **Task 1 Report**: See `task1/README.md` for detailed documentation
- **Assignment Instructions**: See `HW1_instructions.pdf`

### 🎓 Course Information

**Course**: The Art of Analyzing Big Data - The Data Scientist's Toolbox  
**Instructor**: Dr. Michael Fire  
**Institution**: Ben-Gurion University (BGU)
""")

st.sidebar.success("👆 Select a task above to get started!")

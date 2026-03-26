"""
Task 2: Oscar Actor Explorer
Coming Soon!
"""
import streamlit as st

st.set_page_config(
    page_title="Oscar Actor Explorer",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Oscar Actor Explorer")
st.markdown("### Task 2 - Coming Soon!")

st.info("""
**Task 2: Oscar Actor Explorer** is currently under development.

### Planned Features:
- 🔍 **Actor Profile Search** - Look up any actor or director
- 📊 **Nomination & Win Statistics** - Detailed career analysis  
- 📖 **Wikipedia Integration** - Live bio, birth date, and photos
- 🏆 **Win Rate Calculator** - Compare to category averages
- 💡 **Interesting Patterns** - 3 discoveries from Oscar data

### Technology Stack:
- **ORM**: PonyORM / SQLAlchemy / Peewee (no raw SQL)
- **API**: Wikipedia Python package
- **Database**: SQLite with proper entity relationships

### Requirements:
- Entity/model classes with types and constraints
- Handle edge cases (actor not found, ambiguous matches, zero wins)
- Computed insights (win rate, years to first win, comparisons)

---

Check back soon for the complete implementation!
""")

st.markdown("---")
st.markdown("[← Back to Main Page](../) | [View Task 1: Baby Names →](1_👶_Baby_Names_Explorer)")

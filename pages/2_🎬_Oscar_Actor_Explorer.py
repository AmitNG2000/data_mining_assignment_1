"""
Oscar Actor Explorer - Streamlit Multi-Page App
Task 2: Data Mining Assignment
"""
import streamlit as st
from pathlib import Path
from pony.orm import db_session
import wikipedia

from task2.database import setup_database, db, Person, Film, Category, Nomination
from task2.load_data import load_oscar_data

# Page config
st.set_page_config(
    page_title="Oscar Actor Explorer",
    page_icon="🎬",
    layout="wide"
)

# Check database setup once per session, but also recover if Pony mapping is missing.
needs_init = (
    "oscar_db_checked" not in st.session_state
    or not st.session_state["oscar_db_checked"]
    or db.provider is None
    or db.schema is None
)

if needs_init:
    with st.spinner("Checking database setup..."):
        db_path = Path(__file__).parent.parent / "task2" / "oscars.db"
        if db_path.exists():
            setup_database(str(db_path), create_db=False)
            st.success("Oscar database is ready.")
        else:
            load_oscar_data(db_path=db_path)
            st.success("Oscar database did not exist and was created successfully.")
        st.session_state["oscar_db_checked"] = True


# Title and description
st.title("🎬 Oscar Actor Explorer")
st.markdown("""
Explore Oscar nominations and wins combined with live Wikipedia data.
Enter an actor or actress name to see their complete Oscar history and biography.
""")

# Sidebar for search
with st.sidebar:
    st.header("Search Actor")
    actor_name = st.text_input("Enter actor/actress name:", placeholder="e.g., Meryl Streep")
    search_button = st.button("Search", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Examples")
    example_actors = [
        "Meryl Streep",
        "Leonardo DiCaprio",
        "Katharine Hepburn",
        "Daniel Day-Lewis",
        "Denzel Washington",
        "Cate Blanchett",
        "Tom Hanks",
        "Frances McDormand"
    ]
    for actor in example_actors:
        if st.button(actor, use_container_width=True):
            actor_name = actor
            search_button = True


def search_actor_in_db(name):
    """Search for actor in database"""
    with db_session:
        search_name = name.strip().lower()
        if not search_name:
            return None

        # Try exact match first
        person = Person.get(name=name)
        if person:
            return person
        
        # Try case-insensitive partial match using ORM + Python filtering.
        for person in Person.select():
            person_name = person.name.lower()
            if search_name in person_name or person_name in search_name:
                return person
        
        return None


def get_actor_stats(person):
    """Get actor statistics from database"""
    with db_session:
        person_id = person.id
        nominations = [
            nomination
            for nomination in Nomination.select()
            if nomination.person.id == person_id
        ]

        total_noms = len(nominations)
        total_wins = sum(1 for nomination in nominations if nomination.is_winner)

        categories = sorted({nomination.category.name for nomination in nominations})
        years_list = sorted({nomination.year for nomination in nominations})
        
        films = {}
        for nomination in nominations:
            if nomination.film:
                film_key = (nomination.film.title, nomination.film.year)
                if film_key not in films:
                    films[film_key] = {'nominations': 0, 'wins': 0}
                films[film_key]['nominations'] += 1
                if nomination.is_winner:
                    films[film_key]['wins'] += 1
        
        # Years to first win
        years_to_win = None
        if total_wins > 0:
            all_noms_sorted = sorted(nominations, key=lambda nomination: nomination.ceremony)
            winning_noms_sorted = sorted(
                (nomination for nomination in nominations if nomination.is_winner),
                key=lambda nomination: nomination.ceremony
            )
            first_ceremony = all_noms_sorted[0].ceremony
            first_win = winning_noms_sorted[0].ceremony
            years_to_win = first_win - first_ceremony
        
        nominations_data = sorted(
            [
                (
                    nomination.year,
                    nomination.is_winner,
                    nomination.category.name,
                    nomination.film.title if nomination.film else None,
                    nomination.ceremony,
                )
                for nomination in nominations
            ],
            key=lambda nomination: nomination[4],
            reverse=True,
        )
        
        return {
            'total_nominations': int(total_noms),
            'total_wins': int(total_wins),
            'win_rate': (total_wins / total_noms * 100) if total_noms > 0 else 0,
            'categories': categories,
            'years_active': years_list,
            'films': films,
            'years_to_first_win': years_to_win,
            'nominations_list': nominations_data
        }


def get_wikipedia_info(actor_name):
    """Fetch Wikipedia information for actor"""
    try:
        # Search for the actor
        search_results = wikipedia.search(actor_name, results=3)
        
        if not search_results:
            return None
        
        # Try first result
        page = wikipedia.page(search_results[0], auto_suggest=False)
        
        # Get summary (first 3 sentences)
        summary = wikipedia.summary(search_results[0], sentences=3, auto_suggest=False)
        
        # Try to get image
        try:
            images = page.images
            main_image = images[0] if images else None
        except:
            main_image = None
        
        return {
            'title': page.title,
            'summary': summary,
            'url': page.url,
            'image': main_image
        }
    except wikipedia.exceptions.DisambiguationError as e:
        # If disambiguation, try with "actor" suffix
        try:
            page = wikipedia.page(f"{actor_name} (actor)", auto_suggest=False)
            summary = wikipedia.summary(f"{actor_name} (actor)", sentences=3, auto_suggest=False)
            return {
                'title': page.title,
                'summary': summary,
                'url': page.url,
                'image': None
            }
        except:
            return {'error': f"Multiple results found. Please be more specific."}
    except:
        return None


def generate_did_you_know(person, stats):
    """Generate 'Did You Know?' fun facts"""
    with db_session:
        # Calculate percentiles without raw SQL.
        nominations_per_person = {}
        for nomination in Nomination.select():
            pid = nomination.person.id
            nominations_per_person[pid] = nominations_per_person.get(pid, 0) + 1

        all_noms = list(nominations_per_person.values())

        person_rank = sum(1 for x in all_noms if x < stats['total_nominations'])
        percentile = (person_rank / len(all_noms) * 100) if all_noms else 0
        
        facts = []
        
        # Nomination percentile
        if stats['total_nominations'] >= 10:
            facts.append(f"🌟 {person.name} has {stats['total_nominations']} nominations - more than {percentile:.1f}% of all Oscar-nominated individuals!")
        elif stats['total_nominations'] >= 5:
            facts.append(f"⭐ {person.name} has {stats['total_nominations']} nominations, ranking in the top {100-percentile:.1f}% of Oscar nominees!")
        
        # Win rate comparison
        if stats['total_wins'] > 0:
            avg_win_rate = 15  # Approximate overall win rate
            if stats['win_rate'] > avg_win_rate * 2:
                facts.append(f"🎯 With a {stats['win_rate']:.1f}% win rate, {person.name} wins far more often than the typical nominee!")
            elif stats['win_rate'] < 10 and stats['total_nominations'] >= 5:
                facts.append(f"🎲 Despite {stats['total_nominations']} nominations, {person.name}'s {stats['win_rate']:.1f}% win rate shows how competitive the Oscars truly are!")
        
        # First time winner
        if stats['years_to_first_win'] == 0 and stats['total_wins'] > 0:
            facts.append(f"🏆 {person.name} won on their very first nomination - a rare achievement!")
        
        # Long wait
        if stats['years_to_first_win'] and stats['years_to_first_win'] >= 20:
            facts.append(f"⏰ {person.name} waited {stats['years_to_first_win']} ceremonies between first nomination and first win - talk about perseverance!")
        
        # Multiple categories
        if len(stats['categories']) >= 3:
            facts.append(f"🎭 {person.name} has been nominated in {len(stats['categories'])} different categories, showcasing remarkable versatility!")
        
        # Multiple wins
        if stats['total_wins'] >= 4:
            facts.append(f"🏅 {person.name} has won {stats['total_wins']} Oscars - joining the elite club of multiple Oscar winners!")
        
        # No wins but many noms
        if stats['total_wins'] == 0 and stats['total_nominations'] >= 5:
            facts.append(f"💪 {person.name} has {stats['total_nominations']} nominations without a win, demonstrating consistent excellence despite tough competition!")
        
        # Span of career
        if len(stats['years_active']) >= 20:
            try:
                first_year = int(stats['years_active'][0].split('/')[0])
                last_year = int(stats['years_active'][-1].split('/')[0])
                span = last_year - first_year
                facts.append(f"📅 {person.name}'s Oscar journey spans {span}+ years, from {stats['years_active'][0]} to {stats['years_active'][-1]}!")
            except:
                pass
        
        return facts if facts else [f"✨ {person.name} is part of Oscar history!"]


def display_actor_profile(person, stats, wiki_info):
    """Display actor profile card"""
    
    # Header with name
    st.header(f"📊 {person.name}")
    
    # Did You Know? section
    st.subheader("💡 Did You Know?")
    facts = generate_did_you_know(person, stats)
    for fact in facts:
        st.info(fact)
    
    # Two columns for stats and wikipedia
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🏆 Oscar Statistics")
        
        # Key metrics
        metric_cols = st.columns(3)
        with metric_cols[0]:
            st.metric("Nominations", stats['total_nominations'])
        with metric_cols[1]:
            st.metric("Wins", stats['total_wins'])
        with metric_cols[2]:
            st.metric("Win Rate", f"{stats['win_rate']:.1f}%")
        
        # Categories
        st.markdown("**Categories:**")
        for cat in stats['categories']:
            st.write(f"  • {cat}")
        
        # Years active
        if stats['years_active']:
            st.markdown(f"**Years Active:** {stats['years_active'][0]} – {stats['years_active'][-1]}")
        
        # Years to first win
        if stats['years_to_first_win'] is not None:
            if stats['years_to_first_win'] == 0:
                st.markdown("**🎯 Won on first nomination!**")
            else:
                st.markdown(f"**Years to First Win:** {stats['years_to_first_win']} ceremony(s)")
        elif stats['total_wins'] == 0:
            st.markdown("**🏅 No wins yet**")
    
    with col2:
        st.subheader("📖 Wikipedia Info")
        
        if wiki_info and 'error' not in wiki_info:
            # Display image if available
            if wiki_info.get('image'):
                try:
                    st.image(wiki_info['image'], width=300)
                except:
                    pass
            
            # Biography summary
            st.markdown(wiki_info['summary'])
            st.markdown(f"[Read more on Wikipedia]({wiki_info['url']})")
        elif wiki_info and 'error' in wiki_info:
            st.warning(wiki_info['error'])
        else:
            st.info("Wikipedia information not found")
    
    # Films section
    st.subheader("🎬 Nominated Films")
    
    if stats['films']:
        films_data = []
        for (title, year), data in sorted(stats['films'].items(), key=lambda x: x[0][1] if x[0][1] else "", reverse=True):
            films_data.append({
                'Film': title,
                'Year': year if year else "N/A",
                'Nominations': data['nominations'],
                'Wins': data['wins']
            })
        
        st.dataframe(films_data, use_container_width=True, hide_index=True)
    else:
        st.info("No film information available")
    
    # Detailed nominations
    with st.expander("📋 View All Nominations"):
        for nom_data in stats['nominations_list']:
            year, is_winner, category, film, ceremony = nom_data
            status = "🏆 WON" if is_winner else "📌 NOMINATED"
            film_str = f" - {film}" if film else ""
            st.write(f"{status} | {year} | {category}{film_str}")


# Main search logic
if search_button and actor_name:
    with st.spinner(f"Searching for {actor_name}..."):
        # Search in database
        person = search_actor_in_db(actor_name)
        
        if person:
            # Get stats
            stats = get_actor_stats(person)
            
            # Get Wikipedia info
            wiki_info = get_wikipedia_info(actor_name)
            
            # Display profile
            display_actor_profile(person, stats, wiki_info)
        else:
            st.error(f"❌ Actor '{actor_name}' not found in the Oscar database.")
            st.info("Try searching with a different name or check the examples in the sidebar.")

elif not actor_name and search_button:
    st.warning("Please enter an actor name to search.")

# Welcome screen
else:
    st.info("👈 Enter an actor's name in the sidebar to get started!")
    
    # Show some interesting statistics
    st.subheader("📊 Database Statistics")
    
    with db_session:
        total_persons = Person.select().count()
        total_films = Film.select().count()
        total_categories = Category.select().count()
        total_nominations = Nomination.select().count()
        total_wins = sum(1 for nomination in Nomination.select() if nomination.is_winner)
    
    stat_cols = st.columns(5)
    with stat_cols[0]:
        st.metric("Total People", f"{total_persons:,}")
    with stat_cols[1]:
        st.metric("Total Films", f"{total_films:,}")
    with stat_cols[2]:
        st.metric("Categories", f"{total_categories:,}")
    with stat_cols[3]:
        st.metric("Nominations", f"{total_nominations:,}")
    with stat_cols[4]:
        st.metric("Wins", f"{total_wins:,}")
    
    # About section
    st.markdown("""
    ### Oscar Actor Explorer
    
    This interactive application explores Oscar nominations and wins, combining database-driven insights with live Wikipedia data.
    
    **Features:**
    - 🔍 Search any actor or actress by name
    - 📊 View complete Oscar statistics (nominations, wins, categories)
    - 📖 Live Wikipedia integration (biography, photos, birth dates)
    - 💡 Auto-generated "Did You Know?" facts
    - 🎬 Complete filmography of nominated works
    
    **Technology:**
    - **ORM**: PonyORM for database management
    - **API**: Wikipedia Python package for live data
    - **Database**: SQLite with 10,829 nominations from 6,582 unique persons
    
    **Data Coverage:**
    - Oscar ceremonies from 1927/28 to 2024
    - All major categories (Acting, Directing, Writing, Technical)
    - 109 different award categories over Oscar history
    
    """)

# Footer
st.markdown("---")
st.markdown("📚 **Task 2**: Oscar Actor Explorer | Built with PonyORM, Wikipedia API, and Streamlit")

"""
Task 3: Pokémon Battle Arena
A database-driven battle game with cheat code system
"""
import streamlit as st
import sys
import time
import sqlite3
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import from task3 modules directly
from task3.database import (
    ensure_pokemon_database_ready, get_all_pokemon, get_pokemon_by_id,
    cheat_double_hp, cheat_godmode, cheat_steal_strongest, 
    cheat_create_legendary, cheat_nerf_all, cheat_max_stats,
    detect_cheats, get_cheat_log, reset_database,
    get_pokemon_stats_analysis
)
from task3.battle_engine import BattleEngine


def _run_cheat_with_retry(func, *args, max_attempts: int = 4, retry_delay: float = 0.25):
    """Retry transient SQLite lock failures to improve UX under Streamlit reruns."""
    last_error = None
    for attempt in range(max_attempts):
        try:
            return func(*args)
        except sqlite3.OperationalError as err:
            last_error = err
            if "database is locked" not in str(err).lower() or attempt == max_attempts - 1:
                raise
            time.sleep(retry_delay * (attempt + 1))
    raise last_error


def _resolve_team_data(team_ids):
    """Resolve selected IDs to Pokémon rows and identify stale selections."""
    team_data = []
    missing_ids = []

    for pid in team_ids:
        pokemon = get_pokemon_by_id(pid)
        if pokemon is None:
            missing_ids.append(pid)
        else:
            team_data.append(pokemon)

    return team_data, missing_ids

st.set_page_config(
    page_title="Pokémon Battle Arena",
    page_icon="⚔️",
    layout="wide"
)


# Ensure database is ready and display status
if 'pokemon_db_checked' not in st.session_state or not st.session_state.pokemon_db_checked:
    with st.spinner("Checking Pokémon database setup..."):
        _, db_message = ensure_pokemon_database_ready()

    st.success(db_message)

    st.session_state['pokemon_db_checked'] = True




# Session state initialization
if 'battle' not in st.session_state:
    st.session_state.battle = None
if 'team1_ids' not in st.session_state:
    st.session_state.team1_ids = []
if 'team2_ids' not in st.session_state:
    st.session_state.team2_ids = []
if 'battle_log' not in st.session_state:
    st.session_state.battle_log = []
if 'cheats_used' not in st.session_state:
    st.session_state.cheats_used = []

# Title
st.title("⚔️ Pokémon Battle Arena")
st.markdown("*Database-driven battle game with type effectiveness and cheat codes*")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎮 Battle", 
    "👥 Team Selection", 
    "🎲 Cheat Codes", 
    "🔍 Cheat Detection",
    "📊 Analysis"
])

# ============== TAB 1: BATTLE ==============
with tab1:
    st.header("Battle Arena")
    
    if st.session_state.battle is None:
        st.info("👈 Select teams in the **Team Selection** tab to start a battle!")
        
        # Both choose teams before showing battle options
        if len(st.session_state.team1_ids) > 0 and len(st.session_state.team2_ids) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔵 Player 1's Team")
                for pid in st.session_state.team1_ids:
                    pokemon = get_pokemon_by_id(pid)
                    if pokemon:
                        type_display = f"{pokemon['type_1']}/{pokemon['type_2']}" if pokemon.get('type_2') and str(pokemon['type_2']).lower() not in ['none', 'nan', ''] else pokemon['type_1']
                        st.write(f"- **{pokemon['name']}** ({type_display}) - HP: {pokemon['hp']}, ATK: {pokemon['attack']}")
            
            with col2:
                st.subheader("🔴 Player 2's Team")
                for pid in st.session_state.team2_ids:
                    pokemon = get_pokemon_by_id(pid)
                    if pokemon:
                        type_display = f"{pokemon['type_1']}/{pokemon['type_2']}" if pokemon.get('type_2') and str(pokemon['type_2']).lower() not in ['none', 'nan', ''] else pokemon['type_1']
                        st.write(f"- **{pokemon['name']}** ({type_display}) - HP: {pokemon['hp']}, ATK: {pokemon['attack']}")
            
            if st.button("⚔️ Start Battle!", type="primary", use_container_width=True):
                # Get Pokémon data and clean up stale selections.
                team1_data, missing_team1 = _resolve_team_data(st.session_state.team1_ids)
                team2_data, missing_team2 = _resolve_team_data(st.session_state.team2_ids)

                if missing_team1:
                    st.session_state.team1_ids = [pid for pid in st.session_state.team1_ids if pid not in missing_team1]
                if missing_team2:
                    st.session_state.team2_ids = [pid for pid in st.session_state.team2_ids if pid not in missing_team2]

                if missing_team1 or missing_team2:
                    missing = missing_team1 + missing_team2
                    st.warning(f"Removed unavailable Pokémon from teams (IDs: {', '.join(map(str, missing))}). Please review teams and start again.")
                    st.rerun()

                try:
                    # Create battle
                    st.session_state.battle = BattleEngine(team1_data, team2_data)
                    st.session_state.battle_log = []
                    st.rerun()
                except ValueError as err:
                    st.error(f"Cannot start battle: {err}")
    
    else:
        # Battle in progress
        battle = st.session_state.battle
        
        # Display team status
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔵 Player 1's Team")
            st.text(battle.get_team_status(battle.team1))
        
        with col2:
            st.subheader("🔴 Player 2's Team")
            st.text(battle.get_team_status(battle.team2))
        
        st.markdown("---")
        
        # Battle controls
        if not battle.is_battle_over():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                if st.button("⚔️ Execute Turn", type="primary", use_container_width=True):
                    turn_log = battle.execute_turn()
                    st.session_state.battle_log.extend(turn_log)
                    st.rerun()
            
            with col2:
                if st.button("⏩ Auto Battle", use_container_width=True):
                    while not battle.is_battle_over() and battle.turn_number < 50:
                        turn_log = battle.execute_turn()
                        st.session_state.battle_log.extend(turn_log)
                    st.rerun()
            
            with col3:
                if st.button("🔄 Reset", use_container_width=True):
                    st.session_state.battle = None
                    st.session_state.battle_log = []
                    st.rerun()
        
        else:
            # Battle over
            st.success(f"🏆 **{battle.winner} WINS!**")
            
            summary = battle.get_battle_summary()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Turns", summary['turns'])
            with col2:
                st.metric("Player 1 Remaining", summary['team1_remaining'])
            with col3:
                st.metric("Player 2 Remaining", summary['team2_remaining'])
            
            if st.button("🔄 New Battle", type="primary", use_container_width=True):
                st.session_state.battle = None
                st.session_state.battle_log = []
                st.rerun()
        
        # Battle log
        if st.session_state.battle_log:
            st.markdown("---")
            st.subheader("📜 Battle Log")
            
            with st.expander("Show Full Battle Log", expanded=False):
                for log_entry in st.session_state.battle_log:
                    st.text(log_entry)

# ============== TAB 2: TEAM SELECTION ==============
with tab2:
    st.header("Team Selection")
    st.markdown("Select 1-3 Pokémon for each team. All stats are loaded from the database.")
    
    # Load all Pokémon
    all_pokemon = get_all_pokemon(limit=200)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔵 Player 1's Team")
        
        # Search filter
        search1 = st.text_input("Search Pokémon (Player 1)", key="search1")
        
        filtered_pokemon1 = all_pokemon
        if search1:
            filtered_pokemon1 = [p for p in all_pokemon if search1.lower() in p['name'].lower()]
        
        # Display selection
        for idx, pokemon in enumerate(filtered_pokemon1[:20]):  # Show first 20
            col_check, col_info = st.columns([1, 4])
            
            with col_check:
                is_selected = pokemon['id'] in st.session_state.team1_ids
                if st.checkbox(
                    f"Select {pokemon['name']} for Player 1",
                    value=is_selected,
                    key=f"p1_{pokemon['id']}_{idx}",
                    label_visibility="collapsed",
                ):
                    if pokemon['id'] not in st.session_state.team1_ids and len(st.session_state.team1_ids) < 3:
                        st.session_state.team1_ids.append(pokemon['id'])
                        st.rerun()
                else:
                    if pokemon['id'] in st.session_state.team1_ids:
                        st.session_state.team1_ids.remove(pokemon['id'])
                        st.rerun()
            
            with col_info:
                type_display = f"{pokemon['type_1']}/{pokemon['type_2']}" if pokemon.get('type_2') and str(pokemon['type_2']).lower() not in ['none', 'nan', ''] else pokemon['type_1']
                st.write(f"**{pokemon['name']}** - {type_display} - Total: {pokemon['total']}")
                st.caption(f"HP: {pokemon['hp']} | ATK: {pokemon['attack']} | DEF: {pokemon['defense']} | SPD: {pokemon['speed']}")
        
        if len(st.session_state.team1_ids) >= 3:
            st.warning("⚠️ Maximum 3 Pokémon per team")
        
        if st.button("🗑️ Clear Team 1", use_container_width=True):
            st.session_state.team1_ids = []
            st.rerun()
    
    with col2:
        st.subheader("🔴 Player 2's Team")
        
        # Search filter
        search2 = st.text_input("Search Pokémon (Player 2)", key="search2")
        
        filtered_pokemon2 = all_pokemon
        if search2:
            filtered_pokemon2 = [p for p in all_pokemon if search2.lower() in p['name'].lower()]
        
        # Display selection
        for idx, pokemon in enumerate(filtered_pokemon2[:20]):  # Show first 20
            col_check, col_info = st.columns([1, 4])
            
            with col_check:
                is_selected = pokemon['id'] in st.session_state.team2_ids
                if st.checkbox(
                    f"Select {pokemon['name']} for Player 2",
                    value=is_selected,
                    key=f"p2_{pokemon['id']}_{idx}",
                    label_visibility="collapsed",
                ):
                    if pokemon['id'] not in st.session_state.team2_ids and len(st.session_state.team2_ids) < 3:
                        st.session_state.team2_ids.append(pokemon['id'])
                        st.rerun()
                else:
                    if pokemon['id'] in st.session_state.team2_ids:
                        st.session_state.team2_ids.remove(pokemon['id'])
                        st.rerun()
            
            with col_info:
                type_display = f"{pokemon['type_1']}/{pokemon['type_2']}" if pokemon.get('type_2') and str(pokemon['type_2']).lower() not in ['none', 'nan', ''] else pokemon['type_1']
                st.write(f"**{pokemon['name']}** - {type_display} - Total: {pokemon['total']}")
                st.caption(f"HP: {pokemon['hp']} | ATK: {pokemon['attack']} | DEF: {pokemon['defense']} | SPD: {pokemon['speed']}")
        
        if len(st.session_state.team2_ids) >= 3:
            st.warning("⚠️ Maximum 3 Pokémon per team")
        
        if st.button("🗑️ Clear Team 2", use_container_width=True):
            st.session_state.team2_ids = []
            st.rerun()

# ============== TAB 3: CHEAT CODES ==============
with tab3:
    st.header("🎲 Cheat Codes")
    st.markdown("""
    Enter cheat codes to modify the database and gain unfair advantages!
    
    **All cheats execute real SQL UPDATE/INSERT queries on the database.**
    """)
    
    st.warning("⚠️ Cheats will be logged and can be detected via SQL audit queries!")
    
    cheat_code_raw = st.text_input("Enter Cheat Code", placeholder="Type cheat code here...")
    # Normalize user input to avoid false negatives caused by spaces/dashes/case differences.
    cheat_code = "".join(ch for ch in cheat_code_raw.upper() if ch.isalnum())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Available Cheat Codes")
        st.markdown("""
        - **UPUPDOWNDOWN** - Double HP (UPDATE)
        - **GODMODE** - Defense/Sp.Def = 999 (UPDATE)
        - **MAXPOWER** - All stats = 255 (UPDATE)
        - **STEAL** - Copy strongest Pokémon (INSERT)
        - **LEGENDARY** - Create custom OP Pokémon (INSERT)
        - **NERF** - Reduce opponent stats by 50% (UPDATE)
        """)
    
    with col2:
        st.subheader("Target Team")
        target_player = st.radio("Apply cheat to:", ["Player 1", "Player 2"], key="cheat_target")
    
    if st.button("🚀 Activate Cheat", type="primary", use_container_width=True):
        target_ids = st.session_state.team1_ids if target_player == "Player 1" else st.session_state.team2_ids
        exclude_ids = st.session_state.team2_ids if target_player == "Player 1" else st.session_state.team1_ids

        if not cheat_code:
            st.error("Please enter a cheat code first.")
            st.stop()

        try:
            if cheat_code == "UPUPDOWNDOWN":
                if target_ids:
                    message = _run_cheat_with_retry(cheat_double_hp, target_ids)
                    st.success(message)
                    st.session_state.cheats_used.append(cheat_code)
                else:
                    st.error("No team selected!")
            
            elif cheat_code == "GODMODE":
                if target_ids:
                    message = _run_cheat_with_retry(cheat_godmode, target_ids)
                    st.success(message)
                    st.session_state.cheats_used.append(cheat_code)
                else:
                    st.error("No team selected!")
            
            elif cheat_code == "MAXPOWER":
                if target_ids:
                    message = _run_cheat_with_retry(cheat_max_stats, target_ids)
                    st.success(message)
                    st.session_state.cheats_used.append(cheat_code)
                else:
                    st.error("No team selected!")
            
            elif cheat_code == "STEAL":
                message, new_id = _run_cheat_with_retry(cheat_steal_strongest, target_ids if target_ids else [])
                st.success(message)
                if new_id:
                    if target_player == "Player 1" and len(st.session_state.team1_ids) < 3:
                        st.session_state.team1_ids.append(new_id)
                    elif target_player == "Player 2" and len(st.session_state.team2_ids) < 3:
                        st.session_state.team2_ids.append(new_id)
                    st.session_state.cheats_used.append(cheat_code)
            
            elif cheat_code == "LEGENDARY":
                custom_name = st.text_input("Legendary Name", value="HACKER", key="legendary_name")
                message, new_id = _run_cheat_with_retry(cheat_create_legendary, custom_name if custom_name else "HACKER")
                st.success(message)
                if target_player == "Player 1" and len(st.session_state.team1_ids) < 3:
                    st.session_state.team1_ids.append(new_id)
                elif target_player == "Player 2" and len(st.session_state.team2_ids) < 3:
                    st.session_state.team2_ids.append(new_id)
                st.session_state.cheats_used.append(cheat_code)
            
            elif cheat_code == "NERF":
                message = _run_cheat_with_retry(cheat_nerf_all, exclude_ids if exclude_ids else [1])
                st.success(message)
                st.session_state.cheats_used.append(cheat_code)
            
            else:
                st.error(f"Invalid cheat code: {cheat_code_raw}")
        except sqlite3.OperationalError as err:
            if "database is locked" in str(err).lower():
                st.error("Database is busy right now. Please wait a second and try again.")
            else:
                st.error(f"Cheat execution failed: {err}")
            st.stop()
    
    # Show used cheats
    if st.session_state.cheats_used:
        st.markdown("---")
        st.subheader("Used Cheats This Session")
        st.write(", ".join(st.session_state.cheats_used))

# ============== TAB 4: CHEAT DETECTION ==============
with tab4:
    st.header("🔍 Cheat Detection & Audit")
    st.markdown("SQL queries to detect abnormal stats and database modifications.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔎 Scan for Anomalies", type="primary", use_container_width=True):
            anomalies = detect_cheats()
            
            if anomalies:
                st.error(f"⚠️ Found {len(anomalies)} suspicious entries!")
                
                for anomaly in anomalies:
                    with st.expander(f"🚨 {anomaly['type']} - {anomaly['pokemon']}"):
                        st.write(anomaly['details'])
            else:
                st.success("✅ No anomalies detected. Database appears clean.")
    
    with col2:
        if st.button("📜 View Cheat Log", use_container_width=True):
            cheat_log = get_cheat_log()
            
            if cheat_log:
                st.info(f"Found {len(cheat_log)} logged cheats")
                
                for entry in cheat_log:
                    st.write(f"**{entry['cheat_code']}** - {entry['pokemon_affected']}")
                    st.caption(f"{entry['description']} | {entry['timestamp']}")
                    st.markdown("---")
            else:
                st.info("No cheats logged yet.")
    
    st.markdown("---")
    st.subheader("SQL Queries Used for Detection")
    
    st.code("""
-- Detect impossible stats (> 255)
SELECT name, hp, attack, defense, sp_atk, sp_def, speed
FROM pokemon
WHERE hp > 255 OR attack > 255 OR defense > 255
   OR sp_atk > 255 OR sp_def > 255 OR speed > 255;

-- Detect custom Pokémon
SELECT name, total FROM pokemon WHERE is_custom = 1;

-- Detect GODMODE (Defense = 999)
SELECT name, defense, sp_def FROM pokemon
WHERE defense = 999 OR sp_def = 999;

-- View cheat log
SELECT * FROM cheat_log ORDER BY timestamp DESC;
    """, language="sql")
    
    # Reset database
    st.markdown("---")
    st.subheader("⚠️ Danger Zone")
    
    if st.button("🔄 Reset Database (Remove All Cheats)", type="secondary"):
        message = reset_database()
        st.success(message)
        st.session_state.battle = None
        st.session_state.team1_ids = []
        st.session_state.team2_ids = []
        st.session_state.cheats_used = []
        st.rerun()

# ============== TAB 5: ANALYSIS ==============
with tab5:
    st.header("📊 Pokémon Dataset Analysis")
    st.markdown("Interesting insights from SQL/ORM queries on the Pokémon dataset.")
    
    analysis = get_pokemon_stats_analysis()
    
    # Top type combinations
    st.subheader("🔥 Most Overpowered Type Combinations")
    st.markdown("*Average total stats by type combination (min 3 Pokémon)*")
    
    for combo in analysis['top_type_combos']:
        st.write(f"**{combo['types']}** - Avg Total: {combo['avg_total']} (Max: {combo['max_total']}, Count: {combo['count']})")
    
    st.markdown("---")
    
    # Power creep by generation
    st.subheader("📈 Power Creep Across Generations")
    st.markdown("*Is there statistical evidence of power creep?*")
    
    import pandas as pd
    df_gen = pd.DataFrame(analysis['generation_stats'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(df_gen[['generation', 'count', 'avg_total']], use_container_width=True)
    
    with col2:
        import plotly.express as px
        fig = px.line(df_gen, x='generation', y='avg_total', 
                      title='Average Total Stats by Generation',
                      markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Analysis
    avg_change = df_gen['avg_total'].diff().mean()
    if avg_change > 5:
        st.info(f"📊 **Finding**: Stats increase by ~{avg_change:.1f} points per generation on average, suggesting power creep exists!")
    else:
        st.info(f"📊 **Finding**: Stats remain relatively stable across generations (avg change: {avg_change:.1f} points)")
    
    st.markdown("---")
    
    # Weakest legendary
    st.subheader("🦄 Weakest Legendary Pokémon")
    
    if 'weakest_legendary' in analysis:
        weak = analysis['weakest_legendary']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Name", weak['name'])
        with col2:
            st.metric("Total Stats", weak['total'])
        with col3:
            st.metric("Type", weak['types'])
        
        st.info(f"📊 **Finding**: {weak['name']} from Generation {weak['generation']} is the weakest legendary with only {weak['total']} total stats!")
    
    st.markdown("---")
    
    # SQL Queries Used
    st.subheader("SQL Queries Used")
    
    with st.expander("Show Analysis Queries"):
        st.code("""
-- Most overpowered type combinations
SELECT 
    type_1, type_2, COUNT(*) as count,
    AVG(total) as avg_total, MAX(total) as max_total
FROM pokemon
WHERE is_custom = 0
GROUP BY type_1, type_2
HAVING COUNT(*) >= 3
ORDER BY avg_total DESC
LIMIT 5;

-- Power creep by generation
SELECT 
    generation, COUNT(*) as count,
    AVG(total) as avg_total,
    AVG(hp) as avg_hp,
    AVG(attack) as avg_attack,
    AVG(speed) as avg_speed
FROM pokemon
WHERE is_custom = 0
GROUP BY generation
ORDER BY generation;

-- Weakest legendary
SELECT name, total, type_1, type_2, generation
FROM pokemon
WHERE is_legendary = 1 AND is_custom = 0
ORDER BY total ASC
LIMIT 1;
        """, language="sql")


# # Footer
# st.markdown("---")
# st.markdown("""
# ### 🎓 Task 3 Documentation

# **Database Schema**:
# - `pokemon` table: All Pokémon stats from CSV
# - `type_effectiveness` table: Type matchup multipliers
# - `battle_history` table: Battle results log
# - `cheat_log` table: Audit trail for cheats

# **Battle Mechanics**:
# - Turn order determined by Speed stat
# - Damage formula: `(Attack * Power / Defense) * Type_Effectiveness * Random(0.85-1.0)`
# - Type effectiveness from database (2x super effective, 0.5x not very effective, 0x immune)

# **Cheat System**:
# - All cheats execute real SQL operations (UPDATE/INSERT/DELETE)
# - Cheat detection via SQL queries for abnormal values
# - Audit log tracks all modifications

# **Technology**: SQLite3 (raw SQL), Streamlit, Pandas, Plotly
# """)

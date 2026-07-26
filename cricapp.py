import streamlit as st
import json
import os

# File to store data persistently
DATA_FILE = "club_data.json"

# Load data from JSON file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"team_achievements": [], "players": {}}

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Initialize data in session state
if "club_data" not in st.session_state:
    st.session_state.club_data = load_data()

data = st.session_state.club_data

# App Styling
st.set_page_config(page_title="Cricket Club Manager", page_icon="🏏", layout="wide")
st.title("🏏 Cricket Club Dashboard")
st.markdown("Manage player roles, match performances, milestones, and team achievements.")

# Sidebar Navigation
menu = st.sidebar.radio("Navigation Menu", [
    "🏆 Club Summary", 
    "➕ Add New Player", 
    "🏏 Record Match Performance", 
    "🎖️ Add Milestones & Team Glory"
])

# ----------------------------------------------------
# MENU 1: CLUB SUMMARY
# ----------------------------------------------------
if menu == "🏆 Club Summary":
    st.header("📋 Club Overview")
    
    # Team Achievements Section
    st.subheader("Team Achievements")
    if data["team_achievements"]:
        for achievement in data["team_achievements"]:
            st.markdown(f"- 🏆 **{achievement}**")
    else:
        st.info("No team achievements recorded yet.")
        
    st.divider()
    
    # Player Profiles Section
    st.subheader("👥 Squad Roster & Statistics")
    if not data["players"]:
        st.info("No players registered yet. Use the sidebar to add players.")
    else:
        # Create columns to display players cleanly
        for name, profile in data["players"].items():
            with st.expander(f"👤 {name} - {profile['role']}"):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Matches", profile["matches_played"])
                col2.metric("Total Runs", profile["runs_scored"])
                col3.metric("Wickets", profile["wickets_taken"])
                col4.metric("Catches", profile["catches"])
                
                st.markdown("**Personal Milestones:**")
                if profile["milestones"]:
                    for ms in profile["milestones"]:
                        st.markdown(f"- ⭐ {ms}")
                else:
                    st.caption("No individual milestones yet.")

# ----------------------------------------------------
# MENU 2: ADD NEW PLAYER
# ----------------------------------------------------
elif menu == "➕ Add New Player":
    st.header("➕ Register a New Player")
    with st.form("add_player_form"):
        player_name = st.text_input("Player Full Name").strip()
        player_role = st.selectbox("Player Role", [
            "Top-order Batsman", 
            "Middle-order Batsman", 
            "Fast Bowler", 
            "Spin Bowler", 
            "All-rounder", 
            "Wicket-keeper Batsman"
        ])
        submit = st.form_submit_button("Add Player to Roster")
        
        if submit:
            if not player_name:
                st.error("Please enter a valid player name.")
            elif player_name in data["players"]:
                st.warning(f"'{player_name}' is already in the roster.")
            else:
                data["players"][player_name] = {
                    "role": player_role,
                    "matches_played": 0,
                    "runs_scored": 0,
                    "wickets_taken": 0,
                    "catches": 0,
                    "milestones": []
                }
                save_data(data)
                st.success(f"Successfully added {player_name} to the team!")

# ----------------------------------------------------
# MENU 3: RECORD MATCH PERFORMANCE
# ----------------------------------------------------
elif menu == "🏏 Record Match Performance":
    st.header("🏏 Update Match Stats")
    if not data["players"]:
        st.warning("Please add players to the club first before recording match statistics.")
    else:
        with st.form("performance_form"):
            selected_player = st.selectbox("Select Player", list(data["players"].keys()))
            
            col1, col2, col3 = st.columns(3)
            runs = col1.number_input("Runs Scored This Match", min_value=0, step=1, value=0)
            wickets = col2.number_input("Wickets Taken This Match", min_value=0, step=1, value=0)
            catches = col3.number_input("Catches Taken This Match", min_value=0, step=1, value=0)
            
            submit = st.form_submit_button("Update Player Statistics")
            
            if submit:
                # Accumulate the statistics
                player = data["players"][selected_player]
                player["matches_played"] += 1
                player["runs_scored"] += runs
                player["wickets_taken"] += wickets
                player["catches"] += catches
                
                save_data(data)
                st.success(f"Updated stats for {selected_player}!")

# ----------------------------------------------------
# MENU 4: ADD MILESTONES & TEAM GLORY
# ----------------------------------------------------
elif menu == "🎖️ Add Milestones & Team Glory":
    st.header("🎖️ Record Milestones and Trophies")
    
    # Sub-form A: Player Milestone
    st.subheader("Add Individual Player Milestone")
    if not data["players"]:
        st.caption("Add players first to assign personal milestones.")
    else:
        with st.form("milestone_form"):
            m_player = st.selectbox("Select Player for Milestone", list(data["players"].keys()))
            milestone_text = st.text_input("Milestone (e.g., 'Scored a Century against rival club')").strip()
            m_submit = st.form_submit_button("Save Player Milestone")
            
            if m_submit and milestone_text:
                data["players"][m_player]["milestones"].append(milestone_text)
                save_data(data)
                st.success(f"Added milestone for {m_player}!")

    st.divider()
    
    # Sub-form B: Team Achievement
    st.subheader("Add Club/Team Achievement")
    with st.form("team_achievement_form"):
        team_achievement = st.text_input("Team Glory (e.g., 'Won the Local T20 League Tournament')").strip()
        t_submit = st.form_submit_button("Save Team Achievement")
        
        if t_submit and team_achievement:
            data["team_achievements"].append(team_achievement)
            save_data(data)
            st.success("Team achievement saved successfully!")

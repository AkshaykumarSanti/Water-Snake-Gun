import streamlit as st
import random

# --- Page Setup ---
st.set_page_config(
    page_title="Snake Water Gun Game",
    page_icon="🐍",
    layout="centered"
)

# --- Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Logic & Data Structures ---
# 1 for Snake, -1 for Water, 0 for Gun
options_map = {
    "Snake 🐍": 1,
    "Water 💧": -1,
    "Gun 🔫": 0
}
reverse_map = {1: "🐍 Snake", -1: "💧 Water", 0: "🔫 Gun"}

def get_winner(player, computer):
    """
    Returns: 0 for Draw, 1 for Player Win, -1 for Player Loss
    """
    if player == computer:
        return 0
    
    # Logic: 
    # Snake (1) beats Water (-1)
    # Water (-1) beats Gun (0)
    # Gun (0) beats Snake (1)
    win_conditions = [
        (player == 1 and computer == -1),
        (player == -1 and computer == 0),
        (player == 0 and computer == 1)
    ]
    
    return 1 if any(win_conditions) else -1

# --- UI Components ---
st.title("🐍 Snake Water Gun")
st.write("A classic game of strategy and luck!")

# Sidebar for Score and Rules
with st.sidebar:
    st.header("Rules")
    st.markdown("""
    - **Snake** drinks **Water** (Win)
    - **Water** rusts **Gun** (Win)
    - **Gun** kills **Snake** (Win)
    """)
    st.divider()
    if st.button("Reset Game Session"):
        st.session_state.clear()
        st.rerun()

# Initialize Session State for Player Name
if "player_name" not in st.session_state:
    st.session_state.player_name = ""

# Step 1: Get Player Name
if not st.session_state.player_name:
    with st.form("name_form"):
        name_input = st.text_input("Enter your Name to start:", placeholder="Ex: Rahul")
        submit_name = st.form_submit_button("Start Playing")
        if submit_name and name_input:
            st.session_state.player_name = name_input
            st.rerun()
else:
    # Step 2: Main Game Interface
    st.write(f"Hello **{st.session_state.player_name}**! Choose your move:")
    
    # Create three columns for buttons
    col1, col2, col3 = st.columns(3)
    
    player_choice = None
    
    if col1.button("Snake 🐍"):
        player_choice = 1
    if col2.button("Water 💧"):
        player_choice = -1
    if col3.button("Gun 🔫"):
        player_choice = 0

    # Game Result Processing
    if player_choice is not None:
        computer_choice = random.choice([1, -1, 0])
        
        st.divider()
        
        # Displaying choices side by side
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.info(f"**Your Choice:**\n\n{reverse_map[player_choice]}")
        with res_col2:
            st.warning(f"**Computer's Choice:**\n\n{reverse_map[computer_choice]}")
            
        result = get_winner(player_choice, computer_choice)
        
        st.markdown("### Result:")
        if result == 0:
            st.info(f"🤝 It's a Draw, {st.session_state.player_name}!")
        elif result == 1:
            st.success(f"🎉 {st.session_state.player_name} Wins!!")
            st.balloons()
        else:
            st.error(f"😢 {st.session_state.player_name} Lost! Better luck next time.")
            
    st.write("\n")
    if st.button("Change Name"):
        st.session_state.player_name = ""
        st.rerun()
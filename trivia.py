import streamlit as st
from random import shuffle

st.set_page_config(page_title="SAIT Cybersecurity CTF Jeopardy", layout="wide")

# ---------- Styling (Retro Computer vibes) ----------
st.markdown(
    """
    <style>
    /* App background & retro font */
    .stApp { background: linear-gradient(180deg, #001100 0%, #003300 40%, #000800 100%); color: #00ff00; font-family: 'Courier New', 'Lucida Console', monospace; }
    .retro-title { font-size:34px; font-weight:800; color:#00ff00; text-shadow: 0 2px 0 #004400; animation: flicker 2s infinite alternate; }
    .subtitle { color: #ffaa00; margin-bottom:8px; font-style: italic; }

    /* Flicker effect for title */
    @keyframes flicker {
        0%, 18%, 22%, 25%, 53%, 57%, 100% { opacity: 1; }
        20%, 24%, 55% { opacity: 0.4; }
    }

    /* Category column */
    .category { background: linear-gradient(180deg,#002200,#001100); padding:10px; border-radius:6px; text-align:center; box-shadow: 0 0 10px #00ff00; border:1px solid #00aa00; }
    .category h3 { margin: 0; color:#00ff00; text-transform: uppercase; letter-spacing: 2px; }

    /* Buttons (tiles) */
    .stButton>button {
        background: linear-gradient(180deg,#004400,#002200);
        color:#00ff00; padding:12px 10px; border-radius:4px; font-weight:800; border:2px solid #00aa00; box-shadow: 0 0 8px rgba(0,255,0,0.3);
        font-family: 'Courier New', monospace; text-transform: uppercase;
    }
    .stButton>button:hover { box-shadow: 0 0 15px #00ff00; transform: none; }
    .stButton>button[disabled] { background: linear-gradient(180deg,#333333,#111111); color:#666; border-color:#444; box-shadow: none; }

    .question-box { background: linear-gradient(180deg,#001100,#000800); padding:16px; border-radius:6px; border:1px solid #00aa00; box-shadow: 0 0 8px rgba(0,255,0,0.2); }
    .answer { color:#ffaa00; font-weight:800; font-size:18px; font-family: 'Courier New', monospace; }

    /* Team chips in sidebar */
    .team-chip { display:inline-block; padding:6px 10px; margin:4px 6px; border-radius:4px; background:linear-gradient(90deg,#002200,#004400); color:#00ff00; font-weight:700; border: 1px solid #00aa00; }
    .muted { color:#888888 }

    /* Sidebar styling */
    .css-1d391kg, .css-18e3th9, section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001100 0%, #002200 100%);
        border-right: 2px solid #00aa00;
        box-shadow: 2px 0 10px rgba(0, 255, 0, 0.2);
    }
    
    /* Sidebar text and headers */
    .css-1d391kg .markdown-text-container, section[data-testid="stSidebar"] .markdown-text-container,
    .css-1d391kg h2, section[data-testid="stSidebar"] h2,
    .css-1d391kg h3, section[data-testid="stSidebar"] h3,
    .css-1d391kg p, section[data-testid="stSidebar"] p,
    .css-1d391kg label, section[data-testid="stSidebar"] label {
        color: #00ff00 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Sidebar expander */
    .css-1d391kg .streamlit-expanderHeader, section[data-testid="stSidebar"] .streamlit-expanderHeader {
        background: linear-gradient(90deg, #002200, #003300);
        border: 1px solid #00aa00;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Sidebar input fields */
    .css-1d391kg .stTextInput input, section[data-testid="stSidebar"] .stTextInput input,
    .css-1d391kg .stSelectbox select, section[data-testid="stSidebar"] .stSelectbox select {
        background: #001100;
        border: 1px solid #00aa00;
        color: #00ff00;
        font-family: 'Courier New', monospace;
    }
    
    /* Sidebar buttons */
    .css-1d391kg .stButton button, section[data-testid="stSidebar"] .stButton button {
        background: linear-gradient(180deg, #003300, #001100);
        border: 1px solid #00aa00;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 1px;
    }
    
    .css-1d391kg .stButton button:hover, section[data-testid="stSidebar"] .stButton button:hover {
        box-shadow: 0 0 8px #00ff00;
        border-color: #00ff00;
    }

    /* Retro scan lines effect */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0, 255, 0, 0.03) 2px,
            rgba(0, 255, 0, 0.03) 4px
        );
        pointer-events: none;
        z-index: 1000;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="retro-title">SAIT CYBERSECURITY CTF JEOPARDY</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Deploy teams, execute security queries, and capture flags for correct exploits.</div>', unsafe_allow_html=True)

# ---------- Questions bank (category -> point_value -> (question, answer)) ----------
QUESTIONS = {
    "Trojan Territory": {
        100: ("What does 'SAIT' stand for?", "Southern Alberta Institute of Technology"),
        300: ("What building on campus hosts most IT and cybersecurity classes?", "A-Wing / Aldred Centre"),
        500: ("What's the name of SAIT's student cybersecurity club or team?", "SAITSEC / SAIT Cyber Security Club"),
        700: ("SAIT's mascot, a Trojan, symbolizes what ancient civilization?", "Greek / Trojan civilization"),
        1000: ("SAIT's official CTF team once competed in which national-level cyber event?", "Canadian Cyber Defence Challenge")
    },
    "Cyber Frontlines": {
        100: ("What does 'VPN' stand for?", "Virtual Private Network"),
        300: ("Which cybersecurity framework is known by the acronym 'NIST'?", "National Institute of Standards and Technology"),
        500: ("What kind of attack floods a system with traffic to crash it?", "DDoS"),
        700: ("What's the term for secretly exploiting a vulnerability before it's patched?", "Zero-day"),
        1000: ("Name the 2017 ransomware attack that crippled global systems using a Windows SMB flaw.", "WannaCry")
    },
    "Life in Wasteland": {
        100: ("What are bottle caps used for in Fallout?", "Currency"),
        300: ("What's the name of the blue jumpsuit worn by Vault dwellers?", "Vault Suit"),
        500: ("In Fallout 4, which faction controls synths and advanced tech?", "The Institute"),
        700: ("What year did The Great War begin and end?", "October 23, 2077"),
        1000: ("Who was the founder of the Brotherhood of Steel?", "Roger Maxson")
    },
    "Pop Culture Hacked": {
        100: ("In The Matrix, what color pill does Neo take?", "Red pill"),
        300: ("What 1995 movie features the line 'Hack the Planet!'?", "Hackers"),
        500: ("Which Marvel hero is also a world-class hacker and inventor?", "Tony Stark / Iron Man"),
        700: ("What's the name of the hacker group in Mr. Robot?", "fsociety"),
        1000: ("In Watch Dogs, what device does Aiden Pearce use to hack the city?", "Smartphone")
    },
    "Human Exploits": {
        100: ("What's the act of tricking people into revealing info called?", "Phishing"),
        300: ("What's 'tailgating' in a security context?", "Following someone into a secure area"),
        500: ("What's the difference between phishing and spear phishing?", "Spear = targeted"),
        700: ("What famous 1990s hacker was known for phone-based social engineering?", "Kevin Mitnick"),
        1000: ("What psychological principle makes people more likely to comply with fake authority?", "Authority bias")
    },
    "Tech Lore & History": {
        100: ("What does 'WWW' stand for?", "World Wide Web"),
        300: ("What year was the first iPhone released?", "2007"),
        500: ("What was the name of the first computer virus?", "Brain"),
        700: ("Who is known as the father of computing?", "Charles Babbage"),
        1000: ("What did the 'ILOVEYOU' virus of 2000 disguise itself as?", "A love letter email attachment")
    }
}

# ---------- Session state initialization ----------
if "teams" not in st.session_state:
    st.session_state.teams = []  # list of {'name':str,'score':int}
if "board_state" not in st.session_state:
    # track which tiles have been revealed: (category, point_value) -> bool
    st.session_state.board_state = {(cat, points): False for cat in QUESTIONS.keys() for points in QUESTIONS[cat].keys()}
if "current" not in st.session_state:
    st.session_state.current = None  # (category, point_value)

# ---------- Team manager ----------
with st.sidebar.expander("TERMINAL: Teams & Memory", expanded=True):
    st.write("## > ACTIVE_TEAMS.exe")
    with st.form("add_team"):
        new_name = st.text_input("Initialize new team:")
        submitted = st.form_submit_button(">> EXECUTE")
        if submitted and new_name.strip():
            st.session_state.teams.append({"name": new_name.strip(), "score": 0})
    if st.session_state.teams:
        for idx, t in enumerate(st.session_state.teams):
            cols = st.columns((3,1,1))
            cols[0].markdown(f"<span class='team-chip'>{t['name']}</span>", unsafe_allow_html=True)
            cols[1].markdown(f"**{t['score']}**")
            if cols[2].button("DEL", key=f"remove_{idx}"):
                st.session_state.teams.pop(idx)
                st.rerun()

    st.write("---")
    st.write("### > SYSTEM_CONTROL.exe")
    if st.button("CLEAR MEMORY"):
        for t in st.session_state.teams:
            t['score'] = 0
    if st.button("DEFRAG DATABASE"):
        # shuffle is not applicable to the new structure, but we can keep the button for UI consistency
        st.info("Database optimized!")
    if st.button("FORMAT C:\\ (RESET)"):
        st.session_state.board_state = {(cat, points): False for cat in QUESTIONS.keys() for points in QUESTIONS[cat].keys()}
        st.session_state.current = None
        st.rerun()

# ---------- Helper functions ----------

def show_question(category, points):
    q, a = QUESTIONS[category][points]
    st.session_state.current = (category, points)
    st.session_state.board_state[(category, points)] = True
    # small UX: when a question is revealed we re-run so the board reflects the spent tile
    st.rerun()

# ---------- Game board UI ----------
categories = list(QUESTIONS.keys())
point_values = [100, 300, 500, 700, 1000]

cols = st.columns(len(categories))
for col_idx, category in enumerate(categories):
    with cols[col_idx]:
        st.markdown(f"<div class='category'><h3>{category}</h3></div>", unsafe_allow_html=True)
        for points in point_values:
            revealed = st.session_state.board_state.get((category, points), False)
            if revealed:
                st.button("—", key=f"spent_{category}_{points}", disabled=True)
            else:
                if st.button(f"{points}", key=f"btn_{category}_{points}"):
                    show_question(category, points)

st.write("---")

# Progress / remaining tiles indicator
total_tiles = len(categories) * len(point_values)
revealed = sum(1 for v in st.session_state.board_state.values() if v)
remaining = total_tiles - revealed
progress = revealed / total_tiles if total_tiles else 0
st.write(f"**System status:** {revealed} processed / {total_tiles} total — remaining: {remaining}")
st.progress(progress)


# ---------- Question panel ----------
if st.session_state.current:
    category, points = st.session_state.current
    q, a = QUESTIONS[category][points]
    st.markdown(f"<div class='question-box'><h3>Query from {category} ({points} pts)</h3><p>{q}</p></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([3,1])
    with col1:
        if st.button("Execute Debug"):
            st.markdown(f"<div class='answer'>Output: {a}</div>", unsafe_allow_html=True)
    with col2:
        if st.session_state.teams:
            team_names = [t['name'] for t in st.session_state.teams]
            pick = st.selectbox("Allocate points to", options=team_names)
            award_col1, award_col2 = st.columns(2)
            if award_col1.button("Correct"):
                # add points
                for t in st.session_state.teams:
                    if t['name'] == pick:
                        t['score'] += points
                        break
                # celebration for correct answer
                try:
                    st.balloons()
                except Exception:
                    pass
                st.session_state.current = None
                st.rerun()
            if award_col2.button("Error"):
                # optionally subtract
                for t in st.session_state.teams:
                    if t['name'] == pick:
                        t['score'] -= points  # simple penalty rule
                        break
                st.session_state.current = None
                st.rerun()
        else:
            st.info("Initialize teams in the sidebar to allocate memory points")

# ---------- Footer & controls ----------
st.write("\n---\n")
if st.button("Reboot System (new round)"):
    # mark board items as not-spent so they can be reused in new round
    st.session_state.board_state = {(cat, points): False for cat in QUESTIONS.keys() for points in QUESTIONS[cat].keys()}
    st.session_state.current = None
    st.rerun()

st.caption("Designed with retro computer aesthetics. Modify QUESTIONS dict in the source code to change or add queries.")

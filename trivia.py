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
        100: ("Name the SAIT CTrain station in full.", "SAIT/ACAD/Jubilee Station"),
        300: ("SAIT was originally founded under what name?", "Alberta Vocational College"),
        500: ("Name the SAIT building with the letter code G.", "Crandell Building"),
        700: ("Which SAIT alumnus became a Canadian astronaut?", "Jeremy Hansen"),
        1000: ("In what year did SAIT officially become a polytechnic institution?", "2000")
    },
    "Cyber Frontlines": {
        100: ("Which 17th-century Englishman, who attempted to blow up Parliament and failed, inspired the mask worn by the hacktivist group Anonymous?", "Guy Fawkes"),
        300: ("What infamous hacker collective in 2011 targeted Sony, PBS, and other companies \"for the lulz\"?", "LulzSec"),
        500: ("What 2017 global ransomware attack exploited a Windows SMB vulnerability, hitting hospitals, businesses, and critical infrastructure?", "WannaCry"),
        700: ("Which massive cyber espionage campaign, active since 2006, targeted governments and corporations worldwide and is attributed to a state actor?", "Shady RAT"),
        1000: ("In 2015, over 25 gigabytes of user data was leaked by a group self-named \"The Impact Team,\" exposing people seeking extramarital affairs on which two-word Canadian dating network? Both words are common girls' names.", "Ashley Madison")
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
        100: ("What is the term for mass-email scams that trick recipients into revealing credentials?", "Phishing"),
        300: ("What is the term for following an authorized person through a secure entrance without authorization?", "Tailgating"),
        500: ("What is the targeted form of phishing aimed at a specific individual or organization?", "Spear phishing"),
        700: ("Which hacker, once on the FBI’s Most Wanted list, became famous for social engineering to gain access?", "Kevin Mitnick"),
        1000: ("Which major 2011 security-industry breach began with a phishing email containing a malicious Excel attachment?", "RSA SecurID breach")
    },
    "Tech Lore & History": {
        100: ("The OG \"internet cat\" that basically started meme culture?", "Nyan Cat"),
        300: ("Year TikTok officially launched globally (and shook the world)?", "2018"),
        500: ("The first-ever \"computer virus\" that made your floppy scream?", "Brain"),
        700: ("The guy who basically invented computing before it was cool, rocking gears and punch cards?", "Charles Babbage"),
        1000: ("That legendary 2000 email worm that made everyone say \"I LOVE YOU\" but hate their inbox?", "ILOVEYOU virus")
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

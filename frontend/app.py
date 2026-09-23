import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Smart Academic Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #e6e6e6;
    }
    
    /* Main title */
    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
    }
    
    h2, h3 {
        color: #e0d5ff !important;
    }
    
    /* Metric cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(167, 139, 250, 0.3);
        border-radius: 14px;
        padding: 18px;
        backdrop-filter: blur(10px);
    }
    div[data-testid="stMetric"] label {
        color: #b8b0d4 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700;
    }
    
    /* Task cards */
    .task-card {
        background: rgba(255, 255, 255, 0.06);
        border-left: 5px solid #a78bfa;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .task-name {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }
    .task-meta {
        font-size: 0.88rem;
        color: #c4b8e0;
    }
    
    /* Priority badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge-critical { background: #ff4d6d; color: #ffffff; }
    .badge-high     { background: #ff8c42; color: #ffffff; }
    .badge-medium   { background: #ffd166; color: #1a1a1a; }
    .badge-low      { background: #06d6a0; color: #0a0a0a; }
    
    /* Input box */
    .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(167, 139, 250, 0.4) !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #7c3aed, #ec4899);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5);
    }
    
    /* Preset chips (secondary buttons) */
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(167, 139, 250, 0.3) !important;
        font-size: 0.85rem !important;
        padding: 8px 12px !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(167, 139, 250, 0.2) !important;
        transform: translateY(-2px);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.85);
        border-right: 1px solid rgba(167, 139, 250, 0.2);
    }
    
    /* Divider */
    hr { border-color: rgba(167, 139, 250, 0.2); }
</style>
""", unsafe_allow_html=True)


# ---------- HELPERS ----------
def priority_class(label: str) -> str:
    return {
        "Critical": "badge-critical",
        "High": "badge-high",
        "Medium": "badge-medium",
        "Low": "badge-low",
    }.get(label, "badge-low")


def fetch_tasks():
    try:
        r = requests.get(f"{API_URL}/tasks", timeout=90)
        return r.json() if r.status_code == 200 else []
    except Exception as e:
        st.error(f"Could not reach backend: {e}")
        return []


def add_task(text: str):
    try:
        r = requests.post(f"{API_URL}/tasks", json={"text": text}, timeout=90)
        if r.status_code == 200:
            return r.json(), None
        else:
            return None, r.json().get("detail", "Unknown error")
    except Exception as e:
        return None, str(e)


def delete_task(task_id: int):
    try:
        requests.delete(f"{API_URL}/tasks/{task_id}", timeout=90)
    except Exception:
        pass


def fetch_schedule():
    try:
        r = requests.get(f"{API_URL}/schedule", timeout=90)
        if r.status_code == 200:
            return r.json().get("schedule")
        return None
    except Exception:
        return None


# ---------- HEADER ----------
st.markdown("# 🎓 Smart Academic Assistant")
st.markdown("<p style='color:#b8b0d4;font-size:1.05rem;margin-top:-10px;'>AI-powered task prioritization & study planning</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("### 🤖 AI Study Planner")
    st.markdown("<p style='color:#b8b0d4;font-size:0.9rem;'>Generate a 3-day study schedule based on your prioritized tasks.</p>", unsafe_allow_html=True)
    
    if st.button("✨ Generate Schedule", use_container_width=True):
        with st.spinner("AI is planning your next 3 days..."):
            schedule = fetch_schedule()
            if schedule:
                st.session_state["schedule"] = schedule
            else:
                st.session_state["schedule"] = "Could not generate schedule. Add some tasks first."
    
    if "schedule" in st.session_state:
        st.markdown("---")
        st.markdown("#### 📅 Your Plan")
        st.markdown(
            f"<div style='background:rgba(255,255,255,0.05);padding:14px;border-radius:10px;color:#e6e6e6;font-size:0.9rem;white-space:pre-wrap;'>{st.session_state['schedule']}</div>",
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    st.markdown("<p style='color:#7a7090;font-size:0.78rem;'>Powered by Gemini Flash + Rule-Based Priority Engine</p>", unsafe_allow_html=True)


# ---------- INPUT ----------
st.markdown("### ✍️ Add a New Task")
st.markdown("<p style='color:#b8b0d4;font-size:0.9rem;'>Just describe your task in plain English. Our AI will extract the details.</p>", unsafe_allow_html=True)

# Quick preset chips
st.markdown("<p style='color:#b8b0d4;font-size:0.85rem;margin-bottom:8px;'>⚡ What's on your plate? Try these:</p>", unsafe_allow_html=True)

preset_cols = st.columns(4)
presets = [
    ("🔥 Urgent deadline", "Submit assignment in 2 hours, super urgent"),
    ("📖 Study session", "Study for AI exam next week, medium difficulty"),
    ("✍️ Write report", "Write DBMS report due in 3 days, tough"),
    ("🧮 Practice problems", "Practice LeetCode problems this weekend, easy"),
]

# Initialize session state for input
if "task_input" not in st.session_state:
    st.session_state["task_input"] = ""

for i, (label, text) in enumerate(presets):
    with preset_cols[i]:
        if st.button(label, key=f"preset_{i}", use_container_width=True):
            st.session_state["task_input"] = text
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_area(
        "Task description",
        value=st.session_state["task_input"],
        placeholder="What's on your plate today? Type naturally — AI handles the rest.",
        height=90,
        label_visibility="collapsed",
    )
with col2:
    st.write("")
    st.write("")
    analyze_btn = st.button("🚀 Analyze", use_container_width=True)


if analyze_btn:
    if not user_input.strip():
        st.warning("Please describe your task first.")
    else:
        with st.spinner("🧠 AI is analyzing your task..."):
            result, error = add_task(user_input.strip())
        if result:
            st.success(f"✅ Task added: **{result['task_name']}** → Priority: **{result['priority_label']}**")
            # Clear the input after successful add
            st.session_state["task_input"] = ""
            st.rerun()
        else:
            st.error(f"Error: {error}")


st.markdown("---")

# ---------- METRICS ----------
tasks = fetch_tasks()

if tasks:
    total = len(tasks)
    critical = sum(1 for t in tasks if t["priority_label"] == "Critical")
    high = sum(1 for t in tasks if t["priority_label"] == "High")
    
    # Next deadline
    now = datetime.now()
    upcoming = [t for t in tasks if datetime.fromisoformat(t["deadline"].replace("Z", "")) > now]
    next_dl = min(upcoming, key=lambda t: t["deadline"])["deadline"] if upcoming else "—"

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📋 Total Tasks", total)
    m2.metric("🔴 Critical", critical)
    m3.metric("🟠 High Priority", high)
    m4.metric("⏰ Next Deadline", next_dl.split("T")[0] if next_dl != "—" else "—")

st.markdown("### 📌 Your Prioritized Tasks")

if not tasks:
    st.info("No tasks yet. Add one above to get started! 👆")
else:
    for t in tasks:
        badge_class = priority_class(t["priority_label"])
        try:
            deadline_fmt = datetime.fromisoformat(t["deadline"]).strftime("%a, %d %b %Y · %I:%M %p")
        except Exception:
            deadline_fmt = t["deadline"]
        
        col_card, col_btn = st.columns([6, 1])
        with col_card:
            st.markdown(f"""
                <div class="task-card">
                    <div class="task-name">{t['task_name']}</div>
                    <div class="task-meta">
                        📚 {t.get('subject', 'General')} &nbsp;·&nbsp;
                        ⏰ {deadline_fmt} &nbsp;·&nbsp;
                        🎯 Difficulty: {t['difficulty']}/10 &nbsp;·&nbsp;
                        📊 Score: {t['priority_score']}
                    </div>
                    <div style="margin-top:10px;">
                        <span class="badge {badge_class}">{t['priority_label']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with col_btn:
            st.write("")
            st.write("")
            if st.button("🗑️", key=f"del_{t['id']}", help="Delete this task"):
                delete_task(t["id"])
                st.rerun()
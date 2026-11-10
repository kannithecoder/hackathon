import streamlit as st
import time
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="FocusBrake AI", page_icon="🛑", layout="centered")

# --- INITIAL STATE MANAGEMENT ---
if "app_unlocked" not in st.session_state:
    st.session_state.app_unlocked = False
if "time_saved" not in st.session_state:
    st.session_state.time_saved = 45  # Starting sample data in minutes
if "screen_state" not in st.session_state:
    st.session_state.screen_state = "intercept" # intercept, fatigue_check, dashboard

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 5px; }
    .subtitle { font-size: 1.1rem; color: #6B7280; text-align: center; margin-bottom: 30px; }
    .metric-box { background-color: #F3F4F6; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- AI COACH PERSONALITY PROMPTS ---
COACH_RESPONSES = {
    "Gentle Support": {
        "bored": "I know things feel a bit dull right now, but scrolling won't fill that gap. How about we stretch for 60 seconds instead?",
        "work": "Proud of you for staying intentional! I've set a timer for 15 minutes. Go smash it!"
    },
    "The Aggressive Roaster": {
        "bored": "Bored? Again? You have 20 days left for the hackathon and you're hunting for cheap dopamine. Close the tab right now.",
        "work": "Fine. 15 minutes only. If I catch your eyes drifting, I am locking this screen completely. Get to work."
    }
}

# ==========================================
# SCREEN 1: THE AI INTERCEPT GATEKEEPER
# ==========================================
if st.session_state.screen_state == "intercept":
    st.markdown("<div class='main-title'>🛑 FocusBrake AI Intercept</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Your brain tried to open a distracting app out of muscle memory.</div>", unsafe_allow_html=True)
    
    # Configuration Sidebar
    st.sidebar.header("⚙️ Configuration")
    coach_mode = st.sidebar.selectbox("Choose your AI Coach Persona:", ["Gentle Support", "The Aggressive Roaster"])
    
    st.info("🤖 AI Coach: 'Stop right there! Before I unlock this screen, you need to state your intent.'")
    
    # Intent Input
    user_intent = st.text_input("What is your exact, productive reason for opening this app right now?", placeholder="e.g., I need to check the team meet link")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Intent Evaluation", type="primary"):
            if user_intent.strip() == "":
                st.error("You can't leave this blank. Be honest with yourself.")
            elif "bored" in user_intent.lower() or "scroll" in user_intent.lower() or "waste" in user_intent.lower():
                st.warning(f"🚨 Response from {coach_mode}:\n\n\"{COACH_RESPONSES[coach_mode]['bored']}\"")
            else:
                st.success(f"✅ Response from {coach_mode}:\n\n\"{COACH_RESPONSES[coach_mode]['work']}\"")
                time.sleep(2)
                st.session_state.screen_state = "fatigue_check"
                st.rerun()
                
    with col2:
        if st.button("Cancel & Save My Time"):
            st.session_state.time_saved += 15
            st.balloons()
            st.success("Brilliant choice! You just saved 15 minutes of your life.")

# ==========================================
# SCREEN 2: THE BIOMETRIC FATIGUE SCANNER (SIMULATED FOR MULTIPLATFORM RUN)
# ==========================================
elif st.session_state.screen_state == "fatigue_check":
    st.markdown("<div class='main-title'>👁️ AI Fatigue & Blink Analyzer</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Evaluating your physical strain metrics via webcam to ensure safe workflow...</div>", unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for percent_complete in range(100):
        time.sleep(0.02)
        progress_bar.progress(percent_complete + 1)
        if percent_complete < 40:
            status_text.text("📷 Activating camera layer...")
        elif percent_complete < 80:
            status_text.text("🔄 Analyzing blink rate and head posture ratios...")
        else:
            status_text.text("🧠 Calculating final Cognitive Load Index...")
            
    # Mocking a normal energy state result for demonstration flow
    st.success("⚡ Metrics Normal: Fatigue Index is low. You are cleared for focused work.")
    if st.button("Enter Deep Work Dashboard"):
        st.session_state.screen_state = "dashboard"
        st.session_state.app_unlocked = True
        st.rerun()

# ==========================================
# SCREEN 3: DEEP WORK DASHBOARD
# ==========================================
elif st.session_state.screen_state == "dashboard":
    st.markdown("<div class='main-title'>⚡ FocusBrake Deep Work Matrix</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-box'>⏱️ Total Time Saved<br><span style='font-size:1.5rem; color:#2563EB;'>{st.session_state.time_saved} Mins</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-box'>🎯 Intent Accuracy<br><span style='font-size:1.5rem; color:#10B981;'>88%</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-box'>👁️ Strain Risk Level<br><span style='font-size:1.5rem; color:#F59E0B;'>Low</span></div>", unsafe_allow_html=True)
        
    st.write("---")
    st.subheader("🛠️ Active Work Mode Checklist")
    st.checkbox("Reply to team critical message", value=False)
    st.checkbox("Review code file documentation", value=False)
    
    if st.button("Lock Focus Gatekeeper Again"):
        st.session_state.screen_state = "intercept"
        st.session_state.app_unlocked = False
        st.rerun()
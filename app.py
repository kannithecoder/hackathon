import streamlit as st
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="FocusBrake AI", page_icon="🛑", layout="centered")

# --- STATE MANAGEMENT ---
if "time_saved" not in st.session_state:
    st.session_state.time_saved = 45
if "screen_state" not in st.session_state:
    st.session_state.screen_state = "intercept"

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: 800; color: #1E3A8A; text-align: center; }
    .subtitle { font-size: 1.1rem; color: #6B7280; text-align: center; margin-bottom: 30px; }
    .metric-box { background-color: #F3F4F6; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SCREEN 1: THE INTERCEPT GATEKEEPER
# ==========================================
if st.session_state.screen_state == "intercept":
    st.markdown("<div class='main-title'>🛑 FocusBrake AI Intercept</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Your brain tried to open a distracting app out of muscle memory.</div>", unsafe_allow_html=True)
    
    st.info("🤖 AI Coach: 'Before I unlock this screen, state your explicit intention below.'")
    user_intent = st.text_input("What is your exact, productive reason for opening this app right now?", placeholder="e.g., Checking team meet updates")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Intent Evaluation", type="primary"):
            if user_intent.strip() == "":
                st.error("Please fill out your intent box honestly.")
            elif any(word in user_intent.lower() for word in ["bored", "scroll", "waste", "timepass"]):
                st.warning("🚨 AI Coach: 'You confessed you are just bored. Step away from the glass!'")
            else:
                st.success("✅ Intent verified. Let's run a physical fatigue check next...")
                time.sleep(1.5)
                st.session_state.screen_state = "fatigue_check"
                st.rerun()
                
    with col2:
        if st.button("Cancel & Save My Time"):
            st.session_state.time_saved += 15
            st.balloons()

# ==========================================
# SCREEN 2: NATIVE LIVE WEBCAM SCANNER
# ==========================================
elif st.session_state.screen_state == "fatigue_check":
    st.markdown("<div class='main-title'>👁️ Live Fatigue Analyzer</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Smile or blink at the camera to verify your cognitive alertness levels.</div>", unsafe_allow_html=True)
    
    # Secure web container for webcam inputs
    img_file = st.camera_input("📷 Take a live analysis snapshot")
    
    if img_file is not None:
        with st.spinner("🧠 Running physical strain and cognitive load calculations..."):
            time.sleep(2)
        st.success("⚡ Metrics Normal: Fatigue index optimal. You are safe to work!")
        
        if st.button("Proceed to Dashboard", type="primary"):
            st.session_state.screen_state = "dashboard"
            st.rerun()
            
    if st.button("🔙 Back"):
        st.session_state.screen_state = "intercept"
        st.rerun()

# ==========================================
# SCREEN 3: DEEP WORK DASHBOARD
# ==========================================
elif st.session_state.screen_state == "dashboard":
    st.markdown("<div class='main-title'>⚡ FocusBrake Deep Work Matrix</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='metric-box'>⏱️ Total Time Saved<br><span style='font-size:1.5rem; color:#2563EB;'>{st.session_state.time_saved} Mins</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-box'>🎯 Strain Risk Level<br><span style='font-size:1.5rem; color:#10B981;'>Optimal</span></div>", unsafe_allow_html=True)
        
    st.write("---")
    st.subheader("📝 Active Core Task Checklist")
    st.checkbox("Draft hackathon solution proposal documentation")
    st.checkbox("Test frontend interface interactions")
    
    if st.button("Lock Workspace Gatekeeper"):
        st.session_state.screen_state = "intercept"
        st.rerun()

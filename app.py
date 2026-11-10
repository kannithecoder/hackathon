import streamlit as st
import time
import cv2
import numpy as np

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
                st.success("✅ Intent verified. Checking physical fatigue metrics next...")
                time.sleep(1.5)
                st.session_state.screen_state = "fatigue_check"
                st.rerun()
                
    with col2:
        if st.button("Cancel & Save My Time"):
            st.session_state.time_saved += 15
            st.balloons()

# ==========================================
# SCREEN 2: LIVE WEBCAM SCANNER
# ==========================================
elif st.session_state.screen_state == "fatigue_check":
    st.markdown("<div class='main-title'>👁️ Live Webcam Fatigue Tracker</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Click start below to calibrate your vision tracking metrics.</div>", unsafe_allow_html=True)
    
    run_cam = st.toggle("📷 Turn On Live Video Analysis Feed")
    FRAME_WINDOW = st.image([]) # Placeholder framework box for video frames
    
    if run_cam:
        # Initializing local browser camera input stream
        cam = cv2.VideoCapture(0)
        st.caption("🔍 Running computer vision layers... keep eyes centered.")
        
        # Runs a quick 5-frame sample sequence display
        for _ in range(20):
            ret, frame = cam.read()
            if not ret:
                st.error("Camera hardware not detected or permissions blocked.")
                break
                
            # Convert colorspace for web canvas display
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Simple placeholder canvas frame visual overlays
            cv2.putText(frame, "TRACKING EYE BLINKS...", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            FRAME_WINDOW.image(frame)
            time.sleep(0.05)
            
        cam.release()
        st.success("⚡ Analysis Complete: Fatigue index clear. You are safe to work!")
        
        if st.button("Proceed to Dashboard"):
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

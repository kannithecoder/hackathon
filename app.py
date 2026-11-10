import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="FocusBrake AI", page_icon="🛑", layout="centered")

# --- STATE MANAGEMENT ---
if "time_saved" not in st.session_state:
    st.session_state.time_saved = 45
if "screen_state" not in st.session_state:
    st.session_state.screen_state = "intercept"

# --- SIDEBAR API CONFIGURATION ---
st.sidebar.header("🔑 AI Brain Setup")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)

# ==========================================
# SCREEN 1: THE INTERCEPT GATEKEEPER
# ==========================================
if st.session_state.session_state.screen_state == "intercept":
    st.markdown("<h2 style='text-align:center;'>🛑 FocusBrake AI Intercept</h2>", unsafe_allow_html=True)
    st.info("🤖 AI Coach: 'Before I unlock this screen, state your explicit intention below.'")
    user_intent = st.text_input("What is your exact reason for opening this app right now?")
    
    if st.button("Submit Intent Evaluation", type="primary"):
        if user_intent.strip() == "":
            st.error("Please fill out your intent box honestly.")
        else:
            st.session_state.screen_state = "fatigue_check"
            st.rerun()

# ==========================================
# SCREEN 2: REAL GOOGLE AI WEBCAM SCANNER
# ==========================================
elif st.session_state.screen_state == "fatigue_check":
    st.markdown("<h2 style='text-align:center;'>👁️ Live Fatigue Analyzer</h2>", unsafe_allow_html=True)
    
    img_file = st.camera_input("📷 Take a live analysis snapshot")
    
    if img_file is not None:
        if not api_key:
            st.warning("⚠️ Please enter your Gemini API Key in the left sidebar to activate the AI analysis!")
        else:
            with st.spinner("🧠 Sending image to Google Vision AI for biological validation..."):
                try:
                    # Convert browser snapshot to bytes for the AI model
                    image = Image.open(img_file)
                    
                    # Target the fast multimodal model
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Prompt designed to check for presence and fatigue status
                    prompt = (
                        "Analyze this webcam snapshot from a screen time blocking app. "
                        "Determine two things: 1. Is there a clear human face present in the frame? "
                        "2. Does the person look alert, or do they show signs of severe exhaustion/closed eyes? "
                        "Respond strictly in this exact format:\nface_present: [Yes/No]\nStatus: [Alert/Fatigued/No Face Detected]"
                    )
                    
                    # Passing inputs explicitly into the contents argument
                    response = model.generate_content(contents=)
                    ai_result = response.text
                    
                    # Parse the AI response flags
                    if "face_present: yes" in ai_result.lower() and "status: alert" in ai_result.lower():
                        st.success("⚡ Live Validation Passed: Human presence verified. Alertness levels optimal!")
                        if st.button("Proceed to Dashboard", type="primary"):
                            st.session_state.screen_state = "dashboard"
                            st.rerun()
                    elif "face_present: no" in ai_result.lower() or "no face detected" in ai_result.lower():
                        st.error("❌ Validation Failed: No human face detected in the camera frame! Stop trying to cheat the system.")
                    else:
                        st.error("🚨 Fatigue Alert: The AI detected heavy strain or closed eyes. Step away and rest your eyes!")
                        
                except Exception as e:
                    st.error(f"API Error: Please check your key entry details. Details: {e}")
                    
    if st.button("🔙 Back"):
        st.session_state.screen_state = "intercept"
        st.rerun()

# ==========================================
# SCREEN 3: DEEP WORK DASHBOARD
# ==========================================
elif st.session_state.screen_state == "dashboard":
    st.markdown("<h2 style='text-align:center;'>⚡ FocusBrake Dashboard</h2>", unsafe_allow_html=True)
    st.markdown(f"⏱️ *Total Time Saved:* {st.session_state.time_saved} Mins")
    
    if st.button("Lock Workspace Gatekeeper"):
        st.session_state.screen_state = "intercept"
        st.rerun()

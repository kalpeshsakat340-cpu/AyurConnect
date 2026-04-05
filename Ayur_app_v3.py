import streamlit as st
import google.generativeai as genai
import time

# --- PAGE SETUP ---
# Yeh line sabse upar honi zaroori hai
st.set_page_config(page_title="AyurConnect Pro", page_icon="🌿", layout="centered")

# --- SPLASH SCREEN LOGIC (Jadoo yahan hai) ---
if 'first_load' not in st.session_state:
    splash = st.empty()
    with splash.container():
        st.markdown("<h1 style='text-align: center; margin-top: 30vh; font-size: 60px; color: #2e7d32;'>🌿 AyurConnect</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #555;'>Initializing AI Engine...</h3>", unsafe_allow_html=True)
    
    time.sleep(2.5) # 2.5 second ke liye splash screen dikhegi
    splash.empty() # Screen clear ho jayegi
    st.session_state.first_load = True

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f4fbf7; }
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 20px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🌿 AyurConnect: Hyper-Personalized AI")
st.write("Apni Prakriti (Body Type) ke hisaab se sateek ilaj aur diet plan.")

# --- API SETUP ---
API_KEY = "AIzaSyDsu7oMD9p5hoaKwryH2uB3gjMMAV4Ayb0" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

# --- DOSHA LOGIC ---
def calculate_dosha(skin, temp):
    if "Oily" in skin and "Thand" in temp:
        return "Kapha"
    elif "Oily" in skin and "Garmi" in temp:
        return "Pitta"
    elif "Dry" in skin and "Thand" in temp:
        return "Vata"
    else:
        return "Sama (Mixed)"

# --- SMART BOT LOGIC ---
def get_ai_response(user_input, selected_lang, dosha):
    system_instruction = f"""
    You are an expert Ayurvedic Doctor. 
    The patient's Ayurvedic body type (Prakriti) is: {dosha}.
    Make sure the remedies and diet plan DO NOT aggravate their {dosha} dosha.
    
    Structure your answer in these 3 parts:
    1. 🌿 Remedies (Gharelu Upay tailored for {dosha})
    2. 🥗 Detailed Diet Plan (Kya Khayein/Kya Na Khayein for {dosha})
    3. ⚠️ Safety Warning & Disclaimer
    
    VERY IMPORTANT: You MUST write the entire response strictly in {selected_lang} language.
    """
    response = model.generate_content(f"{system_instruction}\n\nPatient Query: {user_input}")
    return response.text

# --- APP INTERFACE ---
with st.container():
    lang_choice = st.selectbox("🌐 Bhasha chunein (Language):", ["Marathi", "Hindi", "English"])
    
    st.markdown("---")
    st.subheader("🩺 Step 1: Apni Prakriti Jaanein")
    
    col1, col2 = st.columns(2)
    with col1:
        skin_type = st.selectbox("Aapki Skin Kaisi Hai?", ["Normal", "Oily (Teliya)", "Dry (Rookhi)"])
    with col2:
        body_temp = st.selectbox("Aapko Zyada Kya Lagta Hai?", ["Normal", "Thand (Cold)", "Garmi (Hot)"])
    
    user_dosha = calculate_dosha(skin_type, body_temp)
    st.success(f"🧘 Aapki Ayurvedic Prakriti hai: **{user_dosha}**")
    
    st.markdown("---")
    st.subheader("🩺 Step 2: Apni Takleef Batayein")
    user_query = st.text_input("", placeholder="Example: Hair fall, Diabetes, Acidity...")
    
    if st.button("Sujhav Lein (Get Personalized Advice)"):
        if user_query:
            with st.spinner(f'Ayur-Assistant {user_dosha} prakriti ke hisaab se plan bana raha hai...'):
                try:
                    result = get_ai_response(user_query, lang_choice, user_dosha)
                    st.markdown("---")
                    st.markdown(result)
                    
                    st.download_button(
                        label="📥 Download Personalized Diet Plan",
                        data=result,
                        file_name=f"AyurConnect_{user_dosha}_Plan.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error aayi hai: {e}")
        else:
            st.warning("Kripya pehle kuch sawaal likhein.")
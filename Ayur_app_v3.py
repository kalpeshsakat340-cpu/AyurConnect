import streamlit as st
import google.generativeai as genai
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="AyurConnect Pro", page_icon="🌿", layout="centered")

# --- UI TRANSLATIONS ---
translations = {
    "Marathi": {
        "title": "🌿 AyurConnect: हायपर-पर्सनलाइज्ड AI",
        "subtitle": "तुमच्या प्रकृतीनुसार (Body Type) अचूक उपचार आणि आहार योजना.",
        "step1": "🩺 पायरी १: तुमची प्रकृती जाणून घ्या",
        "skin_label": "तुमची त्वचा कशी आहे?",
        "temp_label": "तुम्हाला जास्त काय जाणवते?",
        "prakriti_res": "🧘 तुमची आयुर्वेदिक प्रकृती आहे:",
        "step2": "🩺 पायरी २: तुमची समस्या सांगा",
        "btn_text": "सल्ला घ्या (Get Advice)",
        "input_placeholder": "उदा: केस गळणे, ॲसिडिटी...",
        "wait_msg": "तुमच्या प्रकृतीनुसार योजना तयार होत आहे...",
        "download_btn": "📥 आहार योजना डाउनलोड करा"
    },
    "Hindi": {
        "title": "🌿 AyurConnect: हाइपर-पर्सनलाइज्ड AI",
        "subtitle": "अपनी प्रकृति (Body Type) के हिसाब से सटीक इलाज और डाइट प्लान।",
        "step1": "🩺 स्टेप 1: अपनी प्रकृति जानें",
        "skin_label": "आपकी स्किन कैसी है?",
        "temp_label": "आपको ज़्यादा क्या लगता है?",
        "prakriti_res": "🧘 आपकी आयुर्वेदिक प्रकृति है:",
        "step2": "🩺 स्टेप 2: अपनी तकलीफ बताएं",
        "btn_text": "सुझाव लें (Get Advice)",
        "input_placeholder": "उदाहरण: बालों का झड़ना, एसिडिटी...",
        "wait_msg": "आपकी प्रकृति के हिसाब से प्लान बन रहा है...",
        "download_btn": "📥 डाइट प्लान डाउनलोड करें"
    },
    "English": {
        "title": "🌿 AyurConnect: Hyper-Personalized AI",
        "subtitle": "Accurate treatment and diet plan according to your Prakriti.",
        "step1": "🩺 Step 1: Know Your Prakriti",
        "skin_label": "How is your skin?",
        "temp_label": "What do you feel more?",
        "prakriti_res": "🧘 Your Ayurvedic Prakriti is:",
        "step2": "🩺 Step 2: Tell Your Problem",
        "btn_text": "Get Personalized Advice",
        "input_placeholder": "Example: Hair fall, Acidity...",
        "wait_msg": "Creating plan based on your Prakriti...",
        "download_btn": "📥 Download Diet Plan"
    }
}

# --- SPLASH SCREEN ---
if 'first_load' not in st.session_state:
    splash = st.empty()
    with splash.container():
        st.markdown("<h1 style='text-align: center; margin-top: 30vh; font-size: 60px; color: #2e7d32;'>🌿 AyurConnect</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Initializing AI Engine...</h3>", unsafe_allow_html=True)
    time.sleep(2.2)
    splash.empty()
    st.session_state.first_load = True

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f4fbf7; }
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 20px; width: 100%; font-weight: bold; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- API SETUP ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
   model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("API Key not found in Secrets! Please add it in Streamlit settings.")

# --- APP INTERFACE (FIXED LAYOUT) ---
# Yahan humne ek 'Container' banaya taaki Title hamesha sabse upar rahe
header_container = st.container()

# Uske niche humne Language ka option diya
lang_choice = st.selectbox("🌐 Bhasha chunein (Language):", ["Marathi", "Hindi", "English"])
t = translations[lang_choice]

# Ab wapas us upar wale Container mein ja kar Title print kar diya!
with header_container:
    st.title(t["title"])
    st.write(t["subtitle"])
    st.markdown("---")

st.subheader(t["step1"])
col1, col2 = st.columns(2)
with col1:
    skin_type = st.selectbox(t["skin_label"], ["Normal", "Oily", "Dry"])
with col2:
    body_temp = st.selectbox(t["temp_label"], ["Normal", "Cold", "Hot"])

# Dosha Logic
dosha = "Sama"
if "Oily" in skin_type and "Cold" in body_temp: dosha = "Kapha"
elif "Oily" in skin_type and "Hot" in body_temp: dosha = "Pitta"
elif "Dry" in skin_type and "Cold" in body_temp: dosha = "Vata"

st.success(f"{t['prakriti_res']} **{dosha}**")

st.markdown("---")
st.subheader(t["step2"])
user_query = st.text_input("", placeholder=t["input_placeholder"])

if st.button(t["btn_text"]):
    if user_query:
        with st.spinner(t["wait_msg"]):
            try:
                response = model.generate_content(f"Act as Ayurvedic Doctor. Patient is {dosha}. Problem: {user_query}. Respond strictly in {lang_choice} language with Remedies, Diet, and Disclaimer.")
                st.markdown("---")
                st.markdown(response.text)
                st.download_button(label=t["download_btn"], data=response.text, file_name="AyurPlan.txt")
            except Exception as e:
                st.error(f"Error: {e}")
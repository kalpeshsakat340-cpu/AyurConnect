import streamlit as st
import google.generativeai as genai
import time

# --- UI TRANSLATIONS ---
translations = {
    "Marathi": {
        "title": "🌿 AyurConnect: हायपर-पर्सनलाइज्ड AI",
        "subtitle": "तुमच्या प्रकृतीनुसार अचूक उपचार, आहार योजना आणि AI डॉक्टर.",
        "step1": "🩺 पायरी १: तुमची प्रकृती जाणून घ्या",
        "skin_label": "तुमची त्वचा कशी आहे?",
        "temp_label": "तुम्हाला जास्त काय जाणवते?",
        "prakriti_res": "🧘 तुमची आयुर्वेदिक प्रकृती आहे:",
        "tab1_name": "📋 त्वरित योजना (Quick Plan)",
        "tab2_name": "💬 AI डॉक्टरशी चॅट (Chat)",
        "step2_tab1": "तुमची समस्या सांगा (उदा: ॲसिडिटी, केस गळणे)",
        "btn_text": "सल्ला आणि आहार योजना मिळवा",
        "wait_msg": "योजना तयार होत आहे...",
        "download_btn": "📥 आहार योजना डाउनलोड करा",
        "step2_tab2": "AI डॉक्टरला प्रश्न विचारा...",
        "clear_btn": "🗑️ चॅट पुसून टाका",
        "chat_tip": "💡 **टीप:** AI सोबत फक्त 'Hi' करण्याऐवजी तुमचा संपूर्ण प्रश्न एकाच वेळी विचारा. (उदा: 'मला २ दिवसांपासून ॲसिडिटी आहे, मी काय करावे?')."
    },
    "Hindi": {
        "title": "🌿 AyurConnect: हाइपर-पर्सनलाइज्ड AI",
        "subtitle": "अपनी प्रकृति के हिसाब से सटीक इलाज, डाइट प्लान और AI डॉक्टर।",
        "step1": "🩺 स्टेप 1: अपनी प्रकृति जानें",
        "skin_label": "आपकी स्किन कैसी है?",
        "temp_label": "आपको ज़्यादा क्या लगता है?",
        "prakriti_res": "🧘 आपकी आयुर्वेदिक प्रकृति है:",
        "tab1_name": "📋 डाइट प्लान (Quick Plan)",
        "tab2_name": "💬 AI डॉक्टर से चैट (Chat)",
        "step2_tab1": "अपनी तकलीफ बताएं (उदा: एसिडिटी, बालों का झड़ना)",
        "btn_text": "सुझाव और डाइट प्लान लें",
        "wait_msg": "प्लान बन रहा है...",
        "download_btn": "📥 डाइट प्लान डाउनलोड करें",
        "step2_tab2": "AIাবলী डॉक्टर से सवाल पूछें...",
        "clear_btn": "🗑️ चैट क्लियर करें",
        "chat_tip": "💡 **सुझाव:** AI को 'Hi' भेजने के बजाय, अपनी पूरी तकलीफ एक ही मैसेज में लिखें। (उदा: 'मुझे 2 दिन से एसिडिटी है, क्या उपाय है?')."
    },
    "English": {
        "title": "🌿 AyurConnect: Hyper-Personalized AI",
        "subtitle": "Accurate treatment, diet plan, and AI Doctor based on your Prakriti.",
        "step1": "🩺 Step 1: Know Your Prakriti",
        "skin_label": "How is your skin?",
        "temp_label": "What do you feel more?",
        "prakriti_res": "🧘 Your Ayurvedic Prakriti is:",
        "tab1_name": "📋 Quick Diet Plan",
        "tab2_name": "💬 Chat with AI Doctor",
        "step2_tab1": "Tell your problem (e.g., Acidity, Hair fall)",
        "btn_text": "Get Advice & Diet Plan",
        "wait_msg": "Creating plan...",
        "download_btn": "📥 Download Diet Plan",
        "step2_tab2": "Ask the AI Doctor...",
        "clear_btn": "🗑️ Clear Chat",
        "chat_tip": "💡 **Pro Tip:** Instead of sending 'Hi', type your complete problem in a single message. (e.g., 'I have acidity for 2 days, what should I do?')."
    }
}

# --- API SETUP (AUTO LOAD BALANCER - NO SIDEBAR) ---
try:
    api_keys = st.secrets["GEMINI_API_KEYS"]
    
    if "key_index" not in st.session_state:
        st.session_state.key_index = 0

    current_key = api_keys[st.session_state.key_index]
    genai.configure(api_key=current_key)
    
    # Fast model 
    model = genai.GenerativeModel('gemini-2.5-flash')

except Exception as e:
    st.error(f"⚠️ API Error: Lagta hai secrets.toml theek se set nahi hai. Error: {e}")


# --- APP INTERFACE ---
header_container = st.container()
lang_choice = st.selectbox("🌐 Bhasha chunein (Language):", ["Marathi", "Hindi", "English"])
t = translations[lang_choice]

with header_container:
    st.title(t["title"])
    st.write(t["subtitle"])
    st.markdown("---")

# --- DOSHA CALCULATION ---
st.subheader(t["step1"])
col1, col2 = st.columns(2)
with col1:
    skin = st.selectbox(t["skin_label"], ["Dry (Oily/Dry mixed)", "Oily", "Normal/Sensitive"])
with col2:
    temp = st.selectbox(t["temp_label"], ["Cold", "Hot", "Mixed"])

# Prakriti Logic
prakriti = "Vata (वात)"
if skin == "Oily" or temp == "Hot":
    prakriti = "Pitta (पित्त)"
elif skin == "Normal/Sensitive" and temp == "Cold":
    prakriti = "Kapha (कफ)"

st.success(f"{t['prakriti_res']} **{prakriti}**")
st.markdown("---")

# --- TABS ---
tab1, tab2 = st.tabs([t["tab1_name"], t["tab2_name"]])

# --- TAB 1: QUICK PLAN ---
with tab1:
    problem = st.text_input(t["step2_tab1"])
    if st.button(t["btn_text"]):
        if problem:
            with st.spinner(t["wait_msg"]):
                prompt = f"Act as an expert Ayurvedic doctor. The patient has {prakriti} dosha and is suffering from {problem}. Give a short home remedy and a diet plan. Respond ONLY in {lang_choice} language."
                try:
                    response = model.generate_content(prompt)
                    st.write(response.text)
                    st.download_button(
                        label=t["download_btn"],
                        data=response.text,
                        file_name=f"AyurConnect_Plan_{problem}.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    error_msg = str(e).lower()
                    if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:
                        # AUTO SWITCH JADU YAHAN HAI
                        st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                        st.warning("🔄 Server par load zyada tha. Backup server connect ho gaya hai! Kripya dobara button dabayein.")
                    else:
                        st.error(f"Error aagaya: {e}")
        else:
            st.warning("Please ek problem daaliye!")

# --- TAB 2: CHATBOT ---
with tab2:
    st.info(t["chat_tip"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        if 'chat_session' not in st.session_state:
            try:
                st.session_state.chat_session = model.start_chat(history=[])
            except:
                pass

    if st.button(t["clear_btn"]):
        st.session_state.messages = []
        try:
            st.session_state.chat_session = model.start_chat(history=[])
        except:
            pass
        st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input(t["step2_tab2"]):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                system_prompt = f"Act as an Ayurvedic doctor. The user has {prakriti} dosha. Speak ONLY in {lang_choice}. The user says: {user_input}"
                response = st.session_state.chat_session.send_message(system_prompt, stream=True)
                for chunk in response:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.05)
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                error_msg = str(e).lower()
                if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:
                    # AUTO SWITCH JADU YAHAN HAI
                    st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                    st.warning("🔄 AI Doctor ka server busy hai. Auto-shifting... Kripya apna message dobara bhejein.")
                else:
                    st.error(f"Error aagaya: {e}")
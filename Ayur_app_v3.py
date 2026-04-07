import streamlit as st
import google.generativeai as genai
import time

# --- UI TRANSLATIONS ---
translations = {
    "Marathi": {
        "title": "🌿 AyurConnect (Beta)",
        "subtitle": "तुमच्या प्रकृतीनुसार अचूक उपचार आणि आहार योजना.",
        "step1": "🩺 तुमची प्रकृती जाणून घ्या",
        "skin_label": "तुमची त्वचा कशी आहे?",
        "temp_label": "तुम्हाला जास्त काय जाणवते?",
        "prakriti_res": "🧘 तुमची आयुर्वेदिक प्रकृती आहे: ",
        "menu_home": "🏠 त्वरित योजना (Home)",
        "menu_chat": "💬 AI डॉक्टरशी चॅट",
        "step2_tab1": "किंवा तुमची समस्या टाईप करा:",
        "btn_text": "सल्ला आणि आहार योजना मिळवा",
        "wait_msg": "योजना तयार होत आहे...",
        "download_btn": "📥 आहार योजना डाउनलोड करा",
        "step2_tab2": "AI डॉक्टरला प्रश्न विचारा...",
        "clear_btn": "🗑️ चॅट पुसून टाका",
        "chat_tip": "💡 **टीप:** AI सोबत फक्त 'Hi' करण्याऐवजी तुमचा संपूर्ण प्रश्न एकाच वेळी विचारा. (उदा: 'मला २ दिवसांपासून ऍसिडिटी आहे, मी काय करावे?').",
        "disclaimer": "हा AI फक्त माहिती आणि प्राथमिक सल्ल्यासाठी आहे. कोणत्याही गंभीर आजारांसाठी कृपया प्रत्यक्ष डॉक्टरांचा सल्ला घ्या.",
        "aaji_batwa": "👵 आजीचा बटवा (येथे क्लिक करा)",
        "quick_cap": "सामान्य समस्या? त्वरित उपायासाठी खालील बटण दाबा:",
        "custom_prob_title": "### ✍️ तुमची समस्या सांगा",
        "custom_prob_cap": "इतर कोणतीही आरोग्य समस्या? खाली टाईप करा:",
        "prob_placeholder": "उदा. सांधेदुखी, केस गळणे..."
    },
    "Hindi": {
        "title": "🌿 AyurConnect (Beta)",
        "subtitle": "अपनी प्रकृति के हिसाब से सटीक इलाज और डाइट प्लान।",
        "step1": "🩺 अपनी प्रकृति जानें",
        "skin_label": "आपकी स्किन कैसी है?",
        "temp_label": "आपको ज़्यादा क्या लगता है?",
        "prakriti_res": "🧘 आपकी आयुर्वेदिक प्रकृति है: ",
        "menu_home": "🏠 क्विक प्लान (Home)",
        "menu_chat": "💬 AI डॉक्टर से चैट",
        "step2_tab1": "या अपनी तकलीफ टाइप करें:",
        "btn_text": "सुझाव और डाइट प्लान लें",
        "wait_msg": "प्लान बन रहा है...",
        "download_btn": "📥 डाइट प्लान डाउनलोड करें",
        "step2_tab2": "AI डॉक्टर से सवाल पूछें...",
        "clear_btn": "🗑️ चैट क्लियर करें",
        "chat_tip": "💡 **सुझाव:** AI को 'Hi' भेजने के बजाय, अपनी पूरी तकलीफ एक ही मैसेज में लिखें। (उदा: 'मुझे 2 दिन से एसिडिटी है, मैं क्या करूँ?').",
        "disclaimer": "यह AI केवल जानकारी और प्राथमिक सलाह के लिए है। किसी भी गंभीर बीमारी के लिए कृपया असली डॉक्टर से सलाह लें।",
        "aaji_batwa": "👵 दादी माँ के नुस्खे (यहाँ क्लिक करें)",
        "quick_cap": "आम समस्या? तुरंत उपाय के लिए बटन दबाएं:",
        "custom_prob_title": "### ✍️ अपनी तकलीफ बताएं",
        "custom_prob_cap": "कोई और स्वास्थ्य समस्या? नीचे टाइप करें:",
        "prob_placeholder": "उदा. घुटनों का दर्द, बाल झड़ना..."
    },
    "English": {
        "title": "🌿 AyurConnect (Beta)",
        "subtitle": "Accurate treatment and diet plan based on your Prakriti.",
        "step1": "🩺 Know Your Prakriti",
        "skin_label": "How is your skin?",
        "temp_label": "What do you feel more?",
        "prakriti_res": "🧘 Your Ayurvedic Prakriti is: ",
        "menu_home": "🏠 Quick Plan (Home)",
        "menu_chat": "💬 Chat with AI Doctor",
        "step2_tab1": "Or type your problem here:",
        "btn_text": "Get Advice & Diet Plan",
        "wait_msg": "Creating plan...",
        "download_btn": "📥 Download Diet Plan",
        "step2_tab2": "Ask the AI Doctor...",
        "clear_btn": "🗑️ Clear Chat",
        "chat_tip": "💡 **Pro Tip:** Instead of sending 'Hi', type your complete problem at once. (e.g., 'I have had acidity for 2 days, what should I do?').",
        "disclaimer": "This AI is for informational purposes and primary advice only. For any serious illness, please consult a real doctor.",
        "aaji_batwa": "👵 Grandma's Remedies (Click Here)",
        "quick_cap": "Common problems? Click a button:",
        "custom_prob_title": "### ✍️ Describe Your Problem",
        "custom_prob_cap": "Other health problem? Type below:",
        "prob_placeholder": "e.g., Joint pain, Hair fall..."
    }
}

# --- API SETUP ---
try:
    api_keys = st.secrets["GEMINI_API_KEYS"]
    if "key_index" not in st.session_state:
        st.session_state.key_index = 0
        
    current_key = api_keys[st.session_state.key_index]
    genai.configure(api_key=current_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"⚠️ API Error: Lagta hai secrets.toml theek se set nahi hai. Error: {e}")

# --- SIDEBAR (MOBILE MENU) ---
with st.sidebar:
    st.title("⚙️ Settings")
    lang_choice = st.selectbox("🌐 Bhasha (Language):", ["Marathi", "Hindi", "English"])
    t = translations[lang_choice]
    
    st.markdown("---")
    app_mode = st.radio("📱 Menu:", [t["menu_home"], t["menu_chat"]])
    st.markdown("---")
    st.caption("AyurConnect v1.8 | Full Translation Fixed")

# Global Prakriti Logic
prakriti = "Vata (वात)" # Default

# ==========================================
# PAGE 1: HOME (QUICK PLAN)
# ==========================================
if app_mode == t["menu_home"]:
    
    st.title(t["title"])
    st.write(t["subtitle"])
    st.markdown("---")
    
    st.subheader(t["step1"])
    col1, col2 = st.columns(2)
    with col1:
        skin = st.selectbox(t["skin_label"], ["Dry", "Oily", "Mixed (Dry & Oily)", "Normal/Sensitive"])
    with col2:
        temp = st.selectbox(t["temp_label"], ["Cold", "Hot", "Mixed"])

    if skin == "Oily" or temp == "Hot":
        prakriti = "Pitta (पित्त)"
    elif skin == "Normal/Sensitive" and temp == "Cold":
        prakriti = "Kapha (कफ)"
    elif skin == "Mixed (Dry & Oily)":
        prakriti = "Vata-Pitta (वात-पित्त)"

    st.success(f"{t['prakriti_res']} **{prakriti}**")
    st.markdown("---")

    left_col, right_col = st.columns(2)
    quick_problem = None
    submit_btn = False
    problem_input = ""
    
    with left_col:
        # UI Elements completely linked to dictionary translations
        with st.expander(t["aaji_batwa"]):
            st.caption(t["quick_cap"])
            q_col1, q_col2 = st.columns(2)
            with q_col1:
                if st.button("🔥 Acidity / पित्त", use_container_width=True): quick_problem = "Hyper Acidity and Pitta"
                if st.button("📉 वजन कमी (Weight Loss)", use_container_width=True): quick_problem = "Weight Loss and reducing belly fat safely"
                if st.button("🤧 सर्दी-खोकला (Cold & Cough)", use_container_width=True): quick_problem = "Cold, Cough and Sore Throat"
            with q_col2:
                if st.button("🤯 डोकेदुखी (Headache)", use_container_width=True): quick_problem = "Headache and Stress"
                if st.button("📈 वजन वाढ (Weight Gain)", use_container_width=True): quick_problem = "Healthy Weight Gain and Weakness"
                if st.button("🤒 ताप (Fever)", use_container_width=True): quick_problem = "Mild Fever and Body ache"

    with right_col:
        with st.container(border=True):
            # UI Elements completely linked to dictionary translations
            st.markdown(t["custom_prob_title"])
            st.caption(t["custom_prob_cap"])
            problem_input = st.text_input(t["step2_tab1"], label_visibility="collapsed", placeholder=t["prob_placeholder"])
            st.markdown("<br>", unsafe_allow_html=True) 
            submit_btn = st.button(t["btn_text"], type="primary", use_container_width=True)

    final_problem = quick_problem if quick_problem else (problem_input if submit_btn else None)
    
    if final_problem:
        st.markdown("---")
        with st.spinner(t["wait_msg"]):
            prompt = f"Act as an expert Ayurvedic doctor. The patient has {prakriti} dosha. Their problem is: {final_problem}. Give a short, safe home remedy (Gharguti Upay) and diet plan. No modern medicines. Answer in {lang_choice} language. Structure the answer with clear short bullet points."
            try:
                response = model.generate_content(prompt)
                st.write(response.text)
                st.download_button(
                    label=t["download_btn"],
                    data=response.text,
                    file_name=f"AyurConnect_Plan.txt",
                    mime="text/plain"
                )
            except Exception as e:
                error_msg = str(e).lower()
                if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:
                    st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                    st.warning("🔄 Server par load zyada tha. Backup key active ho gayi hai. Kripya wapas click karein!")
                else:
                    st.error(f"Error aagaya: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.warning(f"**Disclaimer:** {t['disclaimer']}", icon="⚠️")

# ==========================================
# PAGE 2: AI DOCTOR CHAT
# ==========================================
elif app_mode == t["menu_chat"]:
    st.title(t["menu_chat"])
    st.write(t["subtitle"])
    st.info(t["chat_tip"])
    st.warning(f"**Disclaimer:** {t['disclaimer']}", icon="⚠️")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if 'chat_session' not in st.session_state:
        try:
            st.session_state.chat_session = model.start_chat(history=[])
        except: pass
            
    if st.button(t["clear_btn"]):
        st.session_state.messages = []
        try: st.session_state.chat_session = model.start_chat(history=[])
        except: pass
        st.rerun()

    st.markdown("---")

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
                system_prompt = f"""
                Act as an empathetic and smart Ayurvedic doctor. The patient might have {prakriti} dosha.
                User message: "{user_input}"
                
                RULES:
                1. If the user's message is very short or lacks details (e.g., just says "I have a fever" or "headache"), DO NOT give a full remedy list yet. Instead, ask 1 or 2 relevant follow-up questions to understand the condition better (e.g., "Since when?", "Is there any other symptom?"). Keep it conversational.
                2. If the user provides enough details, then provide safe home remedies in short bullet points.
                3. Always reply in {lang_choice} language.
                """
                
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
                    st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                    st.warning("🔄 AI Doctor ka server busy hai. Auto-shifting to backup server. Kripya apna message dobara bhejein.")
                else:
                    st.error(f"Error aagaya: {e}")
import streamlit as st
import time
from dataeng_os.ui.i18n_helper import t, I18n

# Configure Page
st.set_page_config(
    page_title=t("app_title"),
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar with Language Toggle
with st.sidebar:
    st.title("Settings")
    lang_choice = st.radio("Language", ["PT-BR", "EN-US"], index=0)
    if lang_choice == "PT-BR":
        I18n().set_lang("pt_br")
    else:
        I18n().set_lang("en_us")

# --- HEADER (COCKPIT) ---
st.title(f"✈️ {t('home_welcome')}")
st.markdown(f"*{t('home_subtitle')}*")

# Metrics / Recent Activity Placeholders
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Contracts", value="12", delta="+2")
with col2:
    st.metric(label="Quality Score", value="98%", delta="1%")
with col3:
    st.metric(label="Pending Review", value="3", delta="-1")

st.divider()

# --- QUICK ACTIONS ---
c1, c2, c3 = st.columns(3)
if c1.button(f"✨ {t('dashboard_card_new_contract')}", use_container_width=True):
    st.switch_page("pages/1_Editor.py")

if c2.button(f"🔍 {t('dashboard_card_audit')}", use_container_width=True):
    st.toast("Audit running... (Mock)")

if c3.button(f"📚 {t('dashboard_card_search')}", use_container_width=True):
    st.switch_page("pages/1_Editor.py") # Directs to Catalog tab theoretically

st.divider()

# --- ARCHITECT CHAT (THE HYBRID INTERFACE) ---
st.subheader("🤖 The Architect")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

from dataeng_os.ui.architect import architect

# React to user input
if prompt := st.chat_input(t("chat_placeholder")):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # ANALYZE INTENT
    intent = architect.analyze_intent(prompt)
    
    if intent["action"] == "create_contract":
        st.session_state["wizard_intent"] = intent["topic"]
        st.toast(f"Starting generic contract wizard for: {intent['topic']}")
        time.sleep(1)
        st.switch_page("pages/1_Editor.py")
    else:
        # Normal Chat
        response = architect.chat(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

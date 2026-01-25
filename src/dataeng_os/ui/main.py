import streamlit as st
import time
from dataeng_os.ui.i18n_helper import t

# Configure Page
st.set_page_config(
    page_title=t("app_title"),
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# Inject Custom CSS
with open("dataeng_os/ui/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render Custom Sidebar
from dataeng_os.ui.components.sidebar import render_sidebar # noqa: E402
render_sidebar()

# --- HEADER (COCKPIT) ---
st.markdown(
    f"""
    <div>
        <h1 style="margin-bottom: 0;">✈️ {t('home_welcome')}</h1>
        <p style="color: var(--text-muted); margin-top: 0; font-size: 1.1rem;">
            {t('home_subtitle')}
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Metrics / Recent Activity Placeholders
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Contracts", value="12", delta="+2")
with col2:
    st.metric(label="Quality Score", value="98%", delta="1%")
with col3:
    st.metric(label="Pending Review", value="3", delta="-1")

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# --- QUICK ACTIONS ---
st.markdown("### ⚡ Quick Actions")
c1, c2, c3 = st.columns(3)

# Helper for styled buttons
def action_card(col, icon, label, key):
    if col.button(f"{icon} {label}", use_container_width=True, key=key):
        return True
    return False

if action_card(c1, "✨", t('dashboard_card_new_contract'), "btn_new_contract"):
    st.switch_page("pages/1_Editor.py")

if action_card(c2, "🔍", t('dashboard_card_audit'), "btn_audit"):
    st.switch_page("pages/3_Audit.py")

if action_card(c3, "📚", t('dashboard_card_search'), "btn_search"):
    st.switch_page("pages/1_Editor.py")

st.divider()

# --- ARCHITECT CHAT (THE HYBRID INTERFACE) ---
st.markdown(
    """
    <div class="architect-terminal">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="color: var(--accent); font-weight: bold;">🤖 DataEngOS Architect</span>
            <span style="font-size: 0.8rem; color: #666;">v2.1 (Online)</span>
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    role_color = "--primary" if message["role"] == "user" else "--accent"
    alignment = "flex-end" if message["role"] == "user" else "flex-start"
    bg_color = "var(--bg-surface)" if message["role"] == "user" else "transparent"
    
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

from dataeng_os.ui.architect import architect # noqa: E402

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
        st.switch_page("dataeng_os/ui/pages/1_Editor.py")
    else:
        # Normal Chat
        response = architect.chat(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

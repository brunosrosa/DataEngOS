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

from pathlib import Path

# Inject Custom CSS
css_file = Path(__file__).parent / "styles.css"
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from dataeng_os.ui.components.ux_kit import render_glass_card, toast_agent, render_health_pill, render_quality_gauge
from dataeng_os.ui.components.activity_stream import render_activity_stream

# Render Custom Sidebar
from dataeng_os.ui.components.sidebar import render_sidebar # noqa: E402
render_sidebar()

# --- HEADER (TITLE ONLY) ---
st.markdown(
    f"""
    <h1 style="margin-bottom: 0.5rem;">✈️ {t('home_welcome')}</h1>
    """, 
    unsafe_allow_html=True
)

# --- QUICK ACTIONS (MOVED UP) ---
st.markdown('<div class="card-header" style="margin-bottom: 0.5rem;">⚡ QUICK ACTIONS</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

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

# --- SUBTITLE (MOVED DOWN) ---
st.markdown(
    f"""
    <p style="color: var(--text-muted); margin-top: 0.75rem; margin-bottom: 1rem; font-size: 1rem;">
        {t('home_subtitle')}
    </p>
    """, 
    unsafe_allow_html=True
)

# --- METRICS CARDS ---
st.markdown('<div class="animate-fade-in">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1.6]) 

import textwrap

with col1:
    st.markdown(render_glass_card(
        content=textwrap.dedent(f"""
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%;">
            <h1 style="color: var(--primary); font-size: 3rem; margin: 0; line-height: 1;">12</h1>
            <div style="color: #10B981; font-weight: 500; font-size: 0.9rem; margin-top: 5px;">+2 this week</div>
        </div>
        """),
        header=t("dashboard_header_contracts"),
        height="200px"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(render_glass_card(
        content=render_quality_gauge(98), 
        header=t("dashboard_header_quality"),
        height="200px"
    ), unsafe_allow_html=True)

with col3:
    from dataeng_os.ui.components.activity_stream import render_activity_stream
    st.markdown(render_glass_card(
        content=render_activity_stream(), 
        header=t("dashboard_header_stream"),
        height="200px"
    ), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- ARCHITECT CHAT (THE HYBRID INTERFACE) ---
st.markdown(
    f"""
    <div class="architect-terminal" style="margin-top: 1rem; padding: 0.75rem 0; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 10px; opacity: 0.9;">
            <span style="color: var(--accent); font-weight: bold; font-family: 'Fira Code', monospace;">🤖 DataEngOS Architect</span>
            <span style="font-size: 0.7rem; color: var(--text-muted); border: 1px solid var(--glass-border); padding: 2px 6px; border-radius: 4px;">v2.1 Online</span>
        </div>
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10B981; padding: 4px 12px; border-radius: 20px; display: flex; align-items: center;">
             <span style="height: 8px; width: 8px; background-color: #10B981; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 5px #10B981; animation: pulse-glow 2s infinite;"></span>
             <span style="color: #10B981; font-size: 0.9rem; font-weight: 500;">{t('system_online')}</span>
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

from dataeng_os.ui.architect import architect # noqa: E402

# React to user input
if prompt := st.chat_input(t("chat_placeholder")):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    intent = architect.analyze_intent(prompt)
    
    if intent["action"] == "create_contract":
        st.session_state["wizard_intent"] = intent["topic"]
        st.toast(f"Starting generic contract wizard for: {intent['topic']}")
        time.sleep(1)
        st.switch_page("pages/1_Editor.py")
    else:
        response = architect.chat(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

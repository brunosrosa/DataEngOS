import streamlit as st
from dataeng_os.ui.i18n_helper import t
from dataeng_os.config import config

st.set_page_config(page_title="DataEngOS - Settings", page_icon="⚙️", layout="wide")

st.title("⚙️ Settings")

st.header("🤖 AI Assistant Configuration")

current_key = config.get_api_key()
current_provider = config.get_provider()

with st.form("settings_form"):
    st.info("Configure the LLM provider for the Architect.")
    
    provider = st.selectbox(
        "LLM Provider / Model",
        [
            "gemini/gemini-3-flash-preview", 
            "gemini/gemini-3-pro-preview", 
            "gemini/gemini-flash-latest",
            "openai/gpt-4o"
        ],
        index=0 if "gemini" in current_provider else 3,
        help="Gemini 3 Flash is recommended for speed. Gemini 3 Pro for complex logic."
    )
    
    api_key = st.text_input(
        "API Key", 
        value=current_key if current_key else "", 
        type="password",
        help="Enter your Gemini or OpenAI API Key."
    )
    
    if st.form_submit_button("Save Configuration", type="primary"):
        config.save_config(api_key, provider)
        st.success("Settings saved successfully! You can now use the Architect.")
        
st.divider()

st.subheader("Debug Info")
st.text(f"Current Provider: {provider}")
st.text(f"API Key Set: {'Yes' if api_key else 'No'}")

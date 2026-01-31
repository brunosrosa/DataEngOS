import streamlit as st
from dataeng_os.ui.i18n_helper import t, I18n

def render_sidebar():
    """
    Renders the custom sidebar with unified navigation and settings.
    """
    with st.sidebar:
        # 1. Branding & Context
        st.markdown("## ✈️ DataEngOS")
        
        # Dynamic Project Info - Project Selector
        current_project = st.session_state.get("project_name", "PRJ_01_Sinergia")
        projects = ["PRJ_01_Sinergia", "PRJ_02_Finance", "➕ Create New..."]
        
        selected_project = st.selectbox(
            f"📂 {t('sidebar_project')}",
            projects,
            index=0,
            key="project_selector",
            label_visibility="collapsed"
        )
        
        if selected_project == "➕ Create New...":
            st.info("Project creation wizard starting...")
            # Logic to handle creation would go here
        else:
            st.session_state["project_name"] = selected_project

        # Model Badge
        llm_model = st.session_state.get("llm_model", "Gemini 1.5 Pro")
        st.markdown(
            f"""
            <div style="margin-top: 10px; margin-bottom: 20px; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 8px; border: 1px solid var(--glass-border); display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 0.8rem; color: var(--text-muted);">{t('sidebar_model')}</span>
                <span style="font-size: 0.8rem; color: var(--accent); font-weight: 600;">{llm_model}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.divider()

        # 2. Navigation (Using standard buttons acting as links)
        st.markdown(f"### {t('nav_home')}") 
        
        if st.button("🏠 Home", use_container_width=True, key="nav_home"):
            st.switch_page("main.py")
            
        if st.button("📝 Editor", use_container_width=True, key="nav_editor"):
            st.switch_page("pages/1_Editor.py")
            
        if st.button("🔍 Auditoria", use_container_width=True, key="nav_audit"):
            st.switch_page("pages/3_Audit.py")

        # Spacer before Settings

        # 4. Consolidated Settings
        with st.expander("\u2699\ufe0f Settings"):
            st.markdown(f"#### {t('settings_preferences')}")
            
            # Application Language
            current_lang = "PT-BR" if st.session_state.get("lang") == "pt_br" else "EN-US"
            # We need to map back to index
            idx = 0 if current_lang == "PT-BR" else 1
            
            lang_choice = st.radio(
                "Language", 
                ["PT-BR", "EN-US"], 
                index=idx,
                key="settings_lang_radio"
            )
            
            if lang_choice == "PT-BR":
                I18n().set_lang("pt_br")
            else:
                I18n().set_lang("en_us")

            st.divider()
            
            # LLM Settings
            st.markdown("#### LLM Configuration")
            provider = st.selectbox(t("settings_llm_provider"), ["Google Gemini", "OpenAI", "Azure OpenAI", "Ollama (Local)", "OpenRouter"], key="llm_provider")
            st.text_input(t("settings_api_key"), type="password", key="llm_api_key")
            
            if provider in ["Azure OpenAI", "Ollama (Local)"]:
                st.text_input(t("settings_api_base"), key="llm_api_base")
                
            # Update session state for display
            st.session_state["llm_model"] = f"{provider.split(' ')[0]}" 

            st.divider()
            
            # Cache Control
            if st.button("🧹 Clear Cache", use_container_width=True):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.toast("Cache cleared successfully!")
                
            st.caption("DataEngOS v1.1.0")

import streamlit as st
from dataeng_os.ui.i18n_helper import t, I18n

def render_sidebar():
    """
    Renders the custom sidebar with unified navigation and settings.
    """
    with st.sidebar:
        # 1. Branding & Context
        st.markdown("## ✈️ DataEngOS")
        
        # Dynamic Project Info
        project_name = st.session_state.get("project_name", "PRJ_01_Sinergia")
        llm_model = st.session_state.get("llm_model", "Gemini 1.5 Pro")
        
        st.markdown(
            f"""
            <div style="margin-bottom: 20px; font-size: 0.8rem; color: var(--text-muted);">
                <div><b>{t('sidebar_project')}:</b> {project_name}</div>
                <div><b>{t('sidebar_model')}:</b> {llm_model}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.divider()

        # 2. Navigation (Using standard buttons acting as links)
        st.markdown(f"### {t('nav_home')}") # Using translation for Header if desired, or keep "Navigation"
        
        # ... Navigation buttons ...
        if st.button("🏠 Home", use_container_width=True, key="nav_home"):
            st.switch_page("main.py")
            
        if st.button("📝 Editor", use_container_width=True, key="nav_editor"):
            st.switch_page("pages/1_Editor.py")
            
        if st.button("🔍 Auditoria", use_container_width=True, key="nav_audit"):
            st.switch_page("pages/3_Audit.py")

        st.divider()

        # 3. Status Pill
        st.markdown(
            """
            <div style="display: flex; justify-content: center; width: 100%;">
                <div class="status-pill">
                    <span style="font-size: 8px; margin-right: 5px;">●</span> System Online
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.divider()

        # 4. Consolidated Settings
        with st.expander(f"⚙️ Settings"):
            st.markdown(f"#### {t('settings_preferences')}")
            
            # Application Language
            current_lang = "PT-BR"
            lang_choice = st.radio(
                "Language", 
                ["PT-BR", "EN-US"], 
                index=0,
                key="settings_lang"
            )
            
            if lang_choice == "PT-BR":
                I18n().set_lang("pt_br")
            else:
                I18n().set_lang("en_us")

            st.divider()
            
            # LLM Settings (Restored)
            st.markdown(f"#### LLM Configuration")
            provider = st.selectbox(t("settings_llm_provider"), ["Google Gemini", "OpenAI", "Azure OpenAI", "Ollama (Local)", "OpenRouter"], key="llm_provider")
            api_key = st.text_input(t("settings_api_key"), type="password", key="llm_api_key")
            
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
                
            st.caption(f"DataEngOS v1.1.0")

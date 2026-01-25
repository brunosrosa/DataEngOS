import streamlit as st
from dataeng_os.ui.i18n_helper import t, I18n

def render_sidebar():
    """
    Renders the custom sidebar with unified navigation and settings.
    """
    with st.sidebar:
        # 1. Branding
        st.markdown("## ✈️ DataEngOS")
        st.markdown("*Cockpit Pro*")
        
        st.divider()

        # 2. Navigation (Using standard buttons acting as links)
        st.markdown("### Navigation")
        
        if st.button("🏠 Home", use_container_width=True, key="nav_home"):
            st.switch_page("main.py")
            
        if st.button("📝 Editor", use_container_width=True, key="nav_editor"):
            st.switch_page("pages/1_Editor.py")
            
        if st.button("🔍 Auditoria", use_container_width=True, key="nav_audit"):
            st.switch_page("pages/3_Audit.py")

        st.divider()

        # 3. Status Pill (Mock System Status)
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

        # 4. Consolidated Settings (Expander)
        with st.expander("⚙️ Settings"):
            st.markdown("#### Preferences")
            
            # Language Picker
            current_lang = "PT-BR" # Default logic needs state check
            # Simple toggle logic for demo
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
            
            # Cache Control
            if st.button("🧹 Clear Cache", use_container_width=True):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.toast("Cache cleared successfully!")
                
            st.divider()
            st.caption(f"DataEngOS v1.0.0")

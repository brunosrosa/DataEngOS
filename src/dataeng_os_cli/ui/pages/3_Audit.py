import streamlit as st
from pathlib import Path
import yaml
from dataeng_os.ui.i18n_helper import t

st.set_page_config(page_title="DataEngOS - Audit", page_icon="🔍", layout="wide", initial_sidebar_state="expanded")

# Inject Custom CSS
# Inject Custom CSS
css_file = Path(__file__).parent.parent / "styles.css"
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render Custom Sidebar
from dataeng_os.ui.components.sidebar import render_sidebar # noqa: E402
render_sidebar()

# --- HEADER ---
st.markdown(
    f"""
    <div>
        <h1 style="margin-bottom: 0;">🔍 {t('audit_title')}</h1>
        <p style="color: var(--text-muted); margin-top: 0; font-size: 1.1rem;">
            {t('audit_subtitle')}
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# --- SCANNER LOGIC ---
base_path = Path("projects")
contracts_found = []
issues_found = []

if base_path.exists():
    yaml_files = list(base_path.glob("**/contracts/**/*.yaml"))
    
    for yf in yaml_files:
        try:
            with open(yf, 'r') as f:
                data = yaml.safe_load(f)
                
            dataset = data.get("dataset", {})
            issues = []
            
            # Simple Rubric
            if not dataset.get("description"):
                issues.append(t("audit_issue_missing_description"))
            if not dataset.get("owners"):
                issues.append(t("audit_issue_missing_owners"))
                
            status = "compliant" if not issues else "flagged"
            
            contracts_found.append({
                "file": yf.name,
                "path": str(yf),
                "domain": dataset.get("domain", "unknown"),
                "status": status,
                "issues": issues
            })
            
            if issues:
                issues_found.extend(issues)
                
        except Exception as e:
            contracts_found.append({
                "file": yf.name,
                "path": str(yf),
                "domain": "error",
                "status": "error",
                "issues": [f"Parse Error: {str(e)}"]
            })
            issues_found.append("Parse Error")

# --- METRICS ---
total = len(contracts_found)
compliant = len([c for c in contracts_found if c["status"] == "compliant"])
flagged = total - compliant

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(t("audit_total_contracts"), f"{total}", delta=None)
with col2:
    st.metric(t("audit_compliant"), f"{compliant}", delta=f"{int((compliant/total)*100)}%" if total > 0 else "0%")
with col3:
    st.metric(t("audit_issues"), f"{len(issues_found)}", delta=f"-{len(issues_found)}", delta_color="inverse")

st.divider()

# --- RESULTS LIST ---
st.subheader(t("audit_detailed_report"))

# Search Filter
search_term = st.text_input(t("audit_filter_placeholder"))

if search_term:
    contracts_found = [c for c in contracts_found if search_term.lower() in c['file'].lower() or search_term.lower() in c['domain'].lower()]

if not contracts_found:
    if search_term:
        st.info(f"{t('audit_no_match')} '{search_term}'.")
    else:
        st.info(t("audit_project_empty"))
else:
    for c in contracts_found:
        status_color = "var(--success)" if c["status"] == "compliant" else "var(--danger)"
        status_icon = "✅" if c["status"] == "compliant" else "⚠️"
        
        with st.container():
            st.markdown(
                f"""
                <div class="css-card" style="border-left: 4px solid {status_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-family: 'Fira Code', monospace; font-weight: bold; font-size: 1.1rem;">
                            {status_icon} {c['file']}
                        </span>
                        <span class="status-pill" style="color: {status_color}; border-color: {status_color}; background-color: transparent;">
                            {c['domain']}
                        </span>
                    </div>
                    <div style="margin-top: 0.5rem; color: var(--text-muted);">
                        Path: <code>{c['path']}</code>
                    </div>
                    {'<div style="margin-top: 0.5rem; color: var(--danger);">🛑 Issues: ' + ', '.join(c['issues']) + '</div>' if c['issues'] else ''}
                </div>
                """,
                unsafe_allow_html=True
            )

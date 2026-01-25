import streamlit as st
import yaml
from pathlib import Path
from dataeng_os.models.odcs import DataContract, Dataset, Schema, Column, SLA, Owner, DataContractSpec
from dataeng_os.ui.architect import architect
from dataeng_os.ui.i18n_helper import t
from dataeng_os.ui.components.lineage import render_lineage
from dataeng_os.ui.components.diff_viewer import render_diff

st.set_page_config(page_title="DataEngOS - Editor", page_icon="📝", layout="wide", initial_sidebar_state="expanded")

# Inject Custom CSS
with open("dataeng_os/ui/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render Custom Sidebar
from dataeng_os.ui.components.sidebar import render_sidebar # noqa: E402
render_sidebar()


# --- WIZARD HANDLER ---
wizard_intent = st.session_state.get("wizard_intent")
draft_data = {}

if wizard_intent:
    st.info(f"🤖 The Architect detected you want to work on: **{wizard_intent}**")
    with st.spinner("Generating draft contract..."):
        draft_data = architect.generate_draft(wizard_intent)
        # Clear intent so it doesn't trigger on refresh
        st.session_state.pop("wizard_intent") 

st.title(f"📝 {t('nav_editor')}")

tabs = st.tabs([t("tab_editor"), t("tab_validator"), t("tab_catalog"), "Lineage"])

# --- TAB 1: EDITOR ---
with tabs[0]:
    st.header(t("tab_editor"))
    
    # Pre-fill data if draft exists
    d_dataset = draft_data.get("dataset", {})
    d_schema = draft_data.get("schema", [])
    d_slas = draft_data.get("slas", {})
    
    # --- SECTION 1: METADATA ---
    with st.container(border=True):
        st.markdown(f"### {t('editor_section_metadata')}")
        col1, col2 = st.columns(2)
        domain = col1.text_input(t("contract_domain"), value=d_dataset.get("domain", "marketing"))
        logical_name = col2.text_input(t("contract_logical_name"), value=d_dataset.get("logical_name", "user_clicks"))
        
        col_phy, col_desc = st.columns([1, 2])
        physical_name = col_phy.text_input(t("contract_physical_name"), value=d_dataset.get("physical_name", "raw_user_clicks_v1"))
        description = col_desc.text_input(t("contract_description"), value=d_dataset.get("description", "Stream of user clicks on the website."))
        
        st.markdown(f"**{t('editor_owners_label')}**")
        col3, col4 = st.columns(2)
        owners = d_dataset.get("owners", [{"team": "Data Eng", "email": "data@company.com"}])
        owner_team = col3.text_input(t("contract_owner_team"), value=owners[0]["team"])
        owner_email = col4.text_input(t("contract_owner_email"), value=owners[0]["email"])

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SECTION 2: SCHEMA ---
    with st.container(border=True):
        c_head, c_btn = st.columns([5, 1])
        c_head.markdown(f"### {t('editor_section_schema')}")
        
        # Dynamic Columns State
        if "columns" not in st.session_state or wizard_intent:
            initial_cols = d_schema if d_schema else [
                {"name": "id", "type": "string", "desc": "User ID", "pk": True},
                {"name": "ts", "type": "timestamp", "desc": "Event Time", "pk": False},
                {"name": "url", "type": "string", "desc": "Page URL", "pk": False}
            ]
            st.session_state.columns = initial_cols

        def add_column():
            st.session_state.columns.append({"name": "", "type": "string", "desc": "", "pk": False})

        def remove_column(index):
            st.session_state.columns.pop(index)

        c_btn.button(t("schema_add_column"), on_click=add_column, type="primary")

        # Table Header
        h1, h2, h3, h4, h5 = st.columns([3, 2, 4, 1, 1])
        h1.caption(f"**{t('schema_col_name')}**")
        h2.caption(f"**{t('schema_col_type')}**")
        h3.caption(f"**{t('schema_col_desc')}**")
        h4.caption(f"**{t('schema_col_pk')}**")

        columns_data = []
        for i, col in enumerate(st.session_state.columns):
            c1, c2, c3, c4, c5 = st.columns([3, 2, 4, 1, 1])
            col['name'] = c1.text_input(t("schema_col_name"), value=col['name'], key=f"cname_{i}", label_visibility="collapsed")
            col['type'] = c2.selectbox(t("schema_col_type"), ["string", "int", "timestamp", "decimal", "boolean"], index=0 if col['type']=="string" else 1, key=f"ctype_{i}", label_visibility="collapsed")
            col['desc'] = c3.text_input(t("schema_col_desc"), value=col['desc'], key=f"cdesc_{i}", label_visibility="collapsed")
            col['pk'] = c4.checkbox(t("schema_col_pk"), value=col['pk'], key=f"cpk_{i}", label_visibility="collapsed")
            if c5.button("🗑️", key=f"del_{i}"):
                remove_column(i)
                st.rerun()
            
            if col['name']:
                columns_data.append(Column(
                    name=col['name'], 
                    type=col['type'], 
                    description=col['desc'], 
                    primary_key=col['pk']
                ))

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- SECTION 3: SLAs ---
    with st.container(border=True):
        st.markdown(f"### {t('editor_section_sla')}")
        col_sla1, col_sla2 = st.columns(2)
        freq = col_sla1.selectbox("Frequency", ["daily", "hourly", "streaming", "batch"])
        fresh = col_sla2.text_input("Freshness (e.g. 24h)", value="24h")

    st.divider()

    # Generate current YAML state
    try:
        current_contract = DataContract(
            version="2.2.0",
            spec=DataContractSpec(
                dataset=Dataset(
                    domain=domain,
                    logical_name=logical_name,
                    physical_name=physical_name,
                    description=description,
                    owners=[Owner(team=owner_team, email=owner_email)]
                ),
                schema=Schema(columns=columns_data),
                slas=SLA(frequency=freq, freshness=fresh)
            )
        )
        current_yaml = yaml.dump(current_contract.model_dump(by_alias=True, exclude_none=True), sort_keys=False)
        
        # Check against loaded contract (if any)
        if "loaded_yaml_content" in st.session_state:
            with st.expander("👀 Review Changes (Diff)"):
                render_diff(st.session_state["loaded_yaml_content"], current_yaml)
                
    except Exception as e:
        current_yaml = ""
        st.warning(f"Could not generate preview: {e}")

    if st.button(t("btn_generate_yaml"), type="primary"):
        if current_yaml:
            st.code(current_yaml, language="yaml")
            st.success(t("success_contract_generated"))
        else:
            st.error(t("error_generating_contract"))

# --- TAB 2: VALIDATOR ---
with tabs[1]:
    st.header(t("tab_validator"))
    uploaded_file = st.file_uploader(t("upload_instruction"), type="yaml")
    if uploaded_file:
        try:
            data = yaml.safe_load(uploaded_file)
            DataContract(**data)
            st.success(t("validator_success"))
        except Exception as e:
            st.error(f"{t('validator_fail')}: {e}")

# --- TAB 3: CATALOG (REAL SCAN) ---
with tabs[2]:
    st.header(t("tab_catalog"))
    base_path = Path("projects")
    
    if not base_path.exists():
        st.warning(f"Directory 'projects/' not found. Working dir: {Path.cwd()}")
    else:
        st.info(f"{t('catalog_scanning')} 'projects/'...")
        contracts = list(base_path.glob("**/contracts/**/*.yaml"))
        
        if not contracts:
            st.warning(t("catalog_empty"))
        else:
            for c in contracts:
                with st.expander(f"📄 {c.name} ({c.parent.parent.name})"):
                    st.text(str(c))
                if st.button("Load", key=f"load_{c}"):
                        st.session_state["loaded_contract"] = str(c)
                        with open(c, 'r') as f:
                            content = f.read()
                            st.session_state["loaded_yaml_content"] = content
                            st.code(content, language="yaml")
                            # Trigger a rerun to update the Editor tab state if we were propagating values back
                            # For MVP we are not auto-filling the form from catalog yet (as per previous limitations)
                            # But we can simulate a 'fresh start' for diffing purposes.

# --- TAB 4: LINEAGE ---
with tabs[3]:
    st.header("Lineage Graph")
    # Use current logical name from editor
    current_node = logical_name if logical_name else "Unknown_Dataset"
    
    st.info("Visualizing upstream dependencies based on SQL parsing (Mocked for V1).")
    render_lineage(current_node)

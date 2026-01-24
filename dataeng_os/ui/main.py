import streamlit as st
import yaml
from pathlib import Path
from dataeng_os.models.odcs import DataContract, Dataset, Schema, Column, QualityRule, SLA, Owner

st.set_page_config(page_title="DataEngOS Cockpit", page_icon="✈️", layout="wide")

st.title("✈️ DataEngOS Cockpit")
st.markdown("### Create and Manage Data Contracts without YAML")

tabs = st.tabs(["Contract Editor", "Validator", "Catalog"])

with tabs[0]:
    st.header("Contract Editor")
    
    with st.expander("1. Dataset Metadata", expanded=True):
        col1, col2 = st.columns(2)
        domain = col1.text_input("Domain", value="marketing")
        logical_name = col2.text_input("Logical Name (Entity)", value="user_clicks")
        physical_name = st.text_input("Physical Name (Table/File)", value="raw_user_clicks_v1")
        description = st.text_area("Description", value="Stream of user clicks on the website.")
        
        st.subheader("Owners")
        owner_team = st.text_input("Owner Team", value="Data Engineering")
        owner_email = st.text_input("Owner Email", value="data@company.com")

    with st.expander("2. Schema Definition", expanded=True):
        st.info("Define your columns below.")
        
        # Simple dynamic list simulation using session state would be better, 
        # but for V1 we keep it static or use a text area for quick bulk edit could be an option.
        # Let's do a simple 3 column boilerplate for now.
        
        columns_data = []
        num_cols = st.number_input("Number of Columns", min_value=1, value=3)
        
        for i in range(int(num_cols)):
            c1, c2, c3, c4 = st.columns([2, 1, 2, 1])
            c_name = c1.text_input(f"Col {i+1} Name", key=f"cname_{i}")
            c_type = c2.selectbox(f"Type", ["string", "int", "timestamp", "decimal", "boolean"], key=f"ctype_{i}")
            c_desc = c3.text_input(f"Description", key=f"cdesc_{i}")
            c_pk = c4.checkbox("PK?", key=f"cpk_{i}")
            
            if c_name:
                columns_data.append(Column(
                    name=c_name, 
                    type=c_type, 
                    description=c_desc, 
                    primary_key=c_pk
                ))

    with st.expander("3. SLAs & Quality"):
        freq = st.selectbox("Frequency", ["daily", "hourly", "streaming", "batch"])
        fresh = st.text_input("Freshness (e.g. 24h)", value="24h")

    if st.button("Generate Contract YAML"):
        try:
            # Construct Model
            contract = DataContract(
                version="2.2.0",
                spec={
                    "dataset": Dataset(
                        domain=domain,
                        logical_name=logical_name,
                        physical_name=physical_name,
                        description=description,
                        owners=[Owner(team=owner_team, email=owner_email)]
                    ),
                    "schema": Schema(columns=columns_data),
                    "slas": SLA(frequency=freq, freshness=fresh)
                }
            )
            
            # Dump to YAML
            yaml_str = yaml.dump(contract.model_dump(by_alias=True, exclude_none=True), sort_keys=False)
            st.code(yaml_str, language="yaml")
            st.success("Valid ODCS Contract generated!")
            
        except Exception as e:
            st.error(f"Error generating contract: {e}")

with tabs[1]:
    st.header("Validator")
    uploaded_file = st.file_uploader("Upload .yaml contract", type="yaml")
    if uploaded_file:
        try:
            data = yaml.safe_load(uploaded_file)
            DataContract(**data)
            st.success(f"✅ Contract '{data.get('spec', {}).get('dataset', {}).get('logical_name')}' is VALID.")
        except Exception as e:
            st.error(f"❌ Validation Failed: {e}")

with tabs[2]:
    st.header("Catalog")
    st.write("Scan 'projects/' folder to list existing contracts...")
    # Implementation optional for V1
    base_path = Path("projects")
    if base_path.exists():
        contracts = list(base_path.glob("**/contracts/**/*.yaml"))
        for c in contracts:
            st.text(str(c))

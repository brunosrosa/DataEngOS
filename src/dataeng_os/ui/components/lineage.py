import streamlit as st
import streamlit.components.v1 as components
from typing import Optional, List

def render_lineage(contract_name: str, dependencies: Optional[List[str]] = None):
    """
    Renders a lineage graph. 
    Prioritizes Graphviz if available. 
    Falls back to Mermaid JS.
    """
    if dependencies is None:
        dependencies = ["upstream_system_a", "upstream_table_b"]

    # Try Graphviz First
    try:
        import graphviz # type: ignore
        # Check if dot executable exists
        # This check might fail if graphviz lib is installed but dot binary is not
        
        graph = graphviz.Digraph()
        graph.attr(rankdir='LR')
        graph.attr('node', shape='box', style='filled', fillcolor='lightblue')
        
        # Current Node
        graph.node(contract_name, fillcolor='gold')
        
        # Upstream
        for dep in dependencies:
            graph.node(dep, fillcolor='lightgrey')
            graph.edge(dep, contract_name)
        
        # Mock Downstream
        graph.node("dwh_marts", fillcolor='lightgreen')
        graph.edge(contract_name, "dwh_marts")
        
        st.graphviz_chart(graph)
        
    except Exception as e:
        # Fallback to Mermaid
        st.warning(f"Graphviz not available ({e}). Using Mermaid fallback.")
        render_mermaid(contract_name, dependencies)

def render_mermaid(contract_name, dependencies):
    # Construct Mermaid Graph Definition
    mermaid_code = "graph LR;\n"
    
    # Styles
    mermaid_code += "    classDef current fill:#f9f,stroke:#333,stroke-width:2px;\n"
    mermaid_code += "    classDef external fill:#eee,stroke:#333;\n"
    
    # Nodes
    # Sanitize names (replace spaces)
    c_safe = contract_name.replace(" ", "_")
    mermaid_code += f"    {c_safe}[{contract_name}]:::current;\n"
    
    for dep in dependencies:
        d_safe = dep.replace(" ", "_")
        mermaid_code += f"    {d_safe}[{dep}]:::external --> {c_safe};\n"

    # Mock Downstream
    mermaid_code += f"    {c_safe} --> dwh_marts[DWH Marts]:::external;\n"

    # Render using html component with mermaid.js cdn
    # Or just simple text if that fails too complex
    
    html = f"""
    <div class="mermaid">
    {mermaid_code}
    </div>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{ startOnLoad: true }});
    </script>
    """
    components.html(html, height=200)

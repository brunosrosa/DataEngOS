import streamlit as st
import difflib

def render_diff(old_text: str, new_text: str):
    """
    Renders a side-by-side or unified diff of two strings using HTML. 
    """
    if not old_text:
        st.info("No original version to compare (New Contract).")
        return

    diff = difflib.unified_diff(
        old_text.splitlines(),
        new_text.splitlines(),
        fromfile='Original',
        tofile='Current Draft',
        lineterm=''
    )
    
    diff_text = "\n".join(list(diff))
    
    if not diff_text:
        st.success("No changes detected.")
        return

    # Colored Diff rendering
    st.markdown("### Changes Detected")
    
    # We can use st.code with diff language for simple highlighting
    st.code(diff_text, language="diff")

    # Or we could do a more complex HTML render if needed, but st.code("diff") is usually sufficient for MVP.

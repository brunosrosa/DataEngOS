import streamlit as st
import time
import textwrap

def render_glass_card(content: str, header: str = None, height: str = "240px", animation: bool = True):
    """
    Renders a container with glassmorphism style and standardized header.
    Height defaults to 240px for row alignment.
    """
    anim_class = "animate-fade-in" if animation else ""
    header_html = f'<div class="card-header">{header}</div>' if header else ""
    
    # Use flex column to ensure content fills the space
    return textwrap.dedent(f"""
    <div class="glass-card {anim_class}" style="min-height: {height}; display: flex; flex-direction: column;">
        {header_html}
        <div style="flex-grow: 1; position: relative;">
            {content}
        </div>
    </div>
    """).strip().replace('\n', '')

# ... (skeleton_loader unchanged but shown for context matching if needed, skipping for brevity of instructions)

def skeleton_loader(lines: int = 3):
    # ... (content remains same)
    skel_css = """
    <style>
    @keyframes shimmer {
        0% { background-position: -468px 0; }
        100% { background-position: 468px 0; }
    }
    .skeleton-box {
        display: inline-block;
        height: 1em;
        position: relative;
        overflow: hidden;
        background-color: #1e293b;
        background-image: linear-gradient(to right, #1e293b 0%, #334155 20%, #1e293b 40%, #1e293b 100%);
        background-repeat: no-repeat;
        background-size: 800px 104px; 
        animation-duration: 1s;
        animation-fill-mode: forwards; 
        animation-iteration-count: infinite;
        animation-name: shimmer;
        animation-timing-function: linear;
        border-radius: 4px;
        margin-bottom: 8px;
        width: 100%;
    }
    </style>
    """
    
    html = skel_css
    for _ in range(lines):
        html += '<div class="skeleton-box"></div>'
    
    st.markdown(html, unsafe_allow_html=True)

def toast_agent(message: str, type: str = "success"):
    """
    Shows a toast notification with 'Agent' personality.
    """
    icon = "🤖" if type == "info" else "✅"
    if type == "error": icon = "🛑"
    
    st.toast(f"{icon} [Architect]: {message}", icon=None)

def render_health_pill(status: str = "Online"):
    color = "#10B981" if status == "Online" else "#EF4444"
    anim = "online" if status == "Online" else ""
    # Render as a small sleek badge
    return textwrap.dedent(f"""
    <div class="status-pill {anim}" style="background-color: rgba(16, 185, 129, 0.1); color: {color}; border: 1px solid {color}; padding: 2px 8px; font-size: 0.6rem; display: inline-flex; align-items: center; border-radius: 12px;">
        <span style="font-size: 6px; margin-right: 4px;">●</span> {status}
    </div>
    """).strip()

def render_quality_gauge(score: int):
    """
    Renders a circular progress gauge (Centered Flex).
    """
    return textwrap.dedent(f"""
    <div class="gauge-container" style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center;">
        <div style="position: relative; width: 120px; height: 120px;">
            <svg width="120" height="120" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="none" stroke="#1e293b" stroke-width="8" />
                <circle cx="50" cy="50" r="45" fill="none" stroke="#F97316" stroke-width="8"
                        stroke-dasharray="283" stroke-dashoffset="{283 - (283 * score / 100)}"
                        transform="rotate(-90 50 50)" stroke-linecap="round"
                        style="transition: stroke-dashoffset 1s ease-out;" />
            </svg>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                <div style="font-size: 1.8rem; font-weight: bold; color: #F8FAFC; line-height: 1;">{score}%</div>
                <div style="font-size: 0.6rem; color: #94A3B8; letter-spacing: 1px; margin-top: 2px;">TRUST</div>
            </div>
        </div>
    </div>
    """).strip()

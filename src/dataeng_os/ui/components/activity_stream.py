import streamlit as st
import random
import time
import textwrap

def render_activity_stream(height: int = 240): # Match card height
    """
    Renders a scrolling 'Timeline' feed of agent activities.
    """
    
    # Mock Data
    activities = [
        {"agent": "Architect", "action": "Scanning project structure...", "time": "Just now", "status": "info"},
        {"agent": "dbt-01", "action": "Verified model stg_users", "time": "2s ago", "status": "success"},
        {"agent": "dbt-01", "action": "Found unique key violation", "time": "15s ago", "status": "error"},
        {"agent": "Gov-Bot", "action": "PII detected in email column", "time": "1m ago", "status": "warning"},
        {"agent": "Airflow", "action": "Triggered DAG: daily_ingest", "time": "2m ago", "status": "success"},
        {"agent": "Architect", "action": "Optimized lineage graph", "time": "5m ago", "status": "info"},
    ]
    
    # Header is now handled by the glass card wrapper in main.py, but we can keep title inside if preferred.
    # Actually, main.py passes header="Agent Neural Link". So we just render content.
    
    html_content = '<div class="activity-stream" style="height: 180px; overflow-y: auto; padding-right: 5px;">'
    
    for activity in activities:
        dot_color = "#3B82F6" # info
        if activity["status"] == "success": dot_color = "#10B981"
        if activity["status"] == "error": dot_color = "#EF4444"
        if activity["status"] == "warning": dot_color = "#F59E0B"
        
        # Dedent each item block
        item_html = textwrap.dedent(f"""
        <div class="timeline-item" style="--dot-color: {dot_color};">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
                <span style="color: {dot_color}; font-weight: 600; font-size: 0.8rem;">{activity['agent']}</span>
                <span style="color: #64748B; font-size: 0.7rem;">{activity['time']}</span>
            </div>
            <div style="color: #CBD5E1; font-size: 0.8rem; margin-top: 2px;">{activity['action']}</div>
        </div>
        """)
        html_content += item_html
    
    html_content += '</div>'
    return html_content

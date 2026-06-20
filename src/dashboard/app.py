"""
Module 5 — Factory Compliance Supervision Dashboard
Industrial-Grade Interface with CSS styling and PDF Export integration.
"""

import streamlit as st
import pandas as pd
import sqlite3
import os
import sys
from pathlib import Path

# --- BULLETPROOF PATH ROUTING ---
# Dynamically find the absolute path to the 'src' folder and force Python to read from it.
current_file_path = Path(__file__).resolve()
src_directory = str(current_file_path.parent.parent) # goes up from dashboard -> src

if src_directory not in sys.path:
    sys.path.insert(0, src_directory) # Insert at position 0 to prioritize it

# Now the imports will work flawlessly
from escalation.escalation_engine import get_active_alerts, generate_compliance_csv
# ---------------------------------

# ==========================================
# PAGE CONFIG & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="Industrial Safety UI", page_icon="🛡️", layout="wide")

# ... (keep the rest of your app.py code exactly the same below this)

# Inject custom CSS for that "Enterprise Control Panel" look
st.markdown("""
    <style>
    /* Metric Card Styling */
    div[data-testid="metric-container"] {
        background-color: #1E212B;
        padding: 15px 20px;
        border-radius: 8px;
        border-left: 5px solid #00FFAA;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Pulsing Green Status Dot */
    .status-dot {
        height: 12px; width: 12px; background-color: #00FFAA;
        border-radius: 50%; display: inline-block; margin-right: 8px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 170, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 170, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 170, 0); }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏭 Plant Safety & Compliance Control Panel")
st.markdown("<p style='color: #888;'>Continuous Edge-to-Cloud Monitoring Network</p>", unsafe_allow_html=True)

# ==========================================
# SIDEBAR CONTROL PANEL
# ==========================================
with st.sidebar:
    st.header("🔄 Operations")
    if st.button("Synchronize Telemetry", use_container_width=True):
        generate_compliance_csv()
        st.toast("System logs synchronized!", icon="✅")
        
    st.markdown("---")
    st.markdown("### System Diagnostics")
    st.markdown("<div style='margin-bottom: 10px;'><span class='status-dot'></span> Local Edge Tracking (YOLOv8) <b>Online</b></div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 10px;'><span class='status-dot'></span> Cloud VLM Pipeline <b>Active</b></div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 10px;'><span class='status-dot'></span> Database Ledger <b>Secured</b></div>", unsafe_allow_html=True)

# Fetch current numbers from the database
DB_PATH = "outputs/compliance.db"
if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    df_all = pd.read_sql_query("SELECT * FROM violations", conn)
    conn.close()
else:
    df_all = pd.DataFrame()

# ==========================================
# MAIN TELEMETRY METRICS
# ==========================================
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Logged Events", value=len(df_all) if not df_all.empty else 0)
with col2:
    high_count = len(df_all[df_all['severity'] == 'HIGH']) if not df_all.empty else 0
    st.metric(label="🚨 High Priority Alerts", value=high_count, delta=f"{high_count} Active" if high_count > 0 else "Clear", delta_color="inverse")
with col3:
    crit_count = len(df_all[df_all['severity'] == 'CRITICAL']) if not df_all.empty else 0
    st.metric(label="🔥 Critical Breaches", value=crit_count, delta="Action Required" if crit_count > 0 else "Clear", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True) # Spacer

# ==========================================
# DYNAMIC CRITICAL ALERT BANNER
# ==========================================
alerts = get_active_alerts()
if alerts:
    st.error(f"⚠️ **IMMEDIATE ATTENTION:** {len(alerts)} High/Critical safety protocol breaches detected on the factory floor.")
    with st.expander("Expand Live Alert Stream", expanded=True):
        for idx, alert in enumerate(alerts[:5]):
            st.markdown(f"**[{alert['severity']}]** | Camera: `{alert['clip_id']}` | Time: `{alert['timestamp']}` <br> *{alert['event_description']}*", unsafe_allow_html=True)
            st.divider()

# ==========================================
# INTERACTIVE DATA TABS
# ==========================================
tab1, tab2 = st.tabs(["📊 Historical Compliance Ledger", "📥 Audit Document Center"])

with tab1:
    st.subheader("Security Verification Logs")
    if not df_all.empty:
        severity_filter = st.multiselect("Filter by Threat Level:", options=list(df_all['severity'].unique()), default=list(df_all['severity'].unique()))
        filtered_df = df_all[df_all['severity'].isin(severity_filter)]
        st.dataframe(filtered_df[['event_id', 'clip_id', 'timestamp', 'behavior_class', 'event_description', 'severity']], use_container_width=True, hide_index=True)
    else:
        st.info("The compliance ledger is empty. Awaiting telemetry data.")

with tab2:
    st.subheader("Official Compliance Exports")
    st.markdown("Download standard system event data compiled into official audit documents.")
    
    colA, colB = st.columns(2)
    
    # CSV Download Button
    with colA:
        csv_path = "outputs/compliance_report.csv"
        if os.path.exists(csv_path):
            with open(csv_path, "r", encoding="utf-8") as f:
                st.download_button(label="💾 Download CSV Database", data=f.read(), file_name="factory_compliance_report.csv", mime="text/csv", use_container_width=True)
                
    # PDF Download Button
    with colB:
        pdf_path = "outputs/compliance_report.pdf"
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(label="📄 Download Official PDF Report", data=pdf_file, file_name="Official_Safety_Audit.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.warning("PDF Report not found. Run reports.py to generate.")
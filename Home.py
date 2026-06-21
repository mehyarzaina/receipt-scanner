# imports 
import streamlit as st
from styles import GLOBAL_CSS

# configure how the page looks
st.set_page_config(
    page_title="Receipt Manager", # Browser tab title
    page_icon="🧾",
    layout="centered",
    initial_sidebar_state="collapsed", # Sidebar starts hidden
)

# ── Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 3rem 0 2rem;">
    <h1 style="font-size:2.8rem; font-weight:700; letter-spacing:-1px; margin-bottom:0.6rem;">
        Smart Receipt Tracking
    </h1>

""", unsafe_allow_html=True)

# ── Two Action Cards ─────────────────────────────────────────────────────
col1, spacer, col2 = st.columns([1, 0.08, 1]) # create 3 columns

with col1:
    st.markdown("""
    <div class="card" style="text-align:center; cursor:pointer; min-height:220px;
         display:flex; flex-direction:column; align-items:center; justify-content:center; gap:1rem;">
        <div style="
            width:64px; height:64px; border-radius:16px;
            background: rgba(108,99,255,0.15);
            border: 1px solid rgba(108,99,255,0.3);
            display:flex; align-items:center; justify-content:center;
            font-size:1.8rem;
        ">📄</div>
            <div style="font-size:1.1rem; font-weight:600; margin-bottom:0.3rem;">Upload Receipt</div>
    </div>
    """, unsafe_allow_html=True)

    # button
    if st.button("Open Upload", key="btn_upload", use_container_width=True):
        st.switch_page("pages/1_Upload_Receipt.py")

with col2:
    st.markdown("""
    <div class="card" style="text-align:center; cursor:pointer; min-height:220px;
         display:flex; flex-direction:column; align-items:center; justify-content:center; gap:1rem;">
        <div style="
            width:64px; height:64px; border-radius:16px;
            background: rgba(52,211,153,0.12);
            border: 1px solid rgba(52,211,153,0.25);
            display:flex; align-items:center; justify-content:center;
            font-size:1.8rem;
        ">🗂️</div>
        <div>
            <div style="font-size:1.1rem; font-weight:600; margin-bottom:0.3rem;">View History</div>
      </div>
    """, unsafe_allow_html=True)

    # button
    if st.button("Open History", key="btn_history", use_container_width=True):
        st.switch_page("pages/2_History.py")


# imports
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from styles import GLOBAL_CSS
from database.database import get_session, engine
from database.models import Receipt, Item
from sqlmodel import select
import pandas as pd


st.set_page_config(page_title="Receipt History", page_icon="🗂️", layout="wide", initial_sidebar_state="collapsed")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────
col_back, col_title = st.columns([0.12, 0.88])
with col_back:
    if st.button("← Back", key="back_hist"):
        st.switch_page("Home.py")
with col_title:
    st.markdown("<h1 style='margin:0'>🗂️ Receipt History</h1>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Load all receipts ─────────────────────────────────────────────────────
@st.cache_data(ttl=10)
def load_receipts():
    try:
        session = get_session()
        receipts = session.exec(select(Receipt)).all()
        session.close()
        return receipts
    except Exception as e:
        st.error(f"Failed to load receipts: {e}")
        return []

receipts = load_receipts()

if not receipts:
    st.markdown("""
    <div class="card" style="text-align:center; padding: 3rem; color:#6b7280;">
        <div style="font-size:3rem; margin-bottom:1rem;">🧾</div>
        <div style="font-size:1.1rem; font-weight:500;">No receipts yet</div>
        <div style="margin-top:0.5rem; font-size:0.88rem;">Upload your first receipt to get started.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Filters ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot" style="background:#fbbf24;"></div>
    <span style="font-weight:600;">Filters</span>
</div>
""", unsafe_allow_html=True)

all_shops = sorted(set(r.shop_name for r in receipts if r.shop_name))
all_dates = sorted(set(r.date for r in receipts if r.date))

fcol1, fcol2, fcol3, fcol4 = st.columns(4)
with fcol1:
    shop_filter = st.selectbox("Shop Name", ["All"] + all_shops, key="f_shop")
with fcol2:
    date_from = st.date_input("Date From", value=None, key="f_date_from")
with fcol3:
    date_to = st.date_input("Date To", value=None, key="f_date_to")
with fcol4:
    search_num = st.text_input("Receipt #", placeholder="Search by number...", key="f_num")

# ── Apply filters ─────────────────────────────────────────────────────────
filtered = receipts

if shop_filter != "All":
    filtered = [r for r in filtered if r.shop_name == shop_filter]

if date_from:
    filtered = [r for r in filtered if r.date and r.date >= str(date_from)]

if date_to:
    filtered = [r for r in filtered if r.date and r.date <= str(date_to)]

if search_num.strip():
    filtered = [r for r in filtered if str(r.receipt_num).startswith(search_num.strip())]

st.markdown("<hr>", unsafe_allow_html=True)

# ── Stats bar ─────────────────────────────────────────────────────────────
mc1, mc2, mc3 = st.columns(3)
mc1.metric("Total Receipts", len(filtered))
mc2.metric("Total Spent", f"{sum(r.grand_total or 0 for r in filtered):.3f}")
mc3.metric("Shops", len(set(r.shop_name for r in filtered if r.shop_name)))

st.markdown("<hr>", unsafe_allow_html=True)

# ── Table ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <span style="font-weight:600;">Receipts</span>
</div>
""", unsafe_allow_html=True)

if not filtered:
    st.info("No receipts match the current filters.")
    st.stop()

# Table header
hcols = st.columns([0.12, 0.25, 0.15, 0.18, 0.15, 0.15])
headers = ["Receipt Number", "Shop Name", "Date", "Grand Total", "Image", "Action"]
for col, hdr in zip(hcols, headers):
    col.markdown(f'<span style="color:#6b7280;font-size:0.72rem;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;">{hdr}</span>', unsafe_allow_html=True)

st.markdown('<div style="border-top:1px solid #2a2d3a;margin:0.4rem 0;"></div>', unsafe_allow_html=True)

for r in sorted(filtered, key=lambda x: x.receipt_num or 0, reverse=True):
    row = st.columns([0.12, 0.25, 0.15, 0.18, 0.15, 0.15])

    with row[0]:
        st.markdown(f'<div style="font-family:JetBrains Mono,monospace;font-weight:600;color:#8b85ff;padding:0.6rem 0;"># {r.receipt_num}</div>', unsafe_allow_html=True)

    with row[1]:
        st.markdown(f'<div style="padding:0.6rem 0;">{r.shop_name or "—"}</div>', unsafe_allow_html=True)

    with row[2]:
        st.markdown(f'<div style="padding:0.6rem 0;color:#9ca3af;">{r.date or "—"}</div>', unsafe_allow_html=True)

    with row[3]:
        total_str = f"{r.grand_total:.3f} {r.currency}" if r.grand_total is not None else "—"
        st.markdown(f'<div style="padding:0.6rem 0;font-weight:600;color:#34d399;">{total_str}</div>', unsafe_allow_html=True)

    with row[4]:
        if r.receipt_filename:
            st.markdown(
                f'<div style="padding:0.5rem 0;"><span class="badge badge-success">📷 {r.receipt_filename[-12:] if len(r.receipt_filename)>12 else r.receipt_filename}</span></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<div style="padding:0.5rem 0;color:#374151;font-size:0.82rem;">No image</div>', unsafe_allow_html=True)

    with row[5]:
        if st.button("👁 View", key=f"open_{r.id}"):
            # Load receipt items
            session = get_session()
            items = session.exec(select(Item).where(Item.receipt_id == r.id)).all()

            session.close()

            # Populate session state
            st.session_state["receipt_num"]  = str(r.receipt_num)
            st.session_state["shop_name"]    = r.shop_name or ""
            try:
                from datetime import datetime as dt
                st.session_state["date_val"] = dt.strptime(r.date, "%Y-%m-%d").date() if r.date else None
            except Exception:
                st.session_state["date_val"] = None
            st.session_state["currency"]     = r.currency or "JOD"
            st.session_state["items"]        = [
                {"product_name": it.product_name or "",
                 "quantity": float(it.quantity or 1),
                 "price": float(it.price or 0)}
                for it in items
            ]
            st.session_state["subtotal"]     = r.subtotal or 0.0
            st.session_state["tax_amount"]   = r.tax_amount or 0.0
            st.session_state["tax_amount_input"] = r.tax_amount or 0.0   # ← add here
            st.session_state["grand_total"]  = r.grand_total or 0.0
            st.session_state["image_bytes"]  = None
            st.session_state["image_name"]   = r.receipt_filename
            st.session_state["image_mime"]   = None
            st.session_state["mode"]         = "manual"
            st.session_state["view_mode"]    = True   # ← read-only flag
            st.session_state["ocr_done"]     = False
            st.switch_page("pages/1_Upload_Receipt.py")

    st.markdown('<div style="border-top:1px solid #1e2130;"></div>', unsafe_allow_html=True)
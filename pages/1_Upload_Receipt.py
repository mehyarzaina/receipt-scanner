# imports
import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from styles import GLOBAL_CSS
from gemini_function import extract_receipt_data, extract_single_field, extract_items_field
from datetime import datetime
from helpers import (
    get_image_mime,
    next_item_id, 
    make_item,
    init_form_state,
    recalculate, 
    apply_ocr_data,
    save_receipt,
    clear_form,
    CURRENCIES
)

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="Upload Receipt",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Init ─────────────────────────────────────────────────────
init_form_state()

is_readonly   = st.session_state.get("view_mode", False)
is_auto       = st.session_state.get("mode") == "auto"
can_reextract = is_auto and not is_readonly and bool(st.session_state.get("image_bytes"))

# ── Header ───────────────────────────────────────────────────
col_back, col_title = st.columns([0.15, 0.85])
with col_back:
    if st.button("← Back"):
        clear_form()
        st.switch_page("Home.py")
with col_title:
    title = "🔍 View Receipt" if is_readonly else "📄 Upload Receipt"
    st.markdown(f"<h1 style='margin:0'>{title}</h1>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True) # adds a horizontal line

# ── Mode Selection ───────────────────────────────────────────
if not is_readonly and not st.session_state.get("mode"):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Manual Entry", use_container_width=True):
            st.session_state["mode"] = "manual"
            st.rerun()
    with col2:
        if st.button("AI Auto Extract", use_container_width=True):
            st.session_state["mode"] = "auto"
            st.rerun()
    st.stop()

# ── Auto Upload & Analyze ────────────────────────────────────
if is_auto and not is_readonly:
    uploaded = st.file_uploader(
        "Upload Receipt Image",
        type=["png", "jpg", "jpeg", "webp", "gif", "bmp", "tiff", "heic"]
    )
    if uploaded:
        st.session_state["image_bytes"] = uploaded.read()
        st.session_state["image_mime"]  = get_image_mime(uploaded.name)
        st.session_state["image_name"]  = uploaded.name

    # show image after upload
    if st.session_state.get("image_bytes"):
        st.image(st.session_state["image_bytes"], width=400)

        # Shows loading UI while OCR runs
        if st.button("Analyze Receipt"):
            with st.spinner("Extracting data from image…"):
                # send image to api 
                data = extract_receipt_data(
                    st.session_state["image_bytes"],
                    st.session_state["image_mime"],
                )
                apply_ocr_data(data)
            st.success("Extraction complete!")
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

# ── Readonly Banner ──────────────────────────────────────────
if is_readonly:
    st.info("🔒 View-only mode — no changes can be saved.", icon="🔒")


# ── Re-extract helpers ───────────────────────────────────────
def reextract_field(field_name: str):
    raw = extract_single_field(
        st.session_state["image_bytes"],
        field_name,
        st.session_state["image_mime"],
    ).strip()

    if field_name == "receipt_num":
        st.session_state["receipt_num"] = "".join(c for c in raw if c.isdigit())

    elif field_name == "shop_name":
        st.session_state["shop_name"] = raw

    elif field_name == "date":
        try:
            st.session_state["date_val"] = datetime.strptime(raw, "%Y-%m-%d").date()
        except Exception:
            st.warning(f"Could not parse date: {raw!r}")

    elif field_name == "currency":
        cur = raw.upper()
        if cur in CURRENCIES:
            st.session_state["currency"] = cur
        else:
            st.warning(f"Unrecognised currency: {raw!r}")

    elif field_name == "tax_amount":
        try:
            st.session_state["tax_amount_input"] = float(raw)
            recalculate()
        except ValueError:
            st.warning(f"Could not parse tax amount: {raw!r}")


def reextract_btn(field_name: str, btn_key: str):
    if can_reextract:
        st.button(
            "🔄",
            key=btn_key,
            help=f"Re-extract {field_name} from image",
            on_click=reextract_field,   # ✅ runs BEFORE next render
            args=(field_name,),         # ✅ passes field_name as argument
        )

# ── Receipt Details ──────────────────────────────────────────
st.subheader("Receipt Details")

c1, c2 = st.columns([0.92, 0.08])
with c1:
    st.text_input("Receipt Number", key="receipt_num", disabled=is_readonly)
with c2:
    st.markdown("<div style='margin-top:1.75rem'>", unsafe_allow_html=True)
    reextract_btn("receipt_num", "re_receipt_num")
    st.markdown("</div>", unsafe_allow_html=True)

c1, c2 = st.columns([0.92, 0.08])
with c1:
    st.text_input("Shop Name", key="shop_name", disabled=is_readonly)
with c2:
    st.markdown("<div style='margin-top:1.75rem'>", unsafe_allow_html=True)
    reextract_btn("shop_name", "re_shop_name")
    st.markdown("</div>", unsafe_allow_html=True)

c1, c2 = st.columns([0.92, 0.08])
with c1:
    st.date_input("Date", key="date_val", disabled=is_readonly)
with c2:
    st.markdown("<div style='margin-top:1.75rem'>", unsafe_allow_html=True)
    reextract_btn("date", "re_date")
    st.markdown("</div>", unsafe_allow_html=True)

c1, c2 = st.columns([0.92, 0.08])
with c1:
    st.selectbox("Currency", CURRENCIES, key="currency", disabled=is_readonly)
with c2:
    st.markdown("<div style='margin-top:1.75rem'>", unsafe_allow_html=True)
    reextract_btn("currency", "re_currency")
    st.markdown("</div>", unsafe_allow_html=True)

# ── Items ────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Items")

if can_reextract:
    if st.button("🔄 Re-extract All Items", key="re_items"):
        with st.spinner("Re-extracting items…"):
            try:
                new_items = extract_items_field(
                    st.session_state["image_bytes"],
                    st.session_state["image_mime"],
                )
                st.session_state["items"] = [
                    make_item(
                        product_name=it.get("product_name", ""),
                        quantity=float(it.get("quantity") or 1),
                        price=float(it.get("price") or 0),
                    )
                    for it in new_items
                ]
                recalculate()
            except Exception as e:
                st.error(f"Failed to re-extract items: {e}")
        st.rerun()

# Column headers
h1, h2, h3, h4 = st.columns([0.50, 0.18, 0.18, 0.14])
h1.markdown("<small style='color:#6b7280;'>Product Name</small>", unsafe_allow_html=True)
h2.markdown("<small style='color:#6b7280;'>Quantity</small>", unsafe_allow_html=True)
h3.markdown("<small style='color:#6b7280;'>Price</small>", unsafe_allow_html=True)
if not is_readonly:
    h4.markdown("<small style='color:#6b7280;'>Remove</small>", unsafe_allow_html=True)

items = st.session_state["items"]
items_to_remove = []

for i, item in enumerate(items):
    # MIGRATION: items loaded from session state before the rewrite won't have _id
    if "_id" not in item:
        item["_id"] = next_item_id()
        st.session_state["items"][i] = item

    uid = item["_id"]

    c1, c2, c3, c4 = st.columns([0.50, 0.18, 0.18, 0.14])

    new_name  = c1.text_input(
        "Name", value=item["product_name"],
        key=f"name_{uid}", label_visibility="collapsed", disabled=is_readonly
    )
    new_qty   = c2.number_input(
        "Qty", value=float(item["quantity"]),
        min_value=0.0, step=1.0,
        key=f"qty_{uid}", label_visibility="collapsed", disabled=is_readonly
    )
    new_price = c3.number_input(
        "Price", value=float(item["price"]),
        min_value=0.0, step=0.001, format="%.3f",
        key=f"price_{uid}", label_visibility="collapsed", disabled=is_readonly
    )

    # Write widget values back into the list
    st.session_state["items"][i]["product_name"] = new_name
    st.session_state["items"][i]["quantity"]      = new_qty
    st.session_state["items"][i]["price"]         = new_price

    if not is_readonly:
        with c4:
            st.markdown("<div style='margin-top:0.4rem'>", unsafe_allow_html=True)
            # FIX: delete key uses uid so Streamlit never confuses which button was clicked
            if st.button("🗑️", key=f"del_{uid}", help="Remove item", disabled=len(items) <= 1):
                items_to_remove.append(i)
            st.markdown("</div>", unsafe_allow_html=True)

# Remove flagged items (by list index, which is safe here since we collected indices before mutating)
if items_to_remove:
    st.session_state["items"] = [item for j, item in enumerate(items) if j not in items_to_remove]
    st.rerun()

# Add Item button
if not is_readonly:
    if st.button("＋ Add Item"):
        # FIX: make_item() assigns a fresh stable _id via next_item_id()
        st.session_state["items"].append(make_item())
        st.rerun()

# ── Recalculate after every render ──────────────────────────
recalculate()

# ── Tax & Totals ─────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Totals")

c1, c2 = st.columns([0.92, 0.08])
with c1:
    st.number_input(
        "Tax Amount",
        key="tax_amount_input",
        min_value=0.0,
        step=0.001,
        format="%.3f",
        on_change=recalculate,
        disabled=is_readonly,
    )
    st.session_state["tax_amount"] = st.session_state["tax_amount_input"]
with c2:
    st.markdown("<div style='margin-top:1.75rem'>", unsafe_allow_html=True)
    reextract_btn("tax_amount", "re_tax")
    st.markdown("</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Subtotal",    f"{st.session_state['subtotal']:.3f} {st.session_state['currency']}")
col2.metric("Tax",         f"{st.session_state['tax_amount']:.3f} {st.session_state['currency']}")
col3.metric("Grand Total", f"{st.session_state['grand_total']:.3f} {st.session_state['currency']}")

# ── Save ─────────────────────────────────────────────────────
if not is_readonly:
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("💾 Save Receipt", type="primary", use_container_width=True):
        errors = save_receipt()
        if errors:
            for err in errors:
                st.error(err)
        else:
            st.success("Receipt saved successfully!")
            clear_form()
            st.switch_page("Home.py")
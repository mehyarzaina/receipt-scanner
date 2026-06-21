from database.models import Receipt, Item
from database.database import get_session
import streamlit as st
from datetime import datetime

# ── Constants ───────────────────────────────────────────────
CURRENCIES = ["JOD", "USD", "EUR", "GBP", "SAR", "AED", "EGP", "KWD", "QAR", "BHD", "OMR", "Other"]

# ── Helpers ─────────────────────────────────────────────────
def get_image_mime(filename: str) -> str:
    ext = filename.lower().split(".")[-1] # split after . and get last part
    return {
        "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "png": "image/png", "webp": "image/webp",
        "gif": "image/gif", "bmp": "image/bmp",
        "tiff": "image/tiff", "tif": "image/tiff",
        "heic": "image/heic",
    }.get(ext, "image/jpeg") # jpeg is used as a default

# st.session_state is a dictionary that stores values between reruns.

def next_item_id() -> int:
    """Return a unique, ever-increasing item ID stored in session state."""
    counter = st.session_state.get("_item_counter", 0)
    st.session_state["_item_counter"] = counter + 1
    return counter


def make_item(product_name="", quantity=1.0, price=0.0) -> dict:
    """Create a new item dict with a stable unique _id."""
    return {
        "_id": next_item_id(),
        "product_name": product_name,
        "quantity": float(quantity),
        "price": float(price),
    }


def init_form_state():
    """
    Every interaction (button click, typing, etc.) causes the script to run again from top to bottom. 
    Without st.session_state, all values would reset on every return
    - Creates all required variables in st.session_state.
    - Ensures existing user data is not overwritten during reruns.
    - Creates the first blank receipt item so the form is ready to use immediately.
    """
    defaults = {
        "_item_counter": 0,
        "receipt_num": "",
        "shop_name": "",
        "date_val": None,
        "currency": "Other",
        "items": [],           
        "tax_amount_input": 0.0,
        "tax_amount": 0.0,
        "subtotal": 0.0,
        "grand_total": 0.0,
        "lock_totals": False,
        "ocr_done": False,
        "image_bytes": None,
        "image_mime": None,
        "image_name": None,
        "mode": None,
        "view_mode": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # add with one blank item only on first run
    if not st.session_state["items"]:
        st.session_state["items"] = [make_item()]


def recalculate():
    """Recompute subtotal and grand total from current items + tax."""
    items = st.session_state.get("items", [])
    subtotal = round(sum(
        float(it.get("price") or 0)
        for it in items
    ), 3)
    tax = round(float(st.session_state.get("tax_amount_input") or 0), 3)
    st.session_state["subtotal"] = subtotal
    st.session_state["tax_amount"] = tax
    st.session_state["grand_total"] = round(subtotal + tax, 3)


def apply_ocr_data(data: dict):
    """
    - Takes the data extracted by Gemini.
    - Stores it in st.session_state.
    - Creates properly formatted item rows with unique IDs.
    - Recalculates totals and marks OCR as completed.
    """
    if data.get("receipt_num"):
        st.session_state["receipt_num"] = str(data["receipt_num"])
    if data.get("shop_name"):
        st.session_state["shop_name"] = data["shop_name"]
    if data.get("date"):
        try:
            st.session_state["date_val"] = datetime.strptime(data["date"], "%Y-%m-%d").date()
        except Exception:
            pass
    if data.get("currency"):
        cur = data["currency"].upper()
        if cur in CURRENCIES:
            st.session_state["currency"] = cur
    if data.get("items"):
        st.session_state["items"] = [
            make_item(
                product_name=it.get("product_name", ""),
                quantity=float(it.get("quantity") or 1),
                price=float(it.get("price") or 0),
            )
            for it in data["items"]
        ]
    if data.get("tax_amount") is not None:
        st.session_state["tax_amount_input"] = float(data["tax_amount"] or 0)

    recalculate()
    st.session_state["ocr_done"] = True


def validate_form():
    """
    Before saving the receipt to the database, check that all required fields contain valid data.
    """
    errors = []
    if not st.session_state["receipt_num"].strip():
        errors.append("Receipt number is required.")
    elif not st.session_state["receipt_num"].strip().isdigit():
        errors.append("Receipt number must contain digits only.")
    if not st.session_state["shop_name"].strip():
        errors.append("Shop name is required.")
    if not st.session_state["date_val"]:
        errors.append("Date is required.")
    if not st.session_state["currency"]:
        errors.append("Currency is required.")
    items = st.session_state.get("items", [])
    if not items:
        errors.append("At least one item is required.")
    for i, it in enumerate(items, 1):
        if not it.get("product_name", "").strip():
            errors.append(f"Item {i}: product name required.")
        if float(it.get("quantity") or 0) <= 0:
            errors.append(f"Item {i}: quantity must be > 0.")
        if float(it.get("price") or 0) < 0:
            errors.append(f"Item {i}: price cannot be negative.")
    return errors


def save_receipt():
    errors = validate_form()
    if errors:
        return errors
    session = get_session()
    try:
        receipt_id = int(st.session_state["receipt_num"].strip())

        receipt = Receipt(
            receipt_num=receipt_id,
            shop_name=st.session_state["shop_name"].strip(),
            date=str(st.session_state["date_val"]),
            currency=st.session_state["currency"],
            subtotal=st.session_state["subtotal"],
            tax_amount=st.session_state["tax_amount"],
            grand_total=st.session_state["grand_total"],
            receipt_filename=st.session_state.get("image_name"),
        )
        session.add(receipt)
        session.flush()

        for it in st.session_state["items"]:
            session.add(Item(
                receipt_id=receipt.id,
                product_name=it.get("product_name", "").strip(),
                quantity=float(it.get("quantity") or 0),
                price=float(it.get("price") or 0),
            ))

        session.commit()
        return []
    except Exception as e:
        session.rollback()
        return [f"Database error: {e}"]
    finally:
        session.close()


def clear_form():
    keys = [
        "_item_counter",
        "receipt_num", "shop_name", "date_val", "currency", "items",
        "tax_amount_input", "tax_amount", "subtotal", "grand_total",
        "lock_totals", "ocr_done", "image_bytes", "image_mime",
        "image_name", "mode", "view_mode",
    ]
    for k in keys:
        if k in st.session_state:
            del st.session_state[k]

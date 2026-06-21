import os
import json
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "models/gemini-flash-lite-latest"

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def extract_receipt_data(image_bytes: bytes, image_mime: str = "image/jpeg") -> dict:
    """Extract all receipt fields from an image using Gemini Vision."""

    prompt = """
You are an expert OCR system for receipts. Analyze this receipt image and extract ALL information.

Return a JSON object with EXACTLY this structure (no markdown, no code blocks, just raw JSON):
{
  "receipt_num": <integer or null>,
  "shop_name": <string or null>,
  "date": <string in YYYY-MM-DD format or null>,
  "currency": <3-letter currency code like USD, JOD, EUR, or null>,
  "items": [
    {
      "product_name": <string>,
      "quantity": <number>,
      "price": <number>
    }
  ],
  "subtotal": <number or null>,
  "taxes": [
    {
      "tax_name": <string>,
      "tax_percentage": <number or null>,
      "tax_amount": <number or null>
    }
  ],
  "tax_amount": <sum of ALL tax amounts combined as a single number or null>,
  "grand_total": <number or null>
}

Rules:
- receipt_num must be a pure integer (digits only)
- All prices/amounts must be plain numbers (no currency symbols)
- Extract EVERY tax line separately into the taxes array (e.g. service charge, VAT, GST)
- tax_amount at the top level must be the SUM of all taxes combined
- If tax_percentage is not shown but subtotal and tax_amount are available, calculate it
- If a field is not visible or unreadable, use null
- Extract every line item from the receipt
- Return ONLY valid JSON, nothing else
- Extract all list of items make sure to include them all and the first one "Important"
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part(text=prompt),
                    types.Part(
                        inline_data=types.Blob(
                            data=image_bytes,
                            mime_type=image_mime
                        )
                    )
                ]
            )
        ],
    )

    raw = response.text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    return json.loads(raw)


def extract_single_field(image_bytes: bytes, field_name: str, image_mime: str = "image/jpeg") -> str:
    """Re-extract a single field from the receipt image."""

    field_prompts = {
        "receipt_num": "Extract ONLY the receipt/invoice number from this receipt. Return just the number as a plain integer, nothing else.",
        "shop_name": "Extract ONLY the store/shop/business name from this receipt. Return just the name as a plain string, nothing else.",
        "date": "Extract ONLY the date from this receipt. Return it in YYYY-MM-DD format, nothing else.",
        "currency": "Extract ONLY the currency used in this receipt. Return the 3-letter ISO code (e.g. USD, JOD, EUR), nothing else.",
        "subtotal": "Extract ONLY the subtotal amount (before tax) from this receipt. Return just the number, no currency symbol, nothing else.",
        "tax_amount": "Extract ONLY the tax amount from this receipt. Return just the number, no currency symbol, nothing else.",
        "tax_percentage": "Extract ONLY the tax percentage rate from this receipt. Return just the number (e.g. 16 for 16%), nothing else.",
        "grand_total": "Extract ONLY the grand total / final amount due from this receipt. Return just the number, no currency symbol, nothing else.",
        "items": (
            "Extract ONLY the line items from this receipt. "
            "Return a JSON array and nothing else — no markdown, no code fences, no explanation. "
            'Example format: [{"product_name": "Milk", "quantity": 2, "price": 1.50}, ...]. '
            "Each object must have product_name (string), quantity (number), and price (number per unit). "
            "If quantity is not shown, default to 1."
        ),
    }

    prompt = field_prompts.get(
        field_name,
        f"Extract ONLY the {field_name} from this receipt. Return just the value, nothing else."
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part(text=prompt),
                    types.Part(
                        inline_data=types.Blob(
                            data=image_bytes,
                            mime_type=image_mime
                        )
                    )
                ]
            )
        ],
    )

    return response.text.strip()


def extract_items_field(image_bytes: bytes, image_mime: str = "image/jpeg") -> list:
    """Re-extract items list from the receipt image."""

    prompt = """
Extract ONLY the line items from this receipt.
Return a JSON array with no markdown or code blocks:
[{"product_name": "...", "quantity": <number>, "price": <number>}, ...]
Return ONLY valid JSON array, nothing else.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            types.Content(
                role="user", # the code sending the request
                parts=[
                    types.Part(text=prompt),
                    types.Part(
                        inline_data=types.Blob( # Binary Large Object for 
                            data=image_bytes,
                            mime_type=image_mime
                        )
                    )
                ]
            )
        ],
    )

    raw = response.text.strip() # removes whitespaces 
    raw = re.sub(r"^```(?:json)?\s*", "", raw) # ```json → stripped ``` → stripped ^ means "start of string", \s* removes any whitespace after the '''
    raw = re.sub(r"\s*```$", "", raw) # $ means "end of string", \s* removes any whitespace before the '''

    return json.loads(raw)
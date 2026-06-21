# 🧾 Receipt Manager

Receipt Manager is a Streamlit-based application for digitizing, managing, and searching receipts. The system combines OCR powered by Google Gemini with a PostgreSQL database to provide a streamlined receipt management experience.

## Features

* Upload receipt images and automatically extract data using Gemini Vision OCR
* Manual receipt entry for cases where OCR is unavailable
* Re-extract individual fields with one click when OCR results need correction
* Store receipts and item details in PostgreSQL
* Search and filter previously saved receipts
* View receipt history in a structured table format
* Read-only receipt view for reviewing stored records

---

## Technology Stack

* **Frontend:** Streamlit
* **Database:** PostgreSQL
* **OCR & AI:** Google Gemini Flash Lite
* **Backend:** Python
* **Data Validation:** Custom validation for receipt fields and item entries

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd receipt-manager
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=receipt_db
GEMINI_API_KEY=your_api_key
```

| Variable       | Description                     |
| -------------- | ------------------------------- |
| DB_USER        | PostgreSQL username             |
| DB_PASSWORD    | PostgreSQL password             |
| DB_HOST        | Database host                   |
| DB_PORT        | PostgreSQL port (default: 5432) |
| DB_NAME        | Database name                   |
| GEMINI_API_KEY | Google Gemini API key           |

### 4. Run the Application

```bash
streamlit run Home.py
```

---

## Application Pages

### 🏠 Home

Landing page providing quick access to the application's main features.

### 📄 Upload Receipt

Users can add receipts using one of two methods:

#### Manual Mode

* Enter receipt information manually.
* Add receipt items directly.

#### Automatic Mode

* Upload a receipt image.
* Click **Analyze** to extract receipt information using Gemini Vision OCR.

Additional features:

* Individual **↻ Re-extract** buttons for each field.
* Receipt number validation (digits only).
* Validation for required fields.
* Quantity and price validation for receipt items.
* Automatic storage in PostgreSQL upon submission.

### 🗂️ History

Browse previously saved receipts.

Features include:

* Search by shop name.
* Filter by receipt number.
* Filter by date range.
* Open any receipt in a read-only view.

---

## Supported Image Formats

* PNG
* JPG / JPEG
* WebP
* GIF
* BMP
* TIFF
* HEIC

---

## AI Model

The application uses:

* **models/gemini-flash-lite-latest** for OCR-based receipt information extraction.

---

## Future Enhancements

* Receipt category classification
* Expense analytics dashboard
* Multi-user authentication
* Export to Excel and PDF
* Currency conversion support
* Duplicate receipt detectio

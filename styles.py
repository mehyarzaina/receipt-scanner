"""
Features:
- Imports and applies fonts.
- Sets the application's dark theme colors, typography, and spacing.
- Hides Streamlit's default menu, header, and footer.
- Styles reusable card components with shadows and hover effects.
- Defines application color variables (accent, success, warning, danger).
- Customizes form inputs, labels, buttons, file uploaders, and tables.
- Styles alerts, metrics, badges, section headers, and totals bars.
- Adds custom scrollbar styling.
- Provides reusable classes for readonly fields and other UI elements.

To apply these styles on a page:

    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

This file acts as the central design system for the application,
ensuring a consistent look.
"""


GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    font-family: 'Sora', sans-serif;
    background: #0f1117;
    color: #e8eaf0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2rem 4rem !important; max-width: 1100px !important; }

/* ── Typography ── */
h1 { font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; }
h2 { font-size: 1.4rem; font-weight: 600; }
h3 { font-size: 1.1rem; font-weight: 500; }

/* ── Card / Box ── */
.card {
    background: #1a1d27;
    border: 1px solid #2a2d3a;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 1px 0 rgba(255,255,255,0.05) inset;
    transition: box-shadow 0.2s;
}
.card:hover { box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 1px 0 rgba(255,255,255,0.07) inset; }

/* ── Accent colors ── */
:root {
    --accent: #6c63ff;
    --accent-light: #8b85ff;
    --accent-dim: rgba(108,99,255,0.15);
    --success: #34d399;
    --warn: #fbbf24;
    --danger: #f87171;
    --border: #2a2d3a;
    --surface: #1a1d27;
    --surface2: #22253a;
    --text: #e8eaf0;
    --muted: #6b7280;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div,
.stDateInput > div > div > input {
    background: #22253a !important;
    border: 1px solid #2a2d3a !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.5rem 0.75rem !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.2) !important;
}

/* ── Labels ── */
.stTextInput label, .stNumberInput label, .stSelectbox label,
.stDateInput label, .stFileUploader label {
    color: #9ca3af !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #6c63ff !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background: #8b85ff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(108,99,255,0.4) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Secondary button style via key suffix trick */
[data-testid="baseButton-secondary"] > button,
button[kind="secondary"] {
    background: #22253a !important;
    border: 1px solid #2a2d3a !important;
    color: #9ca3af !important;
}
[data-testid="baseButton-secondary"] > button:hover,
button[kind="secondary"]:hover {
    background: #2a2d3a !important;
    color: #e8eaf0 !important;
    box-shadow: none !important;
}

/* ── File uploader ── */
.stFileUploader > div {
    background: #22253a !important;
    border: 2px dashed #2a2d3a !important;
    border-radius: 12px !important;
    transition: border-color 0.2s !important;
}
.stFileUploader > div:hover { border-color: #6c63ff !important; }

/* ── Dataframe / Table ── */
.stDataFrame { border-radius: 12px; overflow: hidden; }
.stDataFrame table { background: #1a1d27 !important; }
.stDataFrame th {
    background: #22253a !important;
    color: #9ca3af !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    border-bottom: 1px solid #2a2d3a !important;
}
.stDataFrame td { color: #e8eaf0 !important; border-bottom: 1px solid #1e2130 !important; }

/* ── Divider ── */
hr { border: none; border-top: 1px solid #2a2d3a; margin: 1.5rem 0; }

/* ── Badge ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.badge-primary { background: rgba(108,99,255,0.2); color: #8b85ff; }
.badge-success { background: rgba(52,211,153,0.15); color: #34d399; }
.badge-warn    { background: rgba(251,191,36,0.15);  color: #fbbf24; }

/* ── Reload icon buttons ── */
.reload-btn > button {
    background: #22253a !important;
    border: 1px solid #2a2d3a !important;
    border-radius: 8px !important;
    color: #6c63ff !important;
    padding: 0.3rem 0.5rem !important;
    font-size: 0.8rem !important;
    min-height: 0 !important;
    height: 2.2rem !important;
    width: 2.2rem !important;
}
.reload-btn > button:hover {
    background: rgba(108,99,255,0.2) !important;
    border-color: #6c63ff !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Section header ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #2a2d3a;
}
.section-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #6c63ff;
    flex-shrink: 0;
}

/* ── Totals bar ── */
.totals-bar {
    background: linear-gradient(135deg, #22253a 0%, #1e2035 100%);
    border: 1px solid #2a2d3a;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
}

/* ── Alerts ── */
.stAlert { border-radius: 10px !important; }

/* ── Success / Error messages ── */
.stSuccess { background: rgba(52,211,153,0.1) !important; border-color: #34d399 !important; }
.stError   { background: rgba(248,113,113,0.1) !important; border-color: #f87171 !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #6c63ff !important; }

/* ── Metric ── */
[data-testid="metric-container"] {
    background: #22253a !important;
    border: 1px solid #2a2d3a !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
[data-testid="metric-container"] label { color: #9ca3af !important; font-size: 0.75rem !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #e8eaf0 !important; font-size: 1.6rem !important; font-weight: 700 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0f1117; }
::-webkit-scrollbar-thumb { background: #2a2d3a; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #6c63ff; }

/* ── Readonly mode ── */
.readonly-field {
    background: #22253a;
    border: 1px solid #2a2d3a;
    border-radius: 10px;
    padding: 0.6rem 0.9rem;
    color: #e8eaf0;
    font-family: 'Sora', sans-serif;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}
.readonly-label {
    color: #6b7280;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.3rem;
}
</style>
"""
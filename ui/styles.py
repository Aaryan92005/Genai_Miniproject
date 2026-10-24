import streamlit as st

def inject_custom_css():
    """Injects high-contrast, startup-grade modern glassmorphic dark theme CSS into Streamlit."""
    st.markdown("""
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Typography & System Colors */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.01em;
        color: #f8fafc !important;
    }

    p, span, div, caption {
        color: #cbd5e1;
    }

    /* App Canvas Background */
    .stApp {
        background: radial-gradient(circle at 12% 15%, rgba(99, 102, 241, 0.15) 0%, transparent 45%),
                    radial-gradient(circle at 88% 85%, rgba(168, 85, 247, 0.12) 0%, transparent 45%),
                    #0b0f19 !important;
        color: #f8fafc !important;
    }

    /* Style Streamlit Header Bar to be transparent while keeping collapsed sidebar toggle visible */
    header[data-testid="stHeader"] {
        background: transparent !important;
        z-index: 9999 !important;
    }
    
    /* Always show the Sidebar Toggle (Open/Close) button */
    div[data-testid="stSidebarCollapsedControl"],
    button[kind="header"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        background: rgba(30, 41, 59, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
    }

    button[kind="header"] svg {
        fill: #f8fafc !important;
        color: #f8fafc !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1220px !important;
    }

    /* Input Widget Labels - HIGH CONTRAST FIX */
    label, 
    .stWidgetLabel, 
    div[data-testid="stWidgetLabel"] p, 
    div[data-testid="stWidgetLabel"] label, 
    label p, 
    .stMarkdown p {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        opacity: 1 !important;
    }

    /* Text Inputs, Text Areas, Selectboxes - HIGH CONTRAST FIX */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    input[type="text"],
    input[type="password"] {
        background: #1e293b !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-size: 0.98rem !important;
        font-weight: 500 !important;
        padding: 10px 14px !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder,
    input::placeholder {
        color: #94a3b8 !important;
        opacity: 0.9 !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.35) !important;
    }

    /* Selectbox Dropdown Menu Popover - HIGH CONTRAST FIX */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    ul[data-testid="stSelectboxVirtualDropdown"] {
        background-color: #1e293b !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6) !important;
    }

    li[role="option"],
    div[data-baseweb="option"] {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    li[role="option"] p,
    li[role="option"] span,
    div[data-baseweb="option"] p,
    div[data-baseweb="option"] span {
        color: #f8fafc !important;
    }

    li[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    div[data-baseweb="option"]:hover {
        background-color: #4f46e5 !important;
        color: #ffffff !important;
    }

    /* Standard Buttons & Form Submit Buttons - HIGH CONTRAST FIX */
    .stButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        letter-spacing: 0.01em !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.4rem !important;
        transition: all 0.22s ease-in-out !important;
        box-shadow: 0 4px 16px rgba(79, 70, 229, 0.4) !important;
    }

    .stButton > button p,
    .stButton > button span,
    .stFormSubmitButton > button p,
    .stFormSubmitButton > button span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.55) !important;
        background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }

    /* Sidebar Base Styling */
    section[data-testid="stSidebar"] {
        background: #0d1322 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4);
    }

    /* Hide Radio Input Circles in Sidebar Navigation */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }

    /* Style Sidebar Radio Labels as Sleek Navigation Buttons */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
        display: flex !important;
        align-items: center !important;
        padding: 10px 14px !important;
        margin-bottom: 5px !important;
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        cursor: pointer !important;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
        background: rgba(99, 102, 241, 0.15) !important;
        border-color: rgba(99, 102, 241, 0.35) !important;
        color: #ffffff !important;
        transform: translateX(4px) !important;
    }

    /* Selected Radio Navigation Button */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[aria-checked="true"],
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%) !important;
        border: 1px solid rgba(168, 85, 247, 0.5) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3) !important;
        position: relative;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[aria-checked="true"]::before,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked)::before {
        content: "";
        position: absolute;
        left: 0;
        top: 20%;
        bottom: 20%;
        width: 4px;
        background: linear-gradient(to bottom, #818cf8, #c084fc);
        border-radius: 0 4px 4px 0;
    }

    /* Premium Glassmorphic Cards */
    .sm-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 22px;
        box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.4);
    }

    /* Gradient Featured Card */
    .sm-card-gradient {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 50%, rgba(236, 72, 153, 0.18) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(168, 85, 247, 0.4);
        border-top: 1px solid rgba(192, 132, 252, 0.55);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 22px;
    }

    /* Metric Values & Labels */
    .sm-metric-val {
        font-family: 'Outfit', sans-serif;
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #a5b4fc 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sm-metric-label {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #cbd5e1;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
    }

    /* Icon Container Box */
    .sm-icon-box {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%);
        border: 1px solid rgba(168, 85, 247, 0.35);
    }

    /* Source Chips */
    .sm-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.18);
        color: #c7d2fe;
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 10px;
        padding: 5px 12px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 4px 6px 4px 0;
    }

    /* Tabs Styling - HIGH CONTRAST FIX */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.8);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        color: #cbd5e1 !important;
        font-weight: 600;
        font-size: 0.95rem;
    }

    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span {
        color: #cbd5e1 !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4);
    }

    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0b0f19;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.4);
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

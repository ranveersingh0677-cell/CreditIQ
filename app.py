import os
from dotenv import load_dotenv

load_dotenv()

import textwrap
from datetime import datetime

import streamlit as st
from groq import Groq


# =========================
# Configuration
# =========================

MODEL_NAME = "llama-3.3-70b-versatile"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# =========================
# Helper functions
# =========================

def build_cam_prompt(
    company_name: str,
    turnover: str,
    loan_amount: str,
    loan_type: str,
    gst_status: str,
    legal_cases: str,
    promoter_background: str,
    collateral: str,
    additional_details: str,
    officer_notes: str,
) -> str:
    """Create a detailed prompt for the Gemini model focused on Indian banking CAM."""

    base_prompt = f"""
    You are a senior credit officer in an Indian bank, writing a professional Credit Appraisal Memo (CAM)
    for internal credit committee use. Use RBI, CIBIL, and standard Indian banking practices.

    Borrower Details:
    - Company Name: {company_name}
    - Annual Turnover: {turnover}
    - Loan Amount Requested: {loan_amount}
    - Loan Type: {loan_type}
    - GST Status: {gst_status}
    - Legal Cases / Litigations: {legal_cases}
    - Promoter Background: {promoter_background}
    - Collateral Offered: {collateral}
    - Additional Financial Details: {additional_details}
    - Credit Officer Notes: {officer_notes}

    TASK:
    Prepare a detailed Credit Appraisal Memo using the **Five C's of Credit** in the Indian banking context:
    1. Character
    2. Capacity (including DSCR and repayment ability)
    3. Capital
    4. Collateral
    5. Conditions

    STRICT DECISION RULES - Follow these exactly:
    - If promoter background is "Adverse market feedback / concerns" → MUST REJECT
    - If legal cases include "Major litigations / NCLT / SARFAESI" → MUST REJECT
    - If GST status is "Active – Frequent Delays" AND legal cases are adverse → MUST REJECT
    - If TWO OR MORE serious risk factors exist simultaneously → MUST REJECT
    - Only APPROVE when character, capacity, capital and collateral are all satisfactory
    - These rules are mandatory and override all other considerations.

    REQUIREMENTS:
    - The memo must be structured with clear headings:
      1. Executive Summary
      2. Business Overview
      3. Banking & Credit History (CIBIL / bureau behavior)
      4. Financial Analysis (profitability, leverage, DSCR, cash flows)
      5. Five C's of Credit Assessment
      6. Risk Assessment & Mitigants
      7. Recommendation & Final Decision
    - Explicitly refer to:
      - CIBIL score / bureau conduct (you may reasonably assume a range based on inputs)
      - GST compliance behavior
      - Key RBI guidelines in generic terms (do NOT fabricate specific circular numbers)
      - DSCR assessment qualitatively (explain assumptions if exact numbers are not available)
    - Be concise but professional, like an internal bank CAM note.

    DECISION FORMAT (VERY IMPORTANT):
    - At the very end of the memo, include a separate section:
      "FINAL DECISION: APPROVE"  OR  "FINAL DECISION: REJECT"
    - Use exactly one of these two words in ALL CAPS after "FINAL DECISION:" so that it can be parsed by software.

    Now draft the complete Credit Appraisal Memo based on the above.
    """

    return textwrap.dedent(base_prompt).strip()


def get_groq_cam(prompt: str) -> str:
    """Call Groq API to generate the CAM text."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return (chat_completion.choices[0].message.content or "").strip()
    except Exception as e:
        return f"Unable to generate CAM due to an error from Groq: {e}"


def extract_decision(cam_text: str) -> str:
    """Parse the final decision from the CAM text."""
    marker = "FINAL DECISION:"
    for line in cam_text.splitlines()[::-1]:
        if marker in line.upper():
            decision_part = line.split(":", 1)[1].strip().upper()
            if "APPROVE" in decision_part:
                return "APPROVE"
            if "REJECT" in decision_part:
                return "REJECT"

    # Fallback: keyword-based heuristic
    upper_text = cam_text.upper()
    if "FINAL DECISION" in upper_text and "APPROVE" in upper_text and "REJECT" not in upper_text:
        return "APPROVE"
    if "FINAL DECISION" in upper_text and "REJECT" in upper_text and "APPROVE" not in upper_text:
        return "REJECT"

    # Default to REJECT if unclear, to be conservative
    return "REJECT"


def build_download_filename(company_name: str) -> str:
    safe_name = company_name.strip() or "borrower"
    safe_name = "".join(ch for ch in safe_name if ch.isalnum() or ch in (" ", "_", "-")).strip()
    safe_name = safe_name.replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"CAM_{safe_name}_{timestamp}.txt"


def inject_custom_css(dark_mode: bool) -> None:
    """Apply custom theme with dark/light modes and premium fintech styling."""

    if dark_mode:
        bg_app = "#0A1628"
        bg_hero = "linear-gradient(135deg, #020617 0%, #0B1220 35%, #111827 70%, #1F2937 100%)"
        bg_card = "rgba(15, 23, 42, 0.95)"
        text_primary = "#F9FAFB"
        text_muted = "#9CA3AF"
        accent = "#F59E0B"
        accent_soft = "rgba(245, 158, 11, 0.14)"
        border_color = "rgba(148, 163, 184, 0.4)"
        badge_bg = "rgba(15, 23, 42, 0.80)"
        badge_text = "#F9FAFB"
        chip_bg = "rgba(15, 23, 42, 0.60)"
        chip_text = "#F9FAFB"
        input_bg = "#112240"
        input_border = "#F59E0B"
        input_text = "#F9FAFB"
        toggle_bg = "#F59E0B"
        toggle_text = "#111827"
        toggle_border = "rgba(148, 163, 184, 0.8)"
    else:
        bg_app = "#F9FAFB"
        bg_hero = "linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 30%, #FEF3C7 100%)"
        bg_card = "#FFFFFF"
        text_primary = "#0A1628"
        text_muted = "#4B5563"
        accent = "#F59E0B"
        accent_soft = "rgba(245, 158, 11, 0.08)"
        border_color = "rgba(148, 163, 184, 0.3)"
        badge_bg = "#F1F5F9"
        badge_text = "#0A1628"
        chip_bg = "#F1F5F9"
        chip_text = "#0A1628"
        input_bg = "#FFFFFF"
        input_border = "#1D4ED8"
        input_text = "#0A1628"
        toggle_bg = "#0A1628"
        toggle_text = "#F9FAFB"
        toggle_border = "rgba(15, 23, 42, 0.9)"

    css_base = f"""
        <style>
            :root {{
                --creditiq-bg-app: {bg_app};
                --creditiq-bg-hero: {bg_hero};
                --creditiq-bg-card: {bg_card};
                --creditiq-text-primary: {text_primary};
                --creditiq-text-muted: {text_muted};
                --creditiq-accent: {accent};
                --creditiq-accent-soft: {accent_soft};
                --creditiq-border-subtle: {border_color};
                --creditiq-badge-bg: {badge_bg};
                --creditiq-badge-text: {badge_text};
                --creditiq-chip-bg: {chip_bg};
                --creditiq-chip-text: {chip_text};
                --creditiq-input-bg: {input_bg};
                --creditiq-input-border: {input_border};
                --creditiq-input-text: {input_text};
                --creditiq-toggle-bg: {toggle_bg};
                --creditiq-toggle-text: {toggle_text};
                --creditiq-toggle-border: {toggle_border};
            }}

            [data-testid="stAppViewContainer"] {{
                background: var(--creditiq-bg-app);
                color: var(--creditiq-text-primary);
            }}

            /* Hero header */
            .creditiq-hero {{
                margin-top: -1.5rem;
                margin-bottom: 1.5rem;
                padding: 1.75rem 1.75rem 1.5rem 1.75rem;
                border-radius: 1.5rem;
                background: var(--creditiq-bg-hero);
                border: 1px solid rgba(15, 23, 42, 0.65);
                position: relative;
                overflow: hidden;
            }}

            .creditiq-hero::after {{
                content: "";
                position: absolute;
                inset: 0;
                background: radial-gradient(circle at top right, rgba(245, 158, 11, 0.18), transparent 45%);
                mix-blend-mode: screen;
                pointer-events: none;
            }}

            .creditiq-logo-pill {{
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.25rem 0.9rem;
                border-radius: 999px;
                background: var(--creditiq-badge-bg);
                border: 1px solid rgba(148, 163, 184, 0.5);
                font-size: 0.8rem;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: var(--creditiq-badge-text);
            }}

            .creditiq-logo-mark {{
                width: 1.6rem;
                height: 1.6rem;
                border-radius: 0.75rem;
                background: radial-gradient(circle at 30% 0%, #FBBF24, #F97316);
                display: inline-flex;
                align-items: center;
                justify-content: center;
                color: #020617;
                font-weight: 800;
                font-size: 0.9rem;
                box-shadow: 0 12px 35px rgba(245, 158, 11, 0.5);
            }}

            .creditiq-title {{
                font-weight: 750;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                font-size: 0.95rem;
                color: var(--creditiq-text-muted);
            }}

            .creditiq-hero-heading {{
                font-size: 2rem;
                font-weight: 700;
                letter-spacing: 0.04em;
                color: var(--creditiq-text-primary) !important;
            }}

            .creditiq-hero-heading span.accent {{
                background: linear-gradient(90deg, #FACC15, #F59E0B, #F97316);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}

            .creditiq-hero-subtitle {{
                margin-top: 0.35rem;
                font-size: 0.95rem;
                color: var(--creditiq-text-muted);
                max-width: 32rem;
            }}

            .creditiq-hero-meta {{
                display: flex;
                gap: 0.75rem;
                flex-wrap: wrap;
                margin-top: 0.9rem;
            }}

            .creditiq-chip {{
                padding: 0.25rem 0.75rem;
                border-radius: 999px;
                font-size: 0.8rem;
                border: 1px solid rgba(148, 163, 184, 0.55);
                color: var(--creditiq-chip-text);
                background: var(--creditiq-chip-bg);
            }}

            .theme-toggle-label {{
                font-size: 0.8rem;
                color: var(--creditiq-text-muted);
            }}

            /* Cards */
            .section-card {{
                background: var(--creditiq-bg-card);
                border-radius: 1rem;
                padding: 1.1rem 1.1rem 1.0rem 1.1rem;
                border: 1px solid var(--creditiq-border-subtle);
                box-shadow: 0 18px 45px rgba(15, 23, 42, 0.22);
                margin-bottom: 1rem;
            }}

            .section-card-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.75rem;
            }}

            .section-title {{
                font-size: 0.95rem;
                font-weight: 600;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: var(--creditiq-text-primary);
            }}

            .section-kicker {{
                font-size: 0.8rem;
                color: var(--creditiq-text-primary);
            }}

            /* Inputs */
            .stTextInput>div>div>input,
            .stSelectbox>div>div>div {{
                border-radius: 0.5rem !important;
                border: 1px solid var(--creditiq-input-border) !important;
                background-color: var(--creditiq-input-bg) !important;
                color: var(--creditiq-input-text) !important;
                box-shadow: none !important;
            }}

            /* Fix for BOTH themes - make text areas clean */
            [data-testid="stTextArea"] textarea {{
                background-color: transparent !important;
                border-radius: 4px !important;
                box-shadow: none !important;
            }}

            .stTextArea>div>textarea {{
                background-color: transparent !important;
                border-radius: 4px !important;
                box-shadow: none !important;
                border: 1px solid var(--creditiq-input-border) !important;
                color: var(--creditiq-input-text) !important;
            }}

            .stTextInput>div>div>input:focus,
            .stTextArea>div>textarea:focus,
            .stSelectbox>div>div>div:focus {{
                border-color: var(--creditiq-input-border) !important;
                box-shadow: 0 0 0 1px {accent_soft};
            }}

            .stTextInput label, .stTextArea label, .stSelectbox label {{
                font-size: 0.86rem;
                font-weight: 500;
                margin-bottom: 0.25rem;
                color: var(--creditiq-text-primary);
            }}

            .stTextInput input::placeholder,
            .stTextArea textarea::placeholder {{
                color: var(--creditiq-text-muted);
                opacity: 0.9;
            }}

            /* Ensure select text & arrow are visible in both themes */
            .stSelectbox span {{
                color: var(--creditiq-input-text) !important;
            }}

            .stSelectbox svg {{
                fill: var(--creditiq-input-text) !important;
            }}

            /* Theme toggle switch */
            [data-testid="stWidget"]:has([data-testid="stSwitch"]) {{
                display: flex;
                justify-content: flex-end;
            }}

            [data-testid="stSwitch"] > label {{
                background: var(--creditiq-toggle-bg);
                color: var(--creditiq-toggle-text);
                border-radius: 999px;
                padding: 0.2rem 0.9rem;
                border: 1.5px solid var(--creditiq-toggle-border);
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                font-size: 0.8rem;
                font-weight: 500;
                box-shadow: 0 0 0 1px rgba(15, 23, 42, 0.25);
            }}

            [data-testid="stSwitch"] svg {{
                fill: var(--creditiq-toggle-text);
            }}

            /* Primary button */
            .stButton>button {{
                background: linear-gradient(90deg, #FACC15, #F59E0B, #F97316) !important;
                color: #020617 !important;
                border-radius: 9999px !important;
                font-weight: 600 !important;
                border: none !important;
                padding: 0.45rem 1.6rem !important;
                box-shadow: 0 14px 30px rgba(245, 158, 11, 0.45) !important;
            }}

            .stButton>button:hover {{
                filter: brightness(1.05);
                transform: translateY(-1px);
            }}

            /* Decision banners */
            .decision-banner {{
                border-radius: 0.9rem;
                padding: 0.9rem 1.15rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.09em;
                font-size: 0.86rem;
                display: flex;
                align-items: center;
                gap: 0.55rem;
                margin-bottom: 0.35rem;
            }}

           .decision-approve {{
    background: linear-gradient(90deg, rgba(22, 163, 74, 0.18), rgba(16, 185, 129, 0.18));
    border: 1px solid rgba(34, 197, 94, 0.8);
    color: {"#DCFCE7" if dark_mode else "#0A1628"};
}}

.decision-reject {{
    background: linear-gradient(90deg, rgba(220, 38, 38, 0.2), rgba(248, 113, 113, 0.16));
    border: 1px solid rgba(248, 113, 113, 0.9);
    color: {"#FEE2E2" if dark_mode else "#0A1628"};
}}

            /* CAM output */
            .cam-box {{
                background: var(--creditiq-bg-card);
                border-radius: 1rem;
                border: 1px solid var(--creditiq-border-subtle);
                padding: 1.1rem 1.25rem;
                backdrop-filter: blur(16px);
                max-height: 460px;
                overflow-y: auto;
                font-size: 0.9rem;
                line-height: 1.55;
            }}

            .cam-box h1, .cam-box h2, .cam-box h3 {{
                margin-top: 0.75rem;
                margin-bottom: 0.2rem;
            }}

            .cam-box p {{
                margin-bottom: 0.35rem;
            }}

            /* Sidebar cards */
.sidebar-card {{
    background: {"rgba(15, 23, 42, 0.9)" if dark_mode else "#F1F5F9"};
    border-radius: 0.9rem;
    padding: 0.9rem 0.85rem;
    border: 1px solid {"rgba(55, 65, 81, 0.9)" if dark_mode else "rgba(148, 163, 184, 0.4)"};
    margin-bottom: 0.55rem;
}}

.sidebar-card-title {{
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: {"#E5E7EB" if dark_mode else "#0A1628"};
                margin-bottom: 0.2rem;
                display: flex;
                align-items: center;
                gap: 0.45rem;
            }}

            .sidebar-badge {{
                width: 1.4rem;
                height: 1.4rem;
                border-radius: 999px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 0.85rem;
                font-weight: 600;
                box-shadow: 0 6px 18px rgba(15, 23, 42, 0.8);
            }}

            .sidebar-badge-gold {{
                background: radial-gradient(circle at 30% 0%, #FACC15, #F59E0B);
                color: #1F2933;
            }}

            .sidebar-badge-blue {{
                background: radial-gradient(circle at 30% 0%, #3B82F6, #1D4ED8);
                color: #EFF6FF;
            }}

            .sidebar-badge-orange {{
                background: radial-gradient(circle at 30% 0%, #FB923C, #EA580C);
                color: #FFF7ED;
            }}

            .sidebar-card-body {{
                font-size: 0.82rem;
                line-height: 1.55;
                color: #9CA3AF;
            }}

            .sidebar-divider {{
                height: 1px;
                margin: 0.4rem 0 0.65rem 0;
                background: linear-gradient(90deg, transparent, rgba(75, 85, 99, 0.7), transparent);
            }}

 /* Sidebar close arrow (<<) color */
[data-testid="stSidebarCollapseButton"] button svg {{
    fill: {"#FFFFFF" if dark_mode else "#0A1628"} !important;
}}
[data-testid="stSidebarCollapseButton"] button {{
    color: {"#FFFFFF" if dark_mode else "#0A1628"} !important;
    opacity: 1 !important;
    visibility: visible !important;
}}footer {{
                visibility: hidden;
            }}

            .creditiq-footer {{
                position: fixed;
                left: 0;
                right: 0;
                bottom: 0;
                padding: 0.5rem 1.25rem;
                background: linear-gradient(90deg, rgba(15, 23, 42, 0.96), rgba(15, 23, 42, 0.98));
                color: #9ca3af;
                font-size: 0.75rem;
                border-top: 1px solid rgba(55, 65, 81, 0.8);
                display: flex;
                justify-content: space-between;
                align-items: center;
                z-index: 999;
            }}

            .creditiq-footer span.brand {{
                color: #facc15;
                font-weight: 600;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }}
        </style>
    """

    st.markdown(css_base, unsafe_allow_html=True)

    if dark_mode:
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #020617 0%, #02040a 50%, #020617 100%) !important;
                color: var(--creditiq-text-primary);
                border-right: 1px solid rgba(15, 23, 42, 0.85);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


def render_footer() -> None:
    st.markdown(
        """
        <div class="creditiq-footer">
            <div>
                <span class="brand">Yuvaan Hackathon 2026</span>
                &nbsp;|&nbsp;
                CreditIQ – AI Credit Intelligence Engine for Indian Banks
            </div>
            <div>
                Built on Streamlit · Powered by Groq AI
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # =========================
    # Streamlit UI
    # =========================

st.set_page_config(
    page_title="CreditIQ – AI Credit Intelligence Engine",
    page_icon="💳",
    layout="wide",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

inject_custom_css(st.session_state.dark_mode)
dark_mode = st.session_state.dark_mode

# Theme-aware styling for all text areas (Collateral, Additional Details, Officer Notes)
if dark_mode:
    textarea_style = """
    <style>
    div[data-testid="stTextArea"] > div > div > textarea {
        background-color: #112240 !important;
        color: #FFFFFF !important;
        border: 1px solid #F59E0B !important;
        border-radius: 4px !important;
    }
    </style>
    """
else:
    textarea_style = """
    <style>
    div[data-testid="stTextArea"] > div > div > textarea {
        background-color: #FFFFFF !important;
        color: #0A1628 !important;
        border: 1px solid #1D4ED8 !important;
        border-radius: 4px !important;
    }
    </style>
    """

st.markdown(textarea_style, unsafe_allow_html=True)

if not dark_mode:
    light_fixes = """
    <style>
    /* Fix toggle button in light mode */
    div[data-testid="stCheckbox"] > label {
        background-color: #0A1628 !important;
        color: #FFFFFF !important;
        border: 2px solid #0A1628 !important;
        border-radius: 20px !important;
        padding: 4px 12px !important;
    }
    div[data-testid="stCheckbox"] svg {
        fill: #FFFFFF !important;
    }

    /* Fix sidebar background in light mode */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        color: #0A1628 !important;
    }
    [data-testid="stSidebar"] p {
        color: #0A1628 !important;
    }
[data-testid="stSidebarCollapseButton"] button {
    background-color: #0A1628 !important;
    border-radius: 50% !important;
    opacity: 1 !important;
}
[data-testid="stSidebarCollapseButton"] button svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}
[data-testid="stHeader"] button svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}
[data-testid="stHeader"] a {
    color: #FFFFFF !important;
}
[data-testid="stHeader"] span {
    color: #FFFFFF !important;
}
    /* Fix tab text colors in light mode */
    [data-testid="stTabs"] button {
        color: #0A1628 !important;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #0A1628 !important;
        border-bottom-color: #F59E0B !important;
    }
    [data-testid="stTabs"] button p {
        color: #0A1628 !important;
    }
    /* Fix chat bot message text in light mode */
    [data-testid="stChatMessage"] p {
        color: #0A1628 !important;
    }
    [data-testid="stChatMessage"] div {
        color: #0A1628 !important;
    }
    [data-testid="stChatMessageContent"] {
        color: #0A1628 !important;
    }
    /* Download button text white */
[data-testid="stDownloadButton"] button {
    color: #FFFFFF !important;
}
    /* Fix download button text */
[data-testid="stDownloadButton"] > button {
    color: #FFFFFF !important;
    background: linear-gradient(90deg, #FACC15, #F59E0B, #F97316) !important;
}
[data-testid="stDownloadButton"] > button p {
    color: #FFFFFF !important;
}

/* Fix blinking cursor color in input fields */
input {
    caret-color: #0A1628 !important;
}
textarea {
    caret-color: #0A1628 !important;
}
/* Chat input cursor white in light mode */
[data-testid="stChatInputTextArea"] textarea {
    caret-color: #FFFFFF !important;
}
   </style>
    """
    st.markdown(light_fixes, unsafe_allow_html=True)

# Hero header with theme toggle
hero_left, hero_right = st.columns([4, 1])

with hero_left:
    st.markdown(
        """
        <div class="creditiq-hero">
            <div class="creditiq-logo-pill">
                <span class="creditiq-logo-mark">CQ</span>
                <span>CreditIQ · Credit Intelligence Engine</span>
            </div>
            <div style="margin-top: 0.85rem;">
                <div class="creditiq-hero-heading">
                    Precision underwriting for <span class="accent">Indian credit</span>.
                </div>
                <div class="creditiq-hero-subtitle">
                    AI-powered CAMs that blend bureau behavior, GST, DSCR and collateral analysis
                    into one premium, committee-ready note.
                </div>
                <div class="creditiq-hero-meta">
                    <span class="creditiq-chip">Five C's of Credit</span>
                    <span class="creditiq-chip">Indian Banking Context</span>
                    <span class="creditiq-chip">Powered by Groq AI</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_right:
    st.write("")  # vertical spacer
    st.write("")
    mode_label = "🌙 Dark mode" if st.session_state.dark_mode else "☀️ Light mode"
    toggled = st.toggle(mode_label, value=st.session_state.dark_mode, key="theme_toggle")
    if toggled != st.session_state.dark_mode:
        st.session_state.dark_mode = toggled
        st.rerun()
    st.markdown('<span class="theme-toggle-label">Toggle visual theme</span>', unsafe_allow_html=True)


tab1, tab2 = st.tabs(["📋 Generate CAM", "💬 Chat with CreditIQ"])

with tab2:
    st.markdown("### 💬 Chat with CreditIQ")
    st.write("Ask me anything about credit appraisal, Indian banking, or loan analysis!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask CreditIQ anything..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are CreditIQ, an expert AI Credit Intelligence Engine for Indian banks. You help credit managers with loan appraisal, risk assessment, and credit decisions. Use Indian banking context — CIBIL, GST, RBI, DSCR, MCA, NCLT. Be professional and concise."},
                            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    reply = response.choices[0].message.content
                except Exception as e:
                    reply = f"Error: {e}"
                st.markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

with tab1:
    st.write(
        "Capture key borrower details below and let **CreditIQ** generate a structured "
        "Credit Appraisal Memo (CAM) using the Five C's of Credit."
    )


    col_main, col_side = st.columns([2.4, 1.6], gap="large")

with col_main:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-card-header">
            <div>
                <div class="section-title">Borrower & Facility Details</div>
                <div class="section-kicker">Core identifiers and facility structure</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    company_name = st.text_input("🏢 Company Name*", placeholder="Registered legal name")
    turnover = st.text_input("📊 Annual Turnover (₹ crore)*", placeholder="e.g., 75")
    loan_amount = st.text_input("💰 Proposed Loan Amount (₹ crore)*", placeholder="e.g., 20")
    loan_type = st.selectbox(
        "📄 Loan Type*",
        [
            "Term Loan – CAPEX",
            "Working Capital – CC/OD",
            "Working Capital – BG/LC",
            "Project Finance",
            "SME / MSME Term Loan",
            "Retail – Home Loan",
            "Retail – LAP",
            "Other",
        ],
    )

    gst_status = st.selectbox(
        "🧾 GST Status*",
        [
            "Active & Compliant",
            "Active – Occasional Delays",
            "Active – Frequent Delays",
            "Cancelled / Suspended",
            "Not Registered",
        ],
    )

    legal_cases = st.selectbox(
        "⚖️ Legal Cases / Litigations*",
        [
            "No adverse legal cases",
            "Minor civil cases (non-financial)",
            "Ongoing financial/legal disputes",
            "Major litigations / NCLT / SARFAESI",
        ],
    )

    promoter_background = st.selectbox(
        "👤 Promoter Background*",
        [
            "Strong & experienced promoters",
            "Moderately experienced promoters",
            "New / first-generation entrepreneurs",
            "Adverse market feedback / concerns",
        ],
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-card-header">
            <div>
                <div class="section-title">Security & Financials</div>
                <div class="section-kicker">Collateral, ratios and officer insights</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Theme-aware styling for the three text areas
    st.markdown(
        """
        <style>
        /* Dark mode text areas */
        [data-theme="dark"] div[data-testid="stTextArea"] > div > div > textarea {
            background-color: #112240 !important;
            color: #FFFFFF !important;
            border: 1px solid #F59E0B !important;
            border-radius: 4px !important;
            box-shadow: none !important;
        }

        /* Light mode text areas */
        [data-theme="light"] div[data-testid="stTextArea"] > div > div > textarea {
            background-color: #FFFFFF !important;
            color: #0A1628 !important;
            border: 1px solid #1D4ED8 !important;
            border-radius: 4px !important;
            box-shadow: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    collateral = st.text_area(
        "🏦 Collateral Offered",
        placeholder="Details of primary and collateral security – type of property, valuation, margin, other comfort.",
    )

    additional_details = st.text_area(
        "📑 Additional Financial Details",
        placeholder="Key ratios if known (DSCR, TOL/TNW, current ratio), banking conduct, other lenders, etc.",
        height=110,
    )

    officer_notes = st.text_area(
        "📝 Credit Officer Notes",
        placeholder="Any specific strengths, risks, deviations from policy, or contextual notes for the sanctioning authority.",
        height=110,
    )

    generate_clicked = st.button("Generate Credit Appraisal Memo")
    st.markdown("</div>", unsafe_allow_html=True)

    cam_text = ""
    decision = None

    if generate_clicked:
        if not company_name or not turnover or not loan_amount:
            st.error("Please fill all mandatory fields marked with * before generating the CAM.")
        else:
            progress = st.progress(0, text="Preparing CAM prompt…")
            prompt = build_cam_prompt(
                company_name=company_name,
                turnover=turnover,
                loan_amount=loan_amount,
                loan_type=loan_type,
                gst_status=gst_status,
                legal_cases=legal_cases,
                promoter_background=promoter_background,
                collateral=collateral,
                additional_details=additional_details,
                officer_notes=officer_notes,
            )
            progress.progress(35, text="Analysing borrower profile and covenants…")

            with st.spinner("Generating Credit Appraisal Memo using Groq AI…"):
                cam_text = get_groq_cam(prompt)
            progress.progress(80, text="Deriving decision from CAM…")
            decision = extract_decision(cam_text)
            progress.progress(100, text="Completed.")

            if decision:
                if decision == "APPROVE":
                    st.markdown(
                        """
                        <div class="decision-banner decision-approve">
                            ✅ APPROVE – CreditIQ indicates this proposal is supportable, subject to policy & committee approval.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        """
                        <div class="decision-banner decision-reject">
                            ⛔ REJECT – CreditIQ indicates this proposal is not supportable in its current form.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            if cam_text:
                st.markdown("### Generated Credit Appraisal Memo")
                st.markdown('<div class="cam-box">', unsafe_allow_html=True)
                st.markdown(cam_text.replace("\n", "  \n"))
                st.markdown("</div>", unsafe_allow_html=True)

                filename = build_download_filename(company_name)
                st.download_button(
                    label="Download CAM as Text",
                    data=cam_text,
                    file_name=filename,
                    mime="text/plain",
                )

with st.sidebar:
    if True:
            st.markdown(
                """
                <div class="sidebar-card">
                    <div class="sidebar-card-title">
                        <span class="sidebar-badge sidebar-badge-gold">🧠</span>
                        <span>CREDITIQ SNAPSHOT</span>
                    </div>
                    <div class="sidebar-divider"></div>
                    <div class="sidebar-card-body">
                        AI-powered credit intelligence engine designed for Indian banks and NBFCs.
                        Generates committee-ready CAMs grounded in local regulations and bureau behavior.
                    </div>
                </div>
                <div class="sidebar-card">
                    <div class="sidebar-card-title">
                        <span class="sidebar-badge sidebar-badge-blue">🇮🇳</span>
                        <span>INDIAN CREDIT LENS</span>
                    </div>
                    <div class="sidebar-divider"></div>
                    <div class="sidebar-card-body">
                        • CIBIL / Bureau behaviour<br/>
                        • GST compliance patterns<br/>
                        • Cash flow & DSCR comfort<br/>
                        • Collateral coverage & LTV<br/>
                        • Policy & RBI-aligned prudence
                    </div>
                </div>
                <div class="sidebar-card">
                    <div class="sidebar-card-title">
                        <span class="sidebar-badge sidebar-badge-orange">⚠️</span>
                        <span>USAGE NOTE</span>
                    </div>
                    <div class="sidebar-divider"></div>
                    <div class="sidebar-card-body">
                        Use CreditIQ as a decision-support layer. Final sanction remains subject
                        to internal credit policy, due diligence and committee approval.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


render_footer()

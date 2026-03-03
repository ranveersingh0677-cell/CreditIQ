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


def inject_custom_css() -> None:
    """Apply custom dark navy and gold theme."""
    st.markdown(
        """
        <style>
            [data-testid="stAppViewContainer"] {
                background: radial-gradient(circle at top left, #0b1730 0%, #020617 45%, #02040a 100%);
                color: #e5e7eb;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #020617 0%, #02040a 50%, #020617 100%);
                color: #e5e7eb;
                border-right: 1px solid rgba(251, 191, 36, 0.25);
            }

            .creditiq-title {
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                background: linear-gradient(90deg, #facc15, #f59e0b, #fbbf24);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .subtitle {
                color: #9ca3af;
                font-size: 0.9rem;
                letter-spacing: 0.06em;
                text-transform: uppercase;
            }

            .stButton>button {
                background: linear-gradient(90deg, #facc15, #f97316);
                color: #020617;
                border-radius: 9999px;
                font-weight: 600;
                border: none;
                padding: 0.5rem 1.75rem;
                box-shadow: 0 10px 25px rgba(234, 179, 8, 0.25);
            }

            .stButton>button:hover {
                background: linear-gradient(90deg, #fbbf24, #fb923c);
                box-shadow: 0 16px 40px rgba(234, 179, 8, 0.40);
            }

            .decision-banner {
                border-radius: 0.75rem;
                padding: 0.85rem 1.25rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-size: 0.9rem;
                display: flex;
                align-items: center;
                gap: 0.6rem;
            }

            .decision-approve {
                background: rgba(22, 163, 74, 0.12);
                border: 1px solid rgba(22, 163, 74, 0.6);
                color: #bbf7d0;
            }

            .decision-reject {
                background: rgba(220, 38, 38, 0.12);
                border: 1px solid rgba(220, 38, 38, 0.6);
                color: #fecaca;
            }

            .cam-box {
                background: rgba(15, 23, 42, 0.8);
                border-radius: 0.75rem;
                border: 1px solid rgba(148, 163, 184, 0.25);
                padding: 1rem 1.25rem;
                backdrop-filter: blur(12px);
            }

            footer {
                visibility: hidden;
            }

            .creditiq-footer {
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
            }

            .creditiq-footer span.brand {
                color: #facc15;
                font-weight: 600;
                letter-spacing: 0.08em;
                text-transform: uppercase;
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

inject_custom_css()


with st.sidebar:
    st.markdown('<h2 class="creditiq-title">CreditIQ</h2>', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="subtitle">AI CREDIT INTELLIGENCE</p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        """
        **Why CreditIQ?**

        - AI-assisted CAM generation
        - Consistent Five C's assessment
        - Embedded Indian banking context (CIBIL, GST, RBI)
        - Faster credit decisioning for PSU & private banks

        **Disclaimer**: This is an AI assistant and should be used to
        augment, not replace, human credit judgment. All approvals are
        subject to each bank's internal credit policy and RBI guidelines.
        """
    )

    st.markdown("---")
    st.caption("Version 0.1 · Built for YUVAAN Hackathon 2026")


st.markdown(
    """
    <h1 class="creditiq-title">CreditIQ</h1>
    <p class="subtitle">AI powered credit intelligence engine for indian banks</p>
    """,
    unsafe_allow_html=True,
)

st.write(
    "Capture key borrower details below and let **CreditIQ** generate a structured "
    "Credit Appraisal Memo (CAM) using the Five C's of Credit."
)


col_main, col_side = st.columns([2.5, 1.5], gap="large")

with col_main:
    st.subheader("Borrower & Facility Details")

    company_name = st.text_input("Company Name*")
    turnover = st.text_input("Annual Turnover (₹ crore)*", placeholder="e.g., 75")
    loan_amount = st.text_input("Proposed Loan Amount (₹ crore)*", placeholder="e.g., 20")
    loan_type = st.selectbox(
        "Loan Type*",
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
        "GST Status*",
        [
            "Active & Compliant",
            "Active – Occasional Delays",
            "Active – Frequent Delays",
            "Cancelled / Suspended",
            "Not Registered",
        ],
    )

    legal_cases = st.selectbox(
        "Legal Cases / Litigations*",
        [
            "No adverse legal cases",
            "Minor civil cases (non-financial)",
            "Ongoing financial/legal disputes",
            "Major litigations / NCLT / SARFAESI",
        ],
    )

    promoter_background = st.selectbox(
        "Promoter Background*",
        [
            "Strong & experienced promoters",
            "Moderately experienced promoters",
            "New / first-generation entrepreneurs",
            "Adverse market feedback / concerns",
        ],
    )

    collateral = st.text_area(
        "Collateral Offered",
        placeholder="Details of primary and collateral security – type of property, valuation, margin, other comfort.",
    )

    additional_details = st.text_area(
        "Additional Financial Details",
        placeholder="Key ratios if known (DSCR, TOL/TNW, current ratio), banking conduct, other lenders, etc.",
        height=120,
    )

    officer_notes = st.text_area(
        "Credit Officer Notes",
        placeholder="Any specific strengths, risks, deviations from policy, or contextual notes for the sanctioning authority.",
        height=120,
    )

    generate_clicked = st.button("Generate Credit Appraisal Memo", use_container_width=False)

    cam_text = ""
    decision = None

    if generate_clicked:
        if not company_name or not turnover or not loan_amount:
            st.error("Please fill all mandatory fields marked with * before generating the CAM.")
        else:
            with st.spinner("Analysing borrower profile and generating CAM using Groq AI..."):
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
                cam_text = get_groq_cam(prompt)
                decision = extract_decision(cam_text)

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

with col_side:
    st.subheader("Indian Credit Lens")
    st.markdown(
        """
        - **CIBIL / Bureau**: Considers bureau behavior and delinquency patterns.
        - **GST**: Looks at compliance, filing regularity and potential leakages.
        - **DSCR**: Evaluates repayment capacity vis-à-vis cash flows.
        - **RBI**: Aligns to broad prudential norms (without citing specific circular numbers).
        - **Security**: Weighs primary and collateral coverage, LTV and margins.

        Use this as a **decision-support tool** alongside your bank's credit policy.
        """
    )


render_footer()

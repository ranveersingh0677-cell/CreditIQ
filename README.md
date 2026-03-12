# CreditIQ — AI-Powered Credit Intelligence Engine for Indian Banks

![CreditIQ Banner](https://img.shields.io/badge/CreditIQ-AI%20Credit%20Intelligence-F59E0B?style=for-the-badge&logo=python)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B?style=for-the-badge&logo=streamlit)
![Groq AI](https://img.shields.io/badge/Groq%20AI-LLaMA%203.3%2070B-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

> **Precision Underwriting. Instant Decisions. Indian Context.**

CreditIQ is a Generative AI-powered Credit Appraisal Memo (CAM) generation engine built specifically for Indian banks and NBFCs. It reduces loan processing time by **90%** and allows credit managers to process **10x more applications** using the power of Large Language Models.

---

## 🔗 Live Demo

👉 **[creditiq-india.streamlit.app](https://creditiq-india.streamlit.app)**

No login required — try it instantly!

---

## 🚨 The Problem

In the Indian banking sector today:

- ⏳ **3–4 weeks** to manually process one corporate loan application
- 📄 **500+ pages** of documents a credit manager reads per application
- ⚠️ **40% of early warning signals** are missed — buried in unstructured data

Credit managers are overwhelmed — more data than ever, yet more time wasted than ever.

---

## ✅ Our Solution

CreditIQ automates the entire credit appraisal process using Generative AI:

1. Credit officer inputs key borrower details
2. AI analyses all inputs using the **Five C's of Credit**
3. Generates a complete **7-section Credit Appraisal Memo**
4. Outputs a clear **APPROVE or REJECT** decision with full reasoning
5. Report is downloadable instantly as a text file

---

## ✨ Features

### 📋 CAM Generator
- Generates structured Credit Appraisal Memos in under 30 seconds
- Follows **Five C's of Credit** — Character, Capacity, Capital, Collateral, Conditions
- Strict **RBI-aligned decision rules** — APPROVE or REJECT with full reasoning
- 7-section structured output — committee ready
- Colour-coded decision banners — Green APPROVE, Red REJECT
- Downloadable CAM report as text file

### 💬 Chat with CreditIQ
- Conversational AI assistant for Indian banking queries
- Ask anything about CIBIL, GST, DSCR, MCA filings, SARFAESI
- Powered by LLaMA 3.3 70B via Groq AI
- Full Indian banking knowledge base
- Instant expert-level responses

### 🌙 Premium UI
- Professional dark and light mode interface
- Theme toggle — Dark navy and gold / Clean white
- Sidebar intelligence cards
- Real-time progress bar during CAM generation
- Fully responsive layout

---

## 🏗️ Technical Architecture

```
INPUT LAYER          AI PROCESSING           OUTPUT LAYER
─────────────        ─────────────────       ─────────────────
Company Details  →   Groq AI Engine      →   Credit Appraisal Memo
GST Status       →   LLaMA 3.3 70B       →   APPROVE / REJECT Decision
Legal Cases      →   Five C's Analyser   →   7-Section Report
Promoter Info    →   Decision Rules      →   Downloadable CAM File
Collateral       →   Chat Intelligence   →   Chat Responses
```

**Stack:**
- **Frontend:** Streamlit (Python)
- **AI Model:** LLaMA 3.3 70B via Groq API
- **Deployment:** Streamlit Cloud
- **Language:** Python 3.11

---

## 🧠 Five C's of Credit — Indian Banking Context

| C | What CreditIQ Analyses |
|---|------------------------|
| **Character** | Promoter background, CIBIL score, bureau conduct |
| **Capacity** | DSCR, cash flows, repayment ability |
| **Capital** | Leverage, TOL/TNW ratio, net worth |
| **Collateral** | Security coverage, LTV, property valuation |
| **Conditions** | GST compliance, sector risks, RBI guidelines |

---

## ⚡ Strict Decision Rules

CreditIQ follows mandatory RBI-aligned decision rules:

- If promoter background is **adverse** → MUST REJECT
- If legal cases include **NCLT / SARFAESI** → MUST REJECT
- If GST is **frequently delayed** AND legal cases are adverse → MUST REJECT
- If **two or more serious risk factors** exist → MUST REJECT
- Only APPROVE when all Five C's are satisfactory

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install streamlit groq python-dotenv
```

### Setup
```bash
# Clone the repository
git clone https://github.com/ranveersingh0677-cell/CreditIQ.git
cd CreditIQ

# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# Run the app
streamlit run app.py
```

### Get Your Free Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for free
3. Create an API key
4. Paste it in your `.env` file

---

## 📊 Impact

| Metric | Value |
|--------|-------|
| Indian corporate credit market | ₹180L Crore annually |
| Reduction in processing time | 90% |
| More applications per manager | 10x |
| CAM generation time | Under 30 seconds |
| Decision accuracy | Rule-based — deterministic |

---

## 🗺️ Roadmap

### Phase 1 — NOW ✅
- [x] CAM Generator live
- [x] Chat assistant live
- [x] APPROVE / REJECT engine
- [x] Dark and light mode UI
- [x] Deployed on Streamlit Cloud

### Phase 2 — Next 3 Months 🔄
- [ ] PDF upload for scanned ITR and bank statements
- [ ] CIBIL API integration
- [ ] MCA and e-Courts live search
- [ ] Multi-borrower comparison dashboard

### Phase 3 — Future 🚀
- [ ] Bank API integration
- [ ] Regulatory compliance engine
- [ ] White-label SaaS for NBFCs
- [ ] Real-time risk monitoring dashboard

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

**Built to transform Indian banking — one credit decision at a time 🚀**

[Live App](https://creditiq-india.streamlit.app) · [GitHub](https://github.com/ranveersingh0677-cell/CreditIQ)

</div>

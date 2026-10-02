# 🛡️ PhishGuard — Built for a Friend

> **A Privacy-First Open Source AI Security Shield against Spear Phishing & Social Engineering**  
> Powered by **Google Gemma 2 Open Weights** & Local Forensic Heuristics.

[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-2026-blueviolet.svg)](https://hacktoberfest.com/)
[![Built with Gemma](https://img.shields.io/badge/Model-Google_Gemma_2-4285F4.svg)](https://ai.google.dev/gemma)
[![Deploy on Render](https://img.shields.io/badge/Deploy-Render-46E3B7.svg)](https://render.com)

---

## 💡 The Story: Why I Built This for Alex

Last week, my close college friend **Alex** nearly fell victim to a sophisticated spear-phishing attack. An email arrived appearing to be from our university's bursar's office, complete with his correct student ID and academic department, urging him to verify his direct deposit details to receive an emergency grant within 12 hours.

Alex had a bad feeling, but **he hesitated to paste the email into commercial cloud LLMs (like ChatGPT)** because the message contained his real name, phone number, and student reference. He didn't want his personal identifiers stored on third-party model servers.

**PhishGuard was built specifically for Alex:**  
An open-source, air-gapped security analyzer that can run completely on his own laptop with **Google Gemma 2**, providing zero data leakage, zero subscription costs, and forensic-grade threat detection.

---

## ✨ Core Capabilities

- **Zero-Leakage Local Inference**: Analyzes sensitive messages offline via Gemma 2 open weights.
- **Deception Tactic Breakdown**: Unpacks psychological coercion, homoglyph domain impersonation, and unverified redirect chains.
- **Friend-Friendly Remediation**: Translates complex security telemetry into 1-2-3 plain English actionable steps.
- **Instant Dual-Mode Engine**: Operates seamlessly in full local air-gapped mode or cloud API preview mode.

---

## 🚀 Quickstart (Running Locally in 1 Minute)

```bash
# Clone the repository
git clone https://github.com/yourusername/phishguard-gemma.git
cd phishguard-gemma

# Install dependencies
pip install -r requirements.txt

# Launch the Streamlit application
streamlit run app.py
```

---

## 🌐 Deploy to Render

PhishGuard includes a ready-to-use `render.yaml` blueprint. Simply link your GitHub repository to Render and deploy as a free Web Service.

---

## 🏆 Hacktoberfest 2026 Submission

- **Challenge**: *Build for a Friend* (Weekend Challenge)
- **Target Categories**: 
  - `Best Use of Gemma`
  - `Best Use of Render`
  - Overall Winner

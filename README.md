# 🛡️ PhishGuard

[![CI Test Suite](https://github.com/Hao610/phishguard-gemma/actions/workflows/ci.yml/badge.svg)](https://github.com/Hao610/phishguard-gemma/actions)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python: 3.10 | 3.11 | 3.12](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python)](https://www.python.org/)
[![AI Architecture: Google Gemma 2](https://img.shields.io/badge/Model-Google%20Gemma%202-4285F4?logo=google)](https://ai.google.dev/gemma)
[![Deployment: Render Blueprint](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render)](https://phishguard-gemma.onrender.com/)
[![Streamlit Cloud](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?logo=streamlit)](https://phishguard-gemma.streamlit.app/)

> **Zero-Leakage Spear-Phishing Threat Scanner & Forensic Auditor**  
> *Built for a Friend (Alex) | Hacktoberfest 2026 Challenge*

🌐 **Live Instances:**
- 🚀 **Official Render Cloud:** [phishguard-gemma.onrender.com](https://phishguard-gemma.onrender.com/) *(Official Hackathon Host)*
- ⚡ **Instant Streamlit Mirror:** [phishguard-gemma.streamlit.app](https://phishguard-gemma.streamlit.app/) *(Zero Cold-Start)*

---

## 💡 The Origin: Built for Alex

Alex almost fell for a spear-phishing email that quoted his **real student ID and tuition balance**.  
He wanted to verify it with AI, but stopped:

> *"Can I paste this email into ChatGPT? It has my real student ID and financial record in it..."*

That moment exposed the **core paradox of modern anti-phishing tools**:
> **The messages most in need of analysis are the ones least safe to upload.**

**PhishGuard** was built to solve this. It inverts the paradigm by running a **privacy-first, dual-stage pipeline**:
1. **Local Privacy Shield:** Automatically strips Personal Identifiable Information (PII) before any telemetry leaves your machine.
2. **Offline-First Heuristics + Gemma 2 Intelligence:** Detects multi-vector social engineering via local rules or Google Gemma 2 open architecture.

---

## ✨ Key Features

- 🔒 **Zero Data Leakage:** PII scrubber automatically redacts credit cards (Luhn format), student IDs, Malaysian NRIC, phone numbers, and emails locally.
- 🔬 **11-Dimensional Threat Heuristic Engine:** Extracts weighted urgency triggers, lookalike domains (homoglyphs), raw IP URLs, URL shorteners, suspicious TLDs, and credential harvesting paths.
- 🧠 **Google Gemma 2 AI Architecture:** Formats inputs using Gemma 2's native `<start_of_turn>` chat structure to produce SOC-grade forensic assessments.
- 🎨 **Adaptive Dual-Theme System:** Features industrial-grade **Obsidian Dark** and **Titanium Light** precision themes that sync with Streamlit's native settings.
- 🔗 **Live Defanged URL Inspector:** Automatically transforms hazardous links (`http://...` → `hxxp[://]...[.]...`) to prevent accidental clicks.
- 📄 **SOC-Ready Incident Response Reports:** Automatically generates printable `.txt` reports complete with SHA-256 evidence chain hashes and remediation steps.
- ⚡ **100% Air-Gap Compatible:** Completely operational without an internet connection or API keys.

---

## 🏗️ Technical Architecture

```
                       ┌─────────────────────────┐
                       │  Incoming Raw Message   │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │  Stage 1: Privacy Shield│
                       │  (Local PII Redaction)  │
                       └────────────┬────────────┘
                                    │ Sanitized Text
                 ┌──────────────────┴──────────────────┐
                 ▼                                     ▼
   ┌───────────────────────────┐         ┌───────────────────────────┐
   │  Stage 2: Heuristic Core  │         │  Stage 3: Gemma 2 Engine  │
   │  - 11 Threat Vectors      │         │  - Google Gemma 2 9B-IT   │
   │  - Weighted Urgency Regex │         │  - Structured JSON Output │
   │  - Homoglyph Detection    │         │  - Adversarial Prompting  │
   └─────────────┬─────────────┘         └─────────────┬─────────────┘
                 │                                     │
                 └──────────────────┬──────────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │ Stage 4: SOC Report Gen │
                       │ - Threat Index (0-100)  │
                       │ - SHA-256 Hash Evidence │
                       │ - Defanged IoC Chain    │
                       └─────────────────────────┘
```

---

## 🚀 Quickstart Guide

### Option 1: One-Click Cloud Deployment (Render)

Deploy your own private instance on Render's infrastructure in under 2 minutes:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Hao610/phishguard-gemma)

The included [`render.yaml`](render.yaml) blueprint automatically manages Python runtimes and Streamlit launch flags.

---

### Option 2: Local Installation (Recommended for Maximum Privacy)

```bash
# 1. Clone the repository
git clone https://github.com/Hao610/phishguard-gemma.git
cd phishguard-gemma

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# 3. Install lightweight dependencies
pip install -r requirements.txt

# 4. Launch the dashboard
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 💻 CLI & Forensic Mail Parser

PhishGuard includes a standalone command-line interface and MIME email parser:

```bash
# Direct text audit
python cli.py scan "URGENT: Your Wells Fargo account is suspended. Verify at http://wellsfarg0.xyz"

# Raw .eml file audit (extracts SPF, DKIM, and Return-Path headers)
python cli.py scan-file tests/sample_phish.eml
```

---

## 🧪 Automated Unit Testing

PhishGuard maintains automated unit test coverage across 13 security test cases:

```bash
pytest tests/ -v
```

```text
tests/test_engine.py::test_bank_phishing_critical PASSED                 [  7%]
tests/test_engine.py::test_credential_harvesting_detection PASSED        [ 15%]
tests/test_engine.py::test_legitimate_email_safe PASSED                  [ 23%]
tests/test_engine.py::test_ip_url_detection PASSED                       [ 30%]
tests/test_engine.py::test_shortened_url_detection PASSED                [ 38%]
tests/test_engine.py::test_pii_redaction_phone_card_email PASSED         [ 46%]
tests/test_engine.py::test_pii_redaction_preserves_safe_content PASSED   [ 53%]
tests/test_engine.py::test_url_defanging_http PASSED                     [ 61%]
tests/test_engine.py::test_url_defanging_https PASSED                    [ 69%]
tests/test_engine.py::test_ioc_extracts_all_dimensions PASSED            [ 76%]
tests/test_engine.py::test_incident_report_contains_hash PASSED          [ 84%]
tests/test_engine.py::test_incident_report_defangs_urls PASSED           [ 92%]
tests/test_engine.py::test_eml_parser_extracts_headers PASSED            [100%]
```

---

## 📜 License

Distributed under the Apache 2.0 Open Source License. See [`LICENSE`](LICENSE) for details.

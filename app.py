"""
PhishGuard — Zero-Leakage Threat Scanner
Built for a Friend (Alex) | Hacktoberfest 2026
Powered by Google Gemma 2 Open-Source AI Architecture

Dual-Theme Design System: Obsidian Dark & Titanium Precision
Strict semantic token architecture, zero hardcoded color coupling.
"""

import streamlit as st
import time
import plotly.graph_objects as go
from engine import PhishGuardEngine

# ─────────────────────────────────────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="PhishGuard | Zero-Leakage Threat Scanner",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/Hao610/phishguard-gemma",
        "Report a bug": "https://github.com/Hao610/phishguard-gemma/issues",
        "About": "PhishGuard — Privacy-first phishing forensics powered by Google Gemma 2",
    }
)

# ─────────────────────────────────────────────────────────────────────────────
# Theme State Initialization (DOM + LocalStorage + Session Synchronizer)
# ─────────────────────────────────────────────────────────────────────────────

if "theme" not in st.session_state:
    st.session_state.theme = "system"  # 'system' | 'dark' | 'light'

# ─────────────────────────────────────────────────────────────────────────────
# Dual-Theme Engine (Obsidian Dark & Titanium Light)
# ─────────────────────────────────────────────────────────────────────────────

def inject_dual_theme_engine(active_theme: str):
    """
    Injects the complete semantic Design Token CSS variables, button system,
    dot-matrix background canvas, and DOM root attributes.
    """
    resolved_theme_attr = f'data-theme="{active_theme}"' if active_theme in ["dark", "light"] else ""
    
    css_content = f"""
<script>
    // Zero-flicker sync: synchronize DOM root attribute with state or system preference
    (function() {{
        const themeChoice = "{active_theme}";
        let finalTheme = themeChoice;
        if (themeChoice === "system") {{
            finalTheme = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? "light" : "dark";
        }}
        document.documentElement.setAttribute("data-theme", finalTheme);
        const stAppContainer = window.parent.document.querySelector('.stApp') || document.querySelector('.stApp');
        if (stAppContainer) {{
            stAppContainer.setAttribute("data-theme", finalTheme);
        }}
    }})();
</script>

<style>
/* ==========================================================================
   SEMANTIC DESIGN TOKENS (DUAL-THEME ENGINE)
   ========================================================================== */

/* 1. Default: Obsidian Titanium Dark Mode (System Fallback & Explicit Dark) */
:root,
[data-theme="dark"] {{
    --app-bg: #050507;
    --dot-color: rgba(255, 255, 255, 0.08);
    --surface-card: rgba(12, 12, 16, 0.55);
    --surface-card-hover: rgba(18, 18, 24, 0.70);
    --border-color: rgba(255, 255, 255, 0.08);
    --border-hover: rgba(255, 255, 255, 0.25);
    
    --text-primary: #ffffff;
    --text-secondary: #a1a1aa;
    --text-muted: #71717a;
    
    /* Primary CTA */
    --btn-primary-bg: linear-gradient(180deg, #27272a 0%, #18181b 100%);
    --btn-primary-border: rgba(255, 255, 255, 0.28);
    --btn-primary-text: #ffffff;
    --btn-primary-shadow: 0 4px 14px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15);
    --btn-primary-hover-bg: linear-gradient(180deg, #3f3f46 0%, #27272a 100%);
    --btn-primary-hover-border: rgba(255, 255, 255, 0.45);

    /* Secondary Action */
    --btn-sec-bg: rgba(255, 255, 255, 0.04);
    --btn-sec-border: rgba(255, 255, 255, 0.10);
    --btn-sec-text: #d4d4d8;
    --btn-sec-hover-bg: rgba(255, 255, 255, 0.08);
    --btn-sec-hover-border: rgba(255, 255, 255, 0.22);
    
    /* Input & Code Elements */
    --input-bg: #09090b;
    --input-border: rgba(255, 255, 255, 0.12);
    --input-focus-border: #38bdf8;
    --code-bg: #09090d;
    --code-text: #38bdf8;
    
    /* Gauge Chart Theme */
    --gauge-paper: #050507;
    --gauge-bg: #0c0c12;
    --gauge-border: #27272a;
    --gauge-num: #ffffff;
    --gauge-tick: #71717a;
}}

/* 2. System Level Light Query Fallback (When no explicit override) */
@media (prefers-color-scheme: light) {{
    :root:not([data-theme="dark"]) {{
        --app-bg: #f8fafc;
        --dot-color: rgba(15, 23, 42, 0.06);
        --surface-card: #ffffff;
        --surface-card-hover: #f1f5f9;
        --border-color: rgba(15, 23, 42, 0.10);
        --border-hover: rgba(15, 23, 42, 0.28);
        
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #64748b;
        
        /* Primary CTA */
        --btn-primary-bg: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%);
        --btn-primary-border: rgba(15, 23, 42, 0.25);
        --btn-primary-text: #0f172a;
        --btn-primary-shadow: 0 2px 8px rgba(15, 23, 42, 0.08), inset 0 1px 0 #ffffff;
        --btn-primary-hover-bg: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        --btn-primary-hover-border: #0f172a;

        /* Secondary Action */
        --btn-sec-bg: rgba(255, 255, 255, 0.85);
        --btn-sec-border: rgba(15, 23, 42, 0.12);
        --btn-sec-text: #1e293b;
        --btn-sec-hover-bg: #ffffff;
        --btn-sec-hover-border: rgba(15, 23, 42, 0.30);
        
        /* Input & Code Elements */
        --input-bg: #ffffff;
        --input-border: rgba(15, 23, 42, 0.15);
        --input-focus-border: #0284c7;
        --code-bg: #f1f5f9;
        --code-text: #0369a1;

        /* Gauge Chart Theme */
        --gauge-paper: #f8fafc;
        --gauge-bg: #ffffff;
        --gauge-border: #cbd5e1;
        --gauge-num: #0f172a;
        --gauge-tick: #64748b;
    }}
}}

/* 3. Explicit Titanium Precision Light Mode */
[data-theme="light"] {{
    --app-bg: #f8fafc;
    --dot-color: rgba(15, 23, 42, 0.06);
    --surface-card: #ffffff;
    --surface-card-hover: #f1f5f9;
    --border-color: rgba(15, 23, 42, 0.10);
    --border-hover: rgba(15, 23, 42, 0.28);
    
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #64748b;
    
    /* Primary CTA */
    --btn-primary-bg: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%);
    --btn-primary-border: rgba(15, 23, 42, 0.25);
    --btn-primary-text: #0f172a;
    --btn-primary-shadow: 0 2px 8px rgba(15, 23, 42, 0.08), inset 0 1px 0 #ffffff;
    --btn-primary-hover-bg: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    --btn-primary-hover-border: #0f172a;

    /* Secondary Action */
    --btn-sec-bg: rgba(255, 255, 255, 0.85);
    --btn-sec-border: rgba(15, 23, 42, 0.12);
    --btn-sec-text: #1e293b;
    --btn-sec-hover-bg: #ffffff;
    --btn-sec-hover-border: rgba(15, 23, 42, 0.30);
    
    /* Input & Code Elements */
    --input-bg: #ffffff;
    --input-border: rgba(15, 23, 42, 0.15);
    --input-focus-border: #0284c7;
    --code-bg: #f1f5f9;
    --code-text: #0369a1;

    /* Gauge Chart Theme */
    --gauge-paper: #f8fafc;
    --gauge-bg: #ffffff;
    --gauge-border: #cbd5e1;
    --gauge-num: #0f172a;
    --gauge-tick: #64748b;
}}

/* ==========================================================================
   GLOBAL CANVAS & SURFACE ARCHITECTURE
   ========================================================================== */

/* Universal smooth transition */
*, *::before, *::after {{
    transition: background-color 0.22s cubic-bezier(0.16, 1, 0.3, 1),
                border-color 0.22s cubic-bezier(0.16, 1, 0.3, 1),
                color 0.22s cubic-bezier(0.16, 1, 0.3, 1),
                box-shadow 0.22s cubic-bezier(0.16, 1, 0.3, 1);
}}

/* App canvas with industrial precision dot-matrix texture */
.stApp {{
    background-color: var(--app-bg) !important;
    background-image: radial-gradient(var(--dot-color) 1.5px, transparent 1.5px) !important;
    background-size: 24px 24px !important;
    color: var(--text-primary) !important;
}}

/* Sidebar styling */
section[data-testid="stSidebar"] {{
    background-color: var(--surface-card) !important;
    border-right: 1px solid var(--border-color) !important;
    backdrop-filter: blur(16px);
}}
section[data-testid="stSidebar"] * {{
    color: var(--text-primary);
}}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] caption {{
    color: var(--text-secondary) !important;
}}

/* Typography */
h1, h2, h3, h4, h5, h6 {{
    color: var(--text-primary) !important;
    font-weight: 700 !important;
}}
p, span, label {{
    color: var(--text-secondary);
}}
.stCaption, caption {{
    color: var(--text-muted) !important;
}}

/* Header typography */
.main-header {{
    font-size: 2.3rem;
    font-weight: 900;
    letter-spacing: -0.6px;
    margin-bottom: 2px;
    background: linear-gradient(90deg, #0ea5e9 0%, #38bdf8 50%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.sub-header {{
    font-size: 1.02rem;
    color: var(--text-secondary) !important;
    margin-bottom: 22px;
}}

/* Surface Card Container */
.cyber-card {{
    background-color: var(--surface-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px;
    padding: 16px 20px;
    backdrop-filter: blur(14px);
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.06);
}}
.cyber-card:hover {{
    border-color: var(--border-hover) !important;
}}

/* ==========================================================================
   BUTTON SYSTEM (NON-INVERTED INDUSTRIAL SYSTEM)
   ========================================================================== */

/* All Streamlit standard buttons (Secondary Action: Scenario Selectors, etc.) */
div[data-testid="stButton"] > button:not([kind="primary"]) {{
    background: var(--btn-sec-bg) !important;
    border: 1px solid var(--btn-sec-border) !important;
    border-radius: 10px !important;
    color: var(--btn-sec-text) !important;
    font-weight: 600 !important;
    padding: 10px 16px !important;
    backdrop-filter: blur(8px);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
}}
div[data-testid="stButton"] > button:not([kind="primary"]):hover {{
    background: var(--btn-sec-hover-bg) !important;
    border-color: var(--btn-sec-hover-border) !important;
    transform: translateY(-1px);
}}
div[data-testid="stButton"] > button:not([kind="primary"]) * {{
    color: inherit !important;
}}

/* Primary CTA Button (Audit Execution) */
div[data-testid="stButton"] > button[kind="primary"] {{
    background: var(--btn-primary-bg) !important;
    border: var(--btn-primary-border) !important;
    border-radius: 10px !important;
    color: var(--btn-primary-text) !important;
    font-weight: 700 !important;
    padding: 12px 20px !important;
    box-shadow: var(--btn-primary-shadow) !important;
}}
div[data-testid="stButton"] > button[kind="primary"]:hover {{
    background: var(--btn-primary-hover-bg) !important;
    border: 1px solid var(--btn-primary-hover-border) !important;
    transform: translateY(-1px);
}}
div[data-testid="stButton"] > button[kind="primary"] * {{
    color: inherit !important;
}}

/* Text Area Input */
div[data-baseweb="textarea"] {{
    background-color: var(--input-bg) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: 10px !important;
}}
div[data-baseweb="textarea"]:focus-within {{
    border-color: var(--input-focus-border) !important;
    box-shadow: 0 0 0 1px var(--input-focus-border) !important;
}}
textarea {{
    color: var(--text-primary) !important;
    background-color: transparent !important;
}}

/* Code Blocks & Defanged Urls */
div[data-testid="stCodeBlock"] {{
    background-color: var(--code-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
}}
code {{
    color: var(--code-text) !important;
}}

/* Timeline Action Steps */
.timeline-step {{
    border-left: 2px solid #0284c7;
    padding-left: 14px;
    margin-bottom: 12px;
}}
.timeline-step strong {{
    color: var(--text-primary) !important;
}}
.timeline-step span, .timeline-step div {{
    color: var(--text-secondary) !important;
}}

/* Monospace Report Container */
.report-box {{
    background: var(--code-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 16px;
    font-family: 'Courier New', monospace;
    font-size: 0.8rem;
    color: var(--code-text);
    white-space: pre;
    overflow-x: auto;
}}

/* Dynamic Theme Switcher Component in Sidebar */
.theme-switch-container {{
    display: flex;
    background: var(--surface-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
    margin-bottom: 16px;
}}
</style>
"""
    st.markdown(css_content, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar: Controls & Theme Selection
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🛡️ PhishGuard")
    st.caption("Forensic-grade phishing analysis — zero data leakage")

    # Dual-Theme Selector Switch
    st.markdown("##### 🎨 Interface Theme")
    theme_choice = st.radio(
        "Theme Mode",
        options=["System (Auto)", "🌙 Dark (Obsidian)", "☀️ Light (Titanium)"],
        index=0 if st.session_state.theme == "system" else (1 if st.session_state.theme == "dark" else 2),
        label_visibility="collapsed",
        horizontal=True
    )
    
    # Map selection back to state
    if "Dark" in theme_choice:
        st.session_state.theme = "dark"
    elif "Light" in theme_choice:
        st.session_state.theme = "light"
    else:
        st.session_state.theme = "system"

    st.markdown("""
    > **Built for Alex** 🎓
    >
    > Alex almost fell for a spear-phishing email quoting his real student ID and
    > tuition balance. He couldn't paste it into public AI out of privacy fear.
    >
    > PhishGuard runs locally or on private cloud — your data never leaves your control.
    """)

    st.markdown("---")
    st.markdown("### ⚙️ Analysis Settings")

    enable_pii = st.toggle(
        "🔒 Auto-Scrub PII",
        value=True,
        help="Masks credit cards, student IDs, phones, emails, and NRIC before any AI execution."
    )

    api_key = st.text_input(
        "🔑 Google AI Studio API Key",
        type="password",
        placeholder="AIza... (optional — enables Gemma 2 cloud mode)",
        help="Get a free key at https://aistudio.google.com/app/apikey — enables Gemma 2 9B model."
    )

    if api_key:
        st.success("✅ Gemma 2 cloud mode active")
    else:
        st.info("ℹ️ Running in offline heuristic mode")

    st.markdown("---")
    st.markdown("### 📦 Architecture")
    st.markdown("""
    - 🔬 **Engine:** Gemma 2 9B IT + 11-dim heuristics
    - 🔒 **Privacy Shield:** PII pre-scrubbed locally
    - 📄 **SOC Artifact:** Downloadable incident report
    - 🎨 **System:** Dual-theme semantic design token
    """)
    st.markdown(
        "[![GitHub](https://img.shields.io/badge/GitHub-Hao610%2Fphishguard--gemma-blue?logo=github)](https://github.com/Hao610/phishguard-gemma)"
    )
    st.caption("🏆 Hacktoberfest 2026 — Build for a Friend | Best Use of Gemma")

# Inject Dual Theme Engine
inject_dual_theme_engine(st.session_state.theme)

# ─────────────────────────────────────────────────────────────────────────────
# Engine instance
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_resource
def get_engine():
    return PhishGuardEngine()

engine = get_engine()

# ─────────────────────────────────────────────────────────────────────────────
# Sample Scenarios
# ─────────────────────────────────────────────────────────────────────────────

SCENARIOS = {
    "bank": {
        "label": "🚨 Bank Lockout Scam",
        "text": (
            "URGENT SECURITY ALERT — Wells Fargo\n\n"
            "Your online banking access has been LOCKED due to 3 failed login attempts "
            "from IP 45.33.32.156 (Russia). To prevent permanent account suspension and "
            "avoid legal escalation, you must verify your identity within 12 hours:\n\n"
            "http://wellsfarg0-secure.accountverify.xyz/login?ref=4111222233334444\n\n"
            "Account Security Dept | Case Ref: WF-2024-88491\n"
            "Failure to respond within the time frame will result in account termination."
        ),
    },
    "bursary": {
        "label": "🎓 Fake University Bursary",
        "text": (
            "Dear Student (ID: 2024-88491),\n\n"
            "Your emergency hardship grant of $1,250.00 has been approved by the "
            "Student Financial Aid Committee (SFAC). "
            "Please confirm your bank account details within 24 hours for immediate wire transfer:\n\n"
            "http://portal-bursary-edu.xyz/disbursement/confirm\n\n"
            "Office of the Registrar | Tel: +1-800-555-0199\n"
            "Action required immediately — funds will be forfeited if unclaimed."
        ),
    },
    "job": {
        "label": "⚠️ Unsolicited Recruiter (Verify Domain)",
        "text": (
            "Hi candidate,\n\n"
            "We reviewed your resume on LinkedIn and are pleased to invite you for an interview.\n\n"
            "Position: Senior DevOps Engineer\n"
            "Date: Tomorrow 15:00 UTC\n"
            "Meeting Portal: https://interview-portal.global-careers-hire.xyz/entry?token=9f82bc1a\n\n"
            "Please confirm your attendance by logging in above.\n"
            "Talent Acquisition Team"
        ),
    },
    "safe": {
        "label": "✅ Genuine Friend Message",
        "text": (
            "Hi Alex,\n\n"
            "Just following up on our project discussion from yesterday. "
            "I uploaded the presentation slides to our shared Google Drive folder — "
            "you should already have access.\n\n"
            "Let me know when you're free for a quick 15-minute sync before Friday's lab submission.\n\n"
            "Best,\nSarah (sarah.w@university.edu)"
        ),
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Main Header
# ─────────────────────────────────────────────────────────────────────────────

st.markdown('<div class="main-header">🛡️ PhishGuard: Zero-Leakage Threat Scanner</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Forensic-grade phishing analysis for non-technical users — '
    'your messages stay private, always.</div>',
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────────────────────────────────────
# Scenario Selector
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("##### ⚡ Load a Real-World Test Scenario:")
sc1, sc2, sc3, sc4 = st.columns(4)

if "current_text" not in st.session_state:
    st.session_state.current_text = SCENARIOS["bank"]["text"]

for col, key in zip([sc1, sc2, sc3, sc4], ["bank", "bursary", "job", "safe"]):
    if col.button(SCENARIOS[key]["label"], use_container_width=True):
        st.session_state.current_text = SCENARIOS[key]["text"]
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Input + Live IoC Panel
# ─────────────────────────────────────────────────────────────────────────────

col_left, col_right = st.columns([1.15, 0.85])

with col_left:
    st.markdown("#### 📥 Message Input")
    raw_input = st.text_area(
        "Paste email, SMS, or WhatsApp message to audit:",
        value=st.session_state.current_text,
        height=200,
        placeholder="Paste suspicious message here...",
        label_visibility="collapsed"
    )

    # PII handling
    final_text = raw_input
    pii_result = None
    if enable_pii and raw_input.strip():
        pii_result = engine.redact_pii(raw_input)
        final_text = pii_result["sanitized_text"]
        if pii_result["total_redacted"] > 0:
            st.success(
                f"🔒 **Privacy Shield Active** — {pii_result['total_redacted']} sensitive items scrubbed "
                f"({pii_result['stats']['emails']} emails, {pii_result['stats']['phones']} phones, "
                f"{pii_result['stats']['cards']} cards, {pii_result['stats']['ids']} IDs)"
            )

    run_btn = st.button(
        "🔍 **Run Forensic Audit**" + (" with Gemma 2" if api_key else " (Heuristic Mode)"),
        use_container_width=True,
        type="primary"
    )

with col_right:
    st.markdown("#### 🔗 Live Indicator of Compromise (IoC) Panel")
    live_ioc = engine.extract_indicators(raw_input) if raw_input.strip() else {}

    if live_ioc:
        urls = live_ioc.get("urls_detected", [])
        urgency = live_ioc.get("urgency_triggers", [])
        domains = live_ioc.get("suspicious_domains", [])
        ip_urls = live_ioc.get("ip_urls", [])
        shortened = live_ioc.get("shortened_urls", [])
        bad_tlds = live_ioc.get("suspicious_tlds", [])
        free_h = live_ioc.get("free_hosting", [])

        if urls:
            st.markdown("**🔗 Defanged URLs:**")
            for u in urls[:5]:
                st.code(engine.defang_url(u), language="text")
            if len(urls) > 5:
                st.caption(f"... and {len(urls) - 5} more")
        else:
            st.caption("✅ No embedded URLs detected")

        flags = []
        if urgency:
            flags.append(f"⏰ **Urgency language:** `{', '.join(urgency[:3])}`")
        if domains:
            for d in domains:
                flags.append(f"🎭 **Lookalike domain** impersonating {d['impersonates']}")
        if ip_urls:
            flags.append("⚠️ **Raw IP URL** — hides real destination")
        if shortened:
            flags.append("🔀 **URL shortener** — destination concealed")
        if bad_tlds:
            flags.append("🚩 **Suspicious TLD** detected")
        if free_h:
            flags.append("🏗️ **Free hosting** infrastructure")
        if live_ioc.get("authority_impersonation"):
            flags.append("🏛️ **Authority impersonation** (govt/law enforcement)")
        if live_ioc.get("attachment_references"):
            flags.append("📎 **Attachment reference** — possible malware vector")

        if flags:
            for f in flags:
                st.markdown(f)
        else:
            st.caption("✅ No active threat flags in current message")
    else:
        st.caption("Enter a message to see live IoC analysis")

# ─────────────────────────────────────────────────────────────────────────────
# Forensic Audit Results
# ─────────────────────────────────────────────────────────────────────────────

if run_btn and raw_input.strip():
    with st.spinner("Analyzing threat telemetry with forensic engine..."):
        time.sleep(0.3)
        result = engine.analyze(final_text, api_key=api_key)

    st.markdown("---")
    st.markdown("## 📊 Forensic Audit Results")

    verdict = result.get("verdict", "SAFE")
    score = result.get("threat_score", 0)
    confidence = result.get("confidence", "MEDIUM")
    attack_type = result.get("attack_type", "Unknown")
    model_used = result.get("_model_used", "Heuristic Engine")

    # ── Verdict Banner ────────────────────────────────────────────────────
    col_v, col_s, col_m = st.columns([1, 1.8, 1.2])

    with col_v:
        if verdict == "CRITICAL_PHISHING":
            st.markdown("""
            <div style="background:linear-gradient(135deg, rgba(239,68,68,0.15), rgba(185,28,28,0.25));
                        border:1px solid #ef4444; border-radius:12px; padding:18px; text-align:center;">
                <h3 style="margin:0; color:#ef4444;">🛑 CRITICAL</h3>
                <p style="margin:4px 0 0 0; color:#f87171; font-size:0.9rem;">High-confidence phishing</p>
            </div>
            """, unsafe_allow_html=True)
        elif verdict == "SUSPICIOUS":
            st.markdown("""
            <div style="background:linear-gradient(135deg, rgba(245,158,11,0.15), rgba(180,83,9,0.25));
                        border:1px solid #f59e0b; border-radius:12px; padding:18px; text-align:center;">
                <h3 style="margin:0; color:#f59e0b;">⚠️ SUSPICIOUS</h3>
                <p style="margin:4px 0 0 0; color:#fbbf24; font-size:0.9rem;">Proceed with caution</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:linear-gradient(135deg, rgba(16,185,129,0.15), rgba(4,120,87,0.25));
                        border:1px solid #10b981; border-radius:12px; padding:18px; text-align:center;">
                <h3 style="margin:0; color:#10b981;">✅ SAFE</h3>
                <p style="margin:4px 0 0 0; color:#34d399; font-size:0.9rem;">No threats detected</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"<br>**Attack Type:** `{attack_type}`", unsafe_allow_html=True)
        st.markdown(f"**Confidence:** `{confidence}`")
        st.caption(f"Analysis by: {model_used}")

    with col_s:
        # Determine theme-adaptive chart colors
        is_light = (st.session_state.theme == "light")
        paper_bg = "#f8fafc" if is_light else "#050507"
        meter_bg = "#ffffff" if is_light else "#0c0c12"
        border_c = "#cbd5e1" if is_light else "#27272a"
        num_c = "#0f172a" if is_light else "#ffffff"
        tick_c = "#64748b" if is_light else "#71717a"
        gauge_color = "#ef4444" if score >= 70 else ("#f59e0b" if score >= 40 else "#10b981")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Threat Index", "font": {"color": tick_c, "size": 14}},
            number={"font": {"color": num_c, "size": 36}, "suffix": "/100"},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": tick_c},
                "bar": {"color": gauge_color, "thickness": 0.25},
                "bgcolor": meter_bg,
                "bordercolor": border_c,
                "steps": [
                    {"range": [0, 40], "color": "#064e3b" if not is_light else "#dcfce7"},
                    {"range": [40, 70], "color": "#78350f" if not is_light else "#fef3c7"},
                    {"range": [70, 100], "color": "#7f1d1d" if not is_light else "#fee2e2"},
                ],
                "threshold": {
                    "line": {"color": gauge_color, "width": 3},
                    "thickness": 0.8,
                    "value": score,
                },
            },
        ))
        fig.update_layout(
            paper_bgcolor=paper_bg,
            plot_bgcolor=paper_bg,
            margin={"t": 40, "b": 10, "l": 20, "r": 20},
            height=200,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_m:
        st.markdown("#### 💡 Plain-English Summary")
        st.write(result.get("summary", ""))

    # ── Red Flags + Tactics ───────────────────────────────────────────────
    st.markdown("---")
    col_rf, col_tac = st.columns(2)

    with col_rf:
        st.markdown("#### 🚩 Specific Red Flags")
        for rf in result.get("red_flags", []):
            st.markdown(f"- 🔴 {rf}")

    with col_tac:
        st.markdown("#### 🎯 Attack Tactics Detected")
        for tactic in result.get("detected_tactics", []):
            tac_emoji = "✅" if tactic == "No Deceptive Tactics Detected" else "⚔️"
            st.markdown(f"- {tac_emoji} **{tactic}**")

    # ── Action Plan Timeline ──────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🛡️ Recommended Actions")
    action_cols = st.columns(min(len(result.get("safe_action_plan", [])), 3))
    for idx, (col, step) in enumerate(zip(action_cols, result.get("safe_action_plan", []))):
        with col:
            st.markdown(f"""
            <div class="timeline-step">
                <strong>Step {idx+1}</strong><br>
                <span>{step}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Incident Report ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📄 Formal Incident Report")
    st.caption(
        "Submit this report to your organization's IT Security team or Security Operations Center (SOC). "
        "All URLs are defanged to prevent accidental clicks."
    )

    dl_col, prev_col = st.columns([1, 2])
    with dl_col:
        st.download_button(
            label="📥 Download Incident Report (.txt)",
            data=result.get("incident_report", ""),
            file_name="phishguard_incident_report.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with prev_col:
        with st.expander("🔍 Preview Report", expanded=False):
            st.code(result.get("incident_report", ""), language="text")

elif run_btn and not raw_input.strip():
    st.warning("⚠️ Please paste a message to audit first.")

# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:var(--text-muted); font-size:0.8rem;'>"
    "🛡️ PhishGuard — Open source, privacy-first forensic phishing analysis | "
    "<a href='https://github.com/Hao610/phishguard-gemma' style='color:#38bdf8'>GitHub</a> | "
    "Powered by Google Gemma 2 Open Weights Architecture"
    "</div>",
    unsafe_allow_html=True
)

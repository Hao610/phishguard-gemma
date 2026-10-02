"""
PhishGuard — Zero-Leakage Threat Scanner
Built for a Friend (Alex) | Hacktoberfest 2026
Powered by Google Gemma 2 Open-Source AI
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
# Styling
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Dark cyber theme */
    .stApp { background-color: #080d1a; }

    .main-header {
        font-size: 2.4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 24px;
    }

    /* Verdict badges */
    .verdict-safe {
        background: linear-gradient(135deg, #064e3b, #065f46);
        border: 1px solid #10b981;
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
    }
    .verdict-suspicious {
        background: linear-gradient(135deg, #451a03, #78350f);
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
    }
    .verdict-critical {
        background: linear-gradient(135deg, #450a0a, #7f1d1d);
        border: 1px solid #ef4444;
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
    }

    /* IoC panel */
    .ioc-panel {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 10px;
    }

    /* Monospace report box */
    .report-box {
        background: #020817;
        border: 1px solid #1e3a5f;
        border-radius: 8px;
        padding: 16px;
        font-family: 'Courier New', monospace;
        font-size: 0.78rem;
        color: #38bdf8;
        white-space: pre;
        overflow-x: auto;
    }

    /* Timeline step */
    .timeline-step {
        border-left: 2px solid #3b82f6;
        padding-left: 14px;
        margin-bottom: 12px;
    }

    /* Scenario buttons */
    div[data-testid="column"] .stButton > button {
        border-radius: 8px;
        font-size: 0.88rem;
        padding: 10px;
        transition: all 0.2s;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Engine instance
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_resource
def get_engine():
    return PhishGuardEngine()

engine = get_engine()

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🛡️ PhishGuard")
    st.caption("*Forensic-grade phishing analysis — zero data leakage*")

    st.markdown("""
    > **Built for Alex** 🎓
    >
    > Alex almost fell for a spear-phishing email that quoted his real student ID and
    > tuition balance. He couldn't paste it into ChatGPT out of privacy fear.
    >
    > PhishGuard runs locally or on a private cloud — your messages never leave your control.
    """)

    st.markdown("---")
    st.markdown("### ⚙️ Analysis Settings")

    enable_pii = st.toggle(
        "🔒 Auto-Scrub PII",
        value=True,
        help="Masks credit cards, student IDs, phones, emails, and NRIC before any API call."
    )

    api_key = st.text_input(
        "🔑 Google AI Studio API Key",
        type="password",
        placeholder="AIza... (optional — enables Gemma 2 cloud mode)",
        help="Get a free key at https://aistudio.google.com/app/apikey — enables Gemma 2 9B analysis."
    )

    if api_key:
        st.success("✅ Gemma 2 cloud mode active")
    else:
        st.info("ℹ️ Running in offline heuristic mode")

    st.markdown("---")
    st.markdown("### 📦 About")
    st.markdown("""
    - 🔬 **Engine:** Gemma 2 9B IT + 11-dim heuristics
    - 🔒 **Privacy:** PII scrubbed before any API call
    - 📄 **Output:** Downloadable forensic incident report
    - 🚀 **Deploy:** One-click via Render
    """)
    st.markdown(
        "[![GitHub](https://img.shields.io/badge/GitHub-Hao610%2Fphishguard--gemma-blue?logo=github)](https://github.com/Hao610/phishguard-gemma)"
    )
    st.caption("🏆 Hacktoberfest 2026 — Build for a Friend | Best Use of Gemma")

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
        "label": "💼 Fake Job Interview",
        "text": (
            "Hi LOI CHIANG HAO,\n\n"
            "Please find below your interview details:\n\n"
            "Position: SRE Engineer (DevOps) — Fresh Graduate\n"
            "Interview Date: 2026-10-01 17:00 (UTC+08:00)\n"
            "Video URL: https://interview.antgroup.com/home/entry?token=695a4c5f-e440-409f-bf2c-c420555e3ea9\n\n"
            "For concerns contact: WONG See Khee | seekhee.w@ant-intl.com | 010-58178688\n\n"
            "This is a system email, please do not reply.\n"
            "Ant Group — Campus Recruitment Department"
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

st.markdown("---")

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
        else:
            st.caption("🔒 Privacy shield active — no PII found in this message")

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
            flags.append(f"⚠️ **Raw IP URL** — hides real destination")
        if shortened:
            flags.append(f"🔀 **URL shortener** — destination concealed")
        if bad_tlds:
            flags.append(f"🚩 **Suspicious TLD** detected")
        if free_h:
            flags.append(f"🏗️ **Free hosting** infrastructure")
        if live_ioc.get("authority_impersonation"):
            flags.append(f"🏛️ **Authority impersonation** (govt/law enforcement)")
        if live_ioc.get("attachment_references"):
            flags.append(f"📎 **Attachment reference** — possible malware vector")

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
    with st.spinner("Analyzing threat telemetry..."):
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
            st.markdown('<div class="verdict-critical">', unsafe_allow_html=True)
            st.error("### 🛑 CRITICAL")
            st.markdown("**High-confidence phishing**")
        elif verdict == "SUSPICIOUS":
            st.markdown('<div class="verdict-suspicious">', unsafe_allow_html=True)
            st.warning("### ⚠️ SUSPICIOUS")
            st.markdown("**Proceed with caution**")
        else:
            st.markdown('<div class="verdict-safe">', unsafe_allow_html=True)
            st.success("### ✅ SAFE")
            st.markdown("**No threats detected**")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"**Attack Type:** `{attack_type}`")
        st.markdown(f"**Confidence:** `{confidence}`")
        st.caption(f"Analysis by: {model_used}")

    with col_s:
        # Threat gauge chart
        gauge_color = "#ef4444" if score >= 70 else "#f59e0b" if score >= 40 else "#10b981"
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Threat Index", "font": {"color": "#94a3b8", "size": 14}},
            number={"font": {"color": "white", "size": 36}, "suffix": "/100"},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#475569"},
                "bar": {"color": gauge_color, "thickness": 0.25},
                "bgcolor": "#0f172a",
                "bordercolor": "#1e293b",
                "steps": [
                    {"range": [0, 40], "color": "#052e16"},
                    {"range": [40, 70], "color": "#422006"},
                    {"range": [70, 100], "color": "#450a0a"},
                ],
                "threshold": {
                    "line": {"color": gauge_color, "width": 3},
                    "thickness": 0.8,
                    "value": score,
                },
            },
        ))
        fig.update_layout(
            paper_bgcolor="#080d1a",
            plot_bgcolor="#080d1a",
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
            {step}
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
        with st.expander("🔍 Preview Report", expanded=(verdict == "CRITICAL_PHISHING")):
            st.code(result.get("incident_report", ""), language="text")

elif run_btn and not raw_input.strip():
    st.warning("⚠️ Please paste a message to audit first.")

# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#334155; font-size:0.8rem;'>"
    "🛡️ PhishGuard — Open source, privacy-first forensic phishing analysis | "
    "<a href='https://github.com/Hao610/phishguard-gemma' style='color:#3b82f6'>GitHub</a> | "
    "Powered by Google Gemma 2 Open Weights"
    "</div>",
    unsafe_allow_html=True
)

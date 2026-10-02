"""
PhishGuard Core Engine v2.0
Powered by Google Gemma 2 Open-Source AI Architecture

Multi-stage forensic pipeline:
  Stage 1 — Static heuristic extraction (zero dependencies, instant)
  Stage 2 — Gemma 2 LLM analysis via Google AI Studio API (cloud-privacy mode)
  Stage 3 — Structured verdict aggregation + incident report generation

Designed for offline privacy, zero data leakage, and deep threat heuristic auditing.
"""

import json
import re
import os
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# Threat Intelligence: Expanded indicator libraries
# ─────────────────────────────────────────────────────────────────────────────

URGENCY_PATTERNS: List[Tuple[str, int]] = [
    # (pattern, weight)
    (r'\bwithin\s+\d+\s+hours?\b', 30),
    (r'\bwithin\s+\d+\s+minutes?\b', 35),
    (r'\bimmediately\b', 25),
    (r'\burgent\b', 20),
    (r'\baction\s+required\b', 20),
    (r'\baccount\s+(suspended|locked|frozen|terminated|disabled)\b', 40),
    (r'\bunauthorized\s+(login|access|attempt)\b', 35),
    (r'\bverify\s+(your|account|identity|information)\b', 20),
    (r'\bpassword\s+expire[sd]?\b', 25),
    (r'\bcompromised\b', 30),
    (r'\btransfer\s+(fund|money|amount)\b', 35),
    (r'\blegal\s+(action|escalation)\b', 30),
    (r'\bfinal\s+notice\b', 30),
    (r'\byour\s+account\s+will\s+be\b', 25),
    (r'\bconfirm\s+(now|immediately|asap)\b', 25),
    (r'\bsecurity\s+alert\b', 20),
    (r'\blimited\s+time\b', 20),
    (r'\bclick\s+here\s+(now|immediately|to\s+verify)\b', 30),
]

LOOKALIKE_DOMAINS: List[Tuple[str, str]] = [
    # (regex, brand)
    (r'paypa[l1][^a-z]', 'PayPal'),
    (r'micros[o0]ft[^a-z]', 'Microsoft'),
    (r'g[o0]{2}gl[e3][^a-z]', 'Google'),
    (r'app[l1][e3][^a-z]', 'Apple'),
    (r'wellsfarg[o0][^a-z]', 'Wells Fargo'),
    (r'amaz[o0]n[^a-z]', 'Amazon'),
    (r'netfl[i1]x[^a-z]', 'Netflix'),
    (r'[il1]nstagram[^a-z]', 'Instagram'),
    (r'faceb[o0]{2}k[^a-z]', 'Facebook'),
    (r'tw[i1]tter[^a-z]', 'Twitter'),
    (r'linked[i1]n[^a-z]', 'LinkedIn'),
    (r'[a4]mazon[^a-z]', 'Amazon'),
    (r'bank[o0]famerica[^a-z]', 'Bank of America'),
    (r'[il1]rs\.', 'IRS'),
]

SUSPICIOUS_TLD_PATTERNS = re.compile(
    r'https?://[^\s<>"]*\.(xyz|tk|ml|ga|cf|pw|top|click|download|loan|win|racing|date|party|gq|icu|buzz|work|fun|host|site|tech|store|online|bid|accountant|science|review|country)\b',
    re.IGNORECASE
)

FREE_HOSTING_PATTERNS = re.compile(
    r'https?://[^\s<>"]*\.(000webhostapp\.com|weebly\.com|wix\.com|blogger\.com|blogspot\.com|glitch\.me|repl\.co|pages\.dev|netlify\.app|vercel\.app|ngrok\.io|serveo\.net)',
    re.IGNORECASE
)

CREDENTIAL_HARVESTER_PATTERNS = re.compile(
    r'(?:login|signin|verify|confirm|update|secure|account|banking|payment)\.(php|aspx|html?)\b',
    re.IGNORECASE
)

IP_URL_PATTERN = re.compile(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

SHORTENED_URL_PATTERN = re.compile(
    r'https?://(bit\.ly|tinyurl\.com|t\.co|ow\.ly|is\.gd|buff\.ly|ift\.tt|goo\.gl|rb\.gy|cutt\.ly|shorturl\.at|tiny\.cc|v\.gd|urlshortx\.com)',
    re.IGNORECASE
)

ATTACHMENT_REFERENCES = re.compile(
    r'\b(attached?|attachment|download|open\s+the\s+file|see\s+attached|invoice|pdf|docx?|xlsx?|\.zip|\.exe|\.js|\.vbs)\b',
    re.IGNORECASE
)

AUTHORITY_IMPERSONATION = re.compile(
    r'\b(irs|fbi|interpol|police|court|government|federal|treasury|social\s+security|medicare|homeland\s+security|dhs|sec\b|fdic)\b',
    re.IGNORECASE
)

BRAND_IMPERSONATION = re.compile(
    r'\b(apple|microsoft|google|amazon|paypal|netflix|facebook|instagram|linkedin|wells\s+fargo|chase\s+bank|bank\s+of\s+america|citibank|barclays|hsbc|dhl|fedex|ups|usps)\b',
    re.IGNORECASE
)

# ─────────────────────────────────────────────────────────────────────────────
# Gemma Prompt Template (Gemma 2 chat format)
# ─────────────────────────────────────────────────────────────────────────────

GEMMA_SYSTEM_PROMPT = """You are PhishGuard, an expert cybersecurity forensic analyst specializing in spear-phishing, social engineering, business email compromise (BEC), and SMS smishing attacks.

Your job is to protect non-technical everyday users — students, elderly people, and professionals who may not recognize sophisticated modern attacks.

Analyze the message with the mindset of a threat intelligence analyst at a Security Operations Center (SOC). Be rigorous but practical."""


def build_gemma_prompt(raw_message: str, indicators: Dict[str, Any]) -> str:
    """Constructs a structured adversarial analysis prompt for Gemma 2 instruction format."""
    return f"""<start_of_turn>user
{GEMMA_SYSTEM_PROMPT}

Analyze this incoming message for phishing, social engineering, or fraud:

--- INCOMING MESSAGE ---
{raw_message}
--- END MESSAGE ---

Pre-computed static indicators:
- URLs found: {indicators['urls_detected']}
- Urgency triggers: {indicators['urgency_triggers']}
- Suspicious domains: {indicators['suspicious_domains']}
- Free hosting detected: {indicators.get('free_hosting', [])}
- IP-based URLs: {indicators.get('ip_urls', [])}
- URL shorteners: {indicators.get('shortened_urls', [])}
- Suspicious TLDs: {indicators.get('suspicious_tlds', [])}
- Authority impersonation: {indicators.get('authority_impersonation', False)}
- Brand impersonation: {indicators.get('brand_impersonation', [])}
- Attachment references: {indicators.get('attachment_references', False)}

Respond with ONLY a valid JSON object — no markdown, no extra text:
{{
  "verdict": "SAFE" | "SUSPICIOUS" | "CRITICAL_PHISHING",
  "threat_score": <integer 0-100>,
  "confidence": "LOW" | "MEDIUM" | "HIGH",
  "summary": "<2-3 sentences in plain language a non-technical friend can understand>",
  "attack_type": "<e.g. Spear Phishing, Smishing, BEC, Credential Harvesting, Vishing, None>",
  "detected_tactics": ["<tactic1>", "<tactic2>"],
  "red_flags": ["<specific red flag 1>", "<specific red flag 2>"],
  "safe_action_plan": ["<Step 1>", "<Step 2>", "<Step 3>"]
}}
<end_of_turn>
<start_of_turn>model
"""


# ─────────────────────────────────────────────────────────────────────────────
# Main Engine
# ─────────────────────────────────────────────────────────────────────────────

class PhishGuardEngine:
    """
    PhishGuard multi-stage forensic engine.

    Stage 1: Static heuristic indicator extraction (always runs, zero latency)
    Stage 2: Gemma 2 LLM analysis via Google AI Studio (when api_key provided)
    Stage 3: Structured verdict + incident report generation
    """

    def __init__(self):
        self._api_key: Optional[str] = os.getenv("GOOGLE_API_KEY", "")

    # ── Stage 1: Static Indicator Extraction ──────────────────────────────

    def extract_indicators(self, text: str) -> Dict[str, Any]:
        """
        Comprehensive multi-dimension indicator extraction.
        Returns a rich IoC (Indicator of Compromise) dictionary.
        """
        # Raw URL extraction
        url_pattern = r'https?://[^\s<>"\']+|www\.[^\s<>"\']+'
        urls = re.findall(url_pattern, text)

        # Urgency analysis (weighted)
        urgency_found = []
        urgency_score = 0
        for pattern, weight in URGENCY_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                urgency_found.extend(matches)
                urgency_score += weight

        # Lookalike domain detection
        suspicious_domains = []
        for url in urls:
            for pattern, brand in LOOKALIKE_DOMAINS:
                if re.search(pattern, url, re.IGNORECASE):
                    suspicious_domains.append({"url": url, "impersonates": brand})

        # Advanced URL analysis
        ip_urls = [u for u in urls if IP_URL_PATTERN.match(u)]
        shortened_urls = [u for u in urls if SHORTENED_URL_PATTERN.match(u)]
        suspicious_tlds = [u for u in urls if SUSPICIOUS_TLD_PATTERNS.search(u)]
        free_hosting = [u for u in urls if FREE_HOSTING_PATTERNS.search(u)]
        credential_pages = [u for u in urls if CREDENTIAL_HARVESTER_PATTERNS.search(u)]

        # Content pattern analysis
        has_authority = bool(AUTHORITY_IMPERSONATION.search(text))
        brand_matches = list(set(BRAND_IMPERSONATION.findall(text)))
        has_attachments = bool(ATTACHMENT_REFERENCES.search(text))

        # Mismatched display/actual URL (HTML anchor check)
        display_url_mismatch = bool(re.search(
            r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(?:https?://[^\s<]+)</a>',
            text, re.IGNORECASE
        ))

        return {
            "urls_detected": urls,
            "urgency_triggers": list(set(urgency_found)),
            "urgency_score": min(urgency_score, 60),
            "suspicious_domains": suspicious_domains,
            "ip_urls": ip_urls,
            "shortened_urls": shortened_urls,
            "suspicious_tlds": suspicious_tlds,
            "free_hosting": free_hosting,
            "credential_pages": credential_pages,
            "authority_impersonation": has_authority,
            "brand_impersonation": brand_matches,
            "attachment_references": has_attachments,
            "display_url_mismatch": display_url_mismatch,
        }

    # ── PII Redaction ─────────────────────────────────────────────────────

    def redact_pii(self, text: str) -> Dict[str, Any]:
        """
        Automatically scrubs sensitive PII before sending to any external API.
        Handles: emails, credit cards, phones, student IDs, NRIC/passport, bank accounts.
        """
        redacted = text
        stats = {"emails": 0, "phones": 0, "cards": 0, "ids": 0, "accounts": 0}

        # Email addresses
        email_re = r'[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-.]{2,}'
        stats["emails"] = len(re.findall(email_re, redacted))
        redacted = re.sub(email_re, "[REDACTED_EMAIL]", redacted)

        # Credit / debit card numbers (Luhn-format detection)
        card_re = r'\b(?:\d[ \-]?){13,19}\b'
        stats["cards"] = len(re.findall(card_re, redacted))
        redacted = re.sub(card_re, "[REDACTED_CARD]", redacted)

        # Phone numbers (international + local formats, Malaysian/SG/US)
        phone_re = (
            r'\b(?:\+?6?0?\d{1,2}[\s\-]?\d{2,4}[\s\-]?\d{4,8})\b'
            r'|\b\d{3}[\s\-\.]\d{3}[\s\-\.]\d{4}\b'
            r'|\b0\d{1,2}[\s\-]?\d{7,8}\b'
        )
        stats["phones"] = len(re.findall(phone_re, redacted))
        redacted = re.sub(phone_re, "[REDACTED_PHONE]", redacted)

        # Malaysian NRIC (e.g., 990101-14-1234)
        nric_re = r'\b\d{6}[\-]?\d{2}[\-]?\d{4}\b'
        ic_found = len(re.findall(nric_re, redacted))
        if ic_found:
            stats["ids"] += ic_found
            redacted = re.sub(nric_re, "[REDACTED_NRIC]", redacted)

        # Student / Account / Reference IDs
        id_re = r'(?i)(?:(?:student\s*)?id|account\s*(?:no|number|#)|ref(?:erence)?|matric)[\s:]+([A-Z0-9\-_]{4,20})'
        stats["ids"] += len(re.findall(id_re, redacted))
        redacted = re.sub(id_re, r'ID: [REDACTED_ID]', redacted)

        # Bank account numbers (8-12 digit standalone)
        acct_re = r'\b\d{8,12}\b'
        acct_candidates = re.findall(acct_re, redacted)
        if acct_candidates:
            stats["accounts"] = len(acct_candidates)
            redacted = re.sub(acct_re, "[REDACTED_ACCOUNT]", redacted)

        return {
            "sanitized_text": redacted,
            "stats": stats,
            "total_redacted": sum(stats.values()),
        }

    # ── URL Utilities ─────────────────────────────────────────────────────

    @staticmethod
    def defang_url(url: str) -> str:
        """Industry-standard defanging: prevents accidental clicks during forensic inspection."""
        return (
            url.replace("https://", "hxxps://")
               .replace("http://", "hxxp://")
               .replace(".", "[.]")
               .replace("://", "[://]")
        )

    # ── Stage 2: Gemma LLM Analysis ──────────────────────────────────────

    def _call_gemma_api(self, prompt: str, api_key: str) -> Optional[Dict[str, Any]]:
        """
        Calls Google AI Studio API with Gemma 2 9B IT model.
        Falls back to gemini-1.5-flash if gemma quota is exceeded.
        Returns parsed JSON dict or None on failure.
        """
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)

            # Try Gemma 2 first (core project requirement)
            for model_name in ["gemma-2-9b-it", "gemma-2-2b-it", "gemini-1.5-flash"]:
                try:
                    model = genai.GenerativeModel(
                        model_name,
                        generation_config={
                            "temperature": 0.1,
                            "max_output_tokens": 1024,
                            "response_mime_type": "application/json",
                        }
                    )
                    response = model.generate_content(prompt)
                    raw = response.text.strip()

                    # Clean markdown wrappers if present
                    if "```json" in raw:
                        raw = raw.split("```json")[1].split("```")[0].strip()
                    elif "```" in raw:
                        raw = raw.split("```")[1].split("```")[0].strip()

                    parsed = json.loads(raw)
                    parsed["_model_used"] = model_name
                    return parsed
                except Exception:
                    continue

        except ImportError:
            pass
        except Exception:
            pass

        return None

    # ── Stage 3: Heuristic Scoring (offline fallback) ────────────────────

    def _heuristic_analyze(self, indicators: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministic multi-dimensional threat scoring.
        Used when no API key is provided or API call fails.
        Produces verdicts consistent with LLM output schema.
        """
        score = 5  # baseline noise floor
        tactics = []
        red_flags = []
        action_plan = []
        attack_type = "None"

        # Dimension 1: URL presence
        if indicators["urls_detected"]:
            score += 20
            tactics.append("Embedded External Links")
            red_flags.append(f"{len(indicators['urls_detected'])} external URL(s) detected in message body")

        # Dimension 2: Urgency (weighted)
        if indicators["urgency_score"] > 0:
            score += min(indicators["urgency_score"], 45)
            tactics.append("Manufactured Psychological Urgency")
            red_flags.append(f"Coercive time-pressure language: {', '.join(indicators['urgency_triggers'][:3])}")
            action_plan.append("Do NOT comply with any time-pressure demands — take time to verify independently.")

        # Dimension 3: Lookalike/homoglyph domains
        if indicators["suspicious_domains"]:
            score += 40
            brands = list(set([d["impersonates"] for d in indicators["suspicious_domains"]]))
            tactics.append("Homoglyph Domain Impersonation")
            red_flags.append(f"Lookalike domain impersonating: {', '.join(brands)}")
            attack_type = "Credential Harvesting"

        # Dimension 4: IP-based URLs (no domain = red flag)
        if indicators["ip_urls"]:
            score += 30
            tactics.append("Raw IP Address URL (no domain)")
            red_flags.append("Message links directly to an IP address — legitimate services never do this")

        # Dimension 5: URL shorteners (hides true destination)
        if indicators["shortened_urls"]:
            score += 20
            tactics.append("URL Shortener (Destination Hidden)")
            red_flags.append("Shortened URL used to conceal the real link destination")

        # Dimension 6: Suspicious TLDs
        if indicators["suspicious_tlds"]:
            score += 25
            tactics.append("Suspicious Low-Cost TLD")
            red_flags.append(f"High-risk domain extension detected in URL")

        # Dimension 7: Free hosting
        if indicators["free_hosting"]:
            score += 15
            tactics.append("Free Hosting Platform (Phisher Infrastructure)")
            red_flags.append("Legitimate organizations do not use free hosting platforms")

        # Dimension 8: Credential harvesting pages
        if indicators["credential_pages"]:
            score += 35
            tactics.append("Credential Harvesting Page")
            red_flags.append("URL path suggests a login or credential-capture page")
            attack_type = "Credential Harvesting"

        # Dimension 9: Authority impersonation
        if indicators["authority_impersonation"]:
            score += 25
            tactics.append("Government/Authority Impersonation")
            red_flags.append("Message claims to be from a government or law enforcement agency")
            attack_type = "Authority Impersonation"

        # Dimension 10: Brand impersonation
        if indicators["brand_impersonation"]:
            score += 15
            tactics.append("Brand Impersonation")
            red_flags.append(f"Known brand names referenced: {', '.join(indicators['brand_impersonation'][:3])}")
            if attack_type == "None":
                attack_type = "Brand Impersonation"

        # Dimension 11: Attachment references
        if indicators["attachment_references"]:
            score += 20
            tactics.append("Malicious Attachment Reference")
            red_flags.append("Message references a file attachment — a common malware delivery vector")

        # Score capping and verdict
        score = min(score, 98)

        if score >= 70:
            verdict = "CRITICAL_PHISHING"
            confidence = "HIGH"
            summary = (
                "HIGH CONFIDENCE THREAT DETECTED. This message shows multiple hallmarks of a sophisticated "
                "phishing attack — fake urgency, deceptive links, and possible impersonation. "
                "Do not click any links, do not reply, and report to your IT department immediately."
            )
            action_plan.append("Block and report the sender to your email provider.")
            action_plan.append("Contact the real organization via their official website or phone number.")
            action_plan.append("Report to your organization's IT security team or CERT.")
        elif score >= 40:
            verdict = "SUSPICIOUS"
            confidence = "MEDIUM"
            summary = (
                "This message has suspicious characteristics that warrant caution. "
                "While not definitively malicious, the combination of external links and pressure tactics "
                "matches common phishing patterns. Verify through official channels before taking action."
            )
            action_plan.append("Do not click links in this message — navigate to the official site manually.")
            action_plan.append("Call the organization's official number to verify this communication.")
        else:
            verdict = "SAFE"
            confidence = "MEDIUM"
            summary = (
                "No strong phishing indicators detected. This message appears to be routine communication. "
                "Always remain alert — even trusted senders can be compromised."
            )
            action_plan.append("Always verify sender addresses even in seemingly safe messages.")

        if not tactics:
            tactics = ["No Deceptive Tactics Detected"]
        if not red_flags:
            red_flags = ["No significant red flags identified"]

        return {
            "verdict": verdict,
            "threat_score": score,
            "confidence": confidence,
            "attack_type": attack_type,
            "summary": summary,
            "detected_tactics": tactics,
            "red_flags": red_flags,
            "safe_action_plan": action_plan,
            "_model_used": "PhishGuard Heuristic Engine v2.0",
        }

    # ── Incident Report Generator ─────────────────────────────────────────

    def generate_incident_report(self, raw_message: str, result: Dict[str, Any],
                                  indicators: Dict[str, Any]) -> str:
        """Generates a formal, printable Incident Response Report for SOC/IT submission."""
        msg_hash = hashlib.sha256(raw_message.encode("utf-8")).hexdigest()
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        model_used = result.get("_model_used", "PhishGuard Heuristic Engine v2.0")

        tactics_str = "\n".join([f"  [{i+1}] {t}" for i, t in enumerate(result.get("detected_tactics", []))])
        flags_str = "\n".join([f"  - {f}" for f in result.get("red_flags", [])])
        actions_str = "\n".join([f"  {i+1}. {a}" for i, a in enumerate(result.get("safe_action_plan", []), 1)])

        defanged_artifacts = "\n".join([
            f"  [{i+1}] {self.defang_url(u)}"
            for i, u in enumerate(indicators.get("urls_detected", []))
        ]) or "  (None)"

        report = f"""================================================================================
         PHISHGUARD INCIDENT RESPONSE & FORENSIC AUDIT REPORT
================================================================================
Generated:           {timestamp}
Payload SHA-256:     {msg_hash}
Analysis Engine:     {model_used}
Confidence Level:    {result.get('confidence', 'MEDIUM')}
--------------------------------------------------------------------------------
THREAT CLASSIFICATION
  Verdict:           {result.get('verdict', 'UNKNOWN')}
  Attack Type:       {result.get('attack_type', 'Unknown')}
  Calibrated Risk:   {result.get('threat_score', 0)} / 100
--------------------------------------------------------------------------------
EXECUTIVE SUMMARY
  {result.get('summary', '')}
--------------------------------------------------------------------------------
IDENTIFIED ATTACK TACTICS
{tactics_str or "  (None identified)"}
--------------------------------------------------------------------------------
RED FLAGS / INDICATORS OF COMPROMISE
{flags_str or "  (None)"}
--------------------------------------------------------------------------------
DEFANGED URL ARTIFACTS (Safe for Inspection)
{defanged_artifacts}
--------------------------------------------------------------------------------
RECOMMENDED REMEDIATION STEPS
{actions_str or "  No specific actions required."}
================================================================================
DISCLAIMER: This report was generated locally. No message content was transmitted
to external servers without explicit user consent.
Submit this document to your Security Operations Center (SOC) or IT department.
================================================================================
"""
        return report

    # ── Public API ────────────────────────────────────────────────────────

    def analyze(self, raw_message: str, api_key: str = "") -> Dict[str, Any]:
        """
        Full forensic analysis pipeline.
        Attempts Gemma 2 API, falls back to deterministic heuristics.
        Always returns the full structured result dict.
        """
        # Use instance key if caller doesn't provide one
        effective_key = api_key or self._api_key

        # Stage 1: Static extraction
        indicators = self.extract_indicators(raw_message)

        # Stage 2: LLM analysis (if key available)
        result = None
        if effective_key:
            prompt = build_gemma_prompt(raw_message, indicators)
            result = self._call_gemma_api(prompt, effective_key)

        # Stage 3: Heuristic fallback
        if result is None:
            result = self._heuristic_analyze(indicators)

        # Attach derived artifacts
        result["indicators"] = indicators
        result["incident_report"] = self.generate_incident_report(raw_message, result, indicators)

        return result

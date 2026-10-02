"""
PhishGuard Automated Test Suite v2.0
Tests the multi-stage forensic engine against known-good and known-bad samples.
"""

import pytest
from engine import PhishGuardEngine
from parser import MailParser


@pytest.fixture
def engine():
    return PhishGuardEngine()


# ── Verdict Tests ──────────────────────────────────────────────────────────

def test_bank_phishing_critical(engine):
    """High-confidence phishing: urgency + lookalike domain + suspicious TLD"""
    sample = (
        "URGENT: Your Wells Fargo account is locked. "
        "Verify your credentials within 12 hours: "
        "http://wellsfarg0-secure.accountverify.xyz/login"
    )
    result = engine.analyze(sample)
    assert result["verdict"] in ["SUSPICIOUS", "CRITICAL_PHISHING"]
    assert result["threat_score"] >= 60
    assert "detected_tactics" in result
    assert len(result["detected_tactics"]) >= 1


def test_credential_harvesting_detection(engine):
    """Credential harvesting: suspicious TLD + login page path"""
    sample = "Please update your details: http://portal-bursary-edu.xyz/login.php?id=2024"
    result = engine.analyze(sample)
    assert result["verdict"] in ["SUSPICIOUS", "CRITICAL_PHISHING"]
    assert result["threat_score"] >= 40


def test_legitimate_email_safe(engine):
    """Clean transactional message with no threat indicators"""
    sample = (
        "Hi Alex, just checking if you have time for our weekly sync tomorrow at 3pm. "
        "No rush, let me know. Thanks, Dave."
    )
    result = engine.analyze(sample)
    assert result["verdict"] == "SAFE"
    assert result["threat_score"] <= 35


def test_ip_url_detection(engine):
    """IP-based URL is a strong phishing signal"""
    sample = "Click to verify your account: http://192.168.1.55/secure/verify"
    result = engine.analyze(sample)
    ioc = result["indicators"]
    assert len(ioc["ip_urls"]) >= 1
    assert result["threat_score"] >= 40


def test_shortened_url_detection(engine):
    """URL shorteners used to hide phishing destinations"""
    sample = "Your package is ready. Track it here: https://bit.ly/3xFakeLink"
    result = engine.analyze(sample)
    ioc = result["indicators"]
    assert len(ioc["shortened_urls"]) >= 1


# ── PII Redaction Tests ────────────────────────────────────────────────────

def test_pii_redaction_phone_card_email(engine):
    """Core PII types are fully redacted"""
    sample = "My phone is 555-123-4567 and card is 4111-2222-3333-4444. Email: test@uni.edu"
    result = engine.redact_pii(sample)
    assert "[REDACTED_PHONE]" in result["sanitized_text"]
    assert "[REDACTED_CARD]" in result["sanitized_text"]
    assert "[REDACTED_EMAIL]" in result["sanitized_text"]
    assert result["stats"]["emails"] == 1
    assert result["stats"]["cards"] == 1
    assert result["total_redacted"] >= 3


def test_pii_redaction_preserves_safe_content(engine):
    """PII redaction does not corrupt non-PII content"""
    sample = "Meeting scheduled for 3pm tomorrow in Room 204."
    result = engine.redact_pii(sample)
    assert "Meeting scheduled" in result["sanitized_text"]
    assert result["total_redacted"] == 0


# ── URL Utilities ──────────────────────────────────────────────────────────

def test_url_defanging_http(engine):
    """Standard http defanging"""
    assert engine.defang_url("http://evil.com") == "hxxp[://]evil[.]com"


def test_url_defanging_https(engine):
    """Standard https defanging"""
    defanged = engine.defang_url("https://phishing-site.xyz")
    assert "hxxps" in defanged
    assert "[.]" in defanged
    assert "https" not in defanged


# ── IoC Extraction Tests ───────────────────────────────────────────────────

def test_ioc_extracts_all_dimensions(engine):
    """Full IoC extraction returns all expected keys"""
    sample = "URGENT: verify your PayPal at http://paypa1-secure.tk/login immediately"
    ioc = engine.extract_indicators(sample)
    assert "urls_detected" in ioc
    assert "urgency_triggers" in ioc
    assert "suspicious_domains" in ioc
    assert "ip_urls" in ioc
    assert "shortened_urls" in ioc
    assert "suspicious_tlds" in ioc
    assert "authority_impersonation" in ioc
    assert "brand_impersonation" in ioc
    assert "attachment_references" in ioc


# ── Incident Report Tests ──────────────────────────────────────────────────

def test_incident_report_contains_hash(engine):
    """Incident report must contain SHA-256 payload hash"""
    sample = "Test message for hashing"
    result = engine.analyze(sample)
    report = result.get("incident_report", "")
    assert "SHA-256" in report
    assert len(report) > 200


def test_incident_report_defangs_urls(engine):
    """URLs in incident report must be defanged"""
    sample = "Click: http://evil-phishing.xyz/steal"
    result = engine.analyze(sample)
    report = result.get("incident_report", "")
    assert "hxxp" in report
    assert "http://evil" not in report


# ── EML Parser Tests ───────────────────────────────────────────────────────

def test_eml_parser_extracts_headers():
    raw_eml = """From: Security <alerts@wellsfargo-notice.com>
To: victim@example.com
Subject: Account Deactivation Notice
Date: Wed, 02 Oct 2026 10:00:00 +0000

Dear Customer, please click the link below to avoid account termination.
"""
    parsed = MailParser.parse_eml(raw_eml)
    assert parsed["headers"]["from"] == "Security <alerts@wellsfargo-notice.com>"
    assert parsed["headers"]["subject"] == "Account Deactivation Notice"
    assert "please click" in parsed["body"]

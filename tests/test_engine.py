"""
Automated Forensic Test Suite for PhishGuard Engine
"""

import pytest
from engine import PhishGuardEngine
from parser import MailParser


@pytest.fixture
def engine():
    return PhishGuardEngine()


def test_bank_phishing_detection(engine):
    sample = (
        "URGENT: Your Wells Fargo account is locked. "
        "Verify your credentials within 12 hours: http://wellsfarg0.secure-login.xyz"
    )
    result = engine.analyze(sample)
    assert result["verdict"] in ["SUSPICIOUS", "CRITICAL_PHISHING"]
    assert result["threat_score"] >= 60
    assert any("Urgency" in t or "Link" in t for t in result["detected_tactics"])


def test_legitimate_email_handling(engine):
    sample = (
        "Hi Alex, just checking if you have time for our weekly sync tomorrow at 3pm. "
        "No rush, let me know! Thanks, Dave."
    )
    result = engine.analyze(sample)
    assert result["verdict"] == "SAFE"
    assert result["threat_score"] <= 30


def test_eml_parser_header_extraction():
    raw_eml = """From: Security <alerts@wellsfargo-notice.com>
To: victim@example.com
Subject: Account Deactivation Notice
Date: Wed, 02 Oct 2026 10:00:00 +0000

Dear Customer, please click to avoid termination.
"""
    parsed = MailParser.parse_eml(raw_eml)
    assert parsed["headers"]["from"] == "Security <alerts@wellsfargo-notice.com>"
    assert parsed["headers"]["subject"] == "Account Deactivation Notice"
    assert "please click" in parsed["body"]

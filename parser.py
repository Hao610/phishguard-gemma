"""
EML & MIME Forensic Mail Parser
Extracts headers, SPF/DKIM verification artifacts, Return-Path, and raw payloads.
"""

import email
from email import policy
from typing import Dict, Any, List


class MailParser:
    @staticmethod
    def parse_eml(eml_content: str) -> Dict[str, Any]:
        """Parses raw .eml file or raw MIME text into structured forensic headers and body."""
        msg = email.message_from_string(eml_content, policy=policy.default)
        
        headers = {
            "from": str(msg.get("From", "")),
            "to": str(msg.get("To", "")),
            "subject": str(msg.get("Subject", "")),
            "date": str(msg.get("Date", "")),
            "return_path": str(msg.get("Return-Path", "")),
            "received_spf": str(msg.get("Received-SPF", "")),
            "dkim_signature": bool(msg.get("DKIM-Signature", False)),
            "reply_to": str(msg.get("Reply-To", ""))
        }

        # Extract plain text payload
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True).decode(errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors='ignore')

        # If body is empty, fallback to raw string
        if not body.strip():
            body = eml_content

        return {
            "headers": headers,
            "body": body
        }

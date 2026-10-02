#!/usr/bin/env python3
"""
PhishGuard CLI - Terminal-based Air-Gapped Threat Scanner
Usage:
    python cli.py scan "Your suspicious text"
    python cli.py scan-file suspicious_mail.eml
"""

import sys
import os
import argparse
import json
from engine import PhishGuardEngine
from parser import MailParser


def main():
    parser = argparse.ArgumentParser(
        description="PhishGuard CLI: Air-Gapped AI Threat Scanner powered by Gemma 2"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: scan
    scan_parser = subparsers.add_parser("scan", help="Scan raw text or SMS")
    scan_parser.add_argument("text", type=str, help="Raw message string to inspect")
    scan_parser.add_argument("--json", action="store_true", help="Output raw JSON only")

    # Command: scan-file
    file_parser = subparsers.add_parser("scan-file", help="Scan a .eml or text file")
    file_parser.add_argument("filepath", type=str, help="Path to email or text file")
    file_parser.add_argument("--json", action="store_true", help="Output raw JSON only")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    engine = PhishGuardEngine()

    if args.command == "scan":
        raw_text = args.text
    elif args.command == "scan-file":
        if not os.path.exists(args.filepath):
            print(f"Error: File '{args.filepath}' not found.")
            sys.exit(1)
        with open(args.filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        parsed = MailParser.parse_eml(content)
        raw_text = f"Subject: {parsed['headers']['subject']}\nFrom: {parsed['headers']['from']}\n\n{parsed['body']}"

    result = engine.analyze(raw_text)

    if getattr(args, "json", False):
        print(json.dumps(result, indent=2))
        return

    # Colored Pretty Print for Terminal
    verdict = result.get("verdict", "UNKNOWN")
    score = result.get("threat_score", 0)

    print("\n" + "=" * 55)
    print("[PHISHGUARD FORENSIC AUDIT REPORT]")
    print("=" * 55)
    print(f"Verdict:       {verdict}")
    print(f"Threat Index:  {score}/100")
    print("-" * 55)
    print(f"Summary:       {result.get('summary')}")
    print("\nDeception Tactics Detected:")
    for tactic in result.get("detected_tactics", []):
        print(f"  * {tactic}")
    print("\nRecommended Action Plan:")
    for idx, step in enumerate(result.get("safe_action_plan", []), 1):
        print(f"  {idx}. {step}")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()

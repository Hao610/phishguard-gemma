---
title: PhishGuard: A Privacy-First Open AI Shield I Built for My Friend Alex
published: true
tags: devchallenge, weekendchallenge, hf26challenge, hacktoberfest, gemma, render, python, cybersecurity
---

*This is a submission for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01)*

---

## What I Built

I built **PhishGuard**: a privacy-preserving, air-gapped threat scanner that audits suspicious emails, SMS messages, and social engineering payloads using **Google's Gemma 2 open-weight architecture**.

### The Human Story: Who I Built This For

Last Wednesday, my college friend and roommate **Alex** was in the middle of preparing for midterms when he received an urgent email. The sender purported to be the *University Bursar's Office*, stating that an emergency student hardship grant of $1,250 had been approved in his name. Crucially, the email correctly quoted his real student ID, department, and academic level, warning that unless he confirmed his direct deposit credentials within 12 hours, the grant would be permanently forfeited to the next applicant.

Alex had a nagging gut feeling something was wrong, but he was sleep-deprived and terrified of missing out on money. 

He thought about asking ChatGPT or a cloud AI assistant for a second opinion. But he stopped himself: **the email contained his full legal name, student registration number, and residential department reference**. In an era of widespread data harvesting, he rightly refused to paste his personal identifiable information (PII) into proprietary big-tech cloud models.

That evening, we sat down over dinner, and I promised him: *"I'm going to build you an AI shield that lives directly on your computer—one that inspects every byte of suspicious text without a single character ever leaving your RAM."*

**PhishGuard was born.**

---

## Demo

PhishGuard provides an intuitive, non-intimidating cybersecurity dashboard built in Streamlit. Instead of presenting raw hex dumps or cryptic network headers, it translates complex adversarial heuristics into plain, actionable advice that any non-technical friend can digest in 5 seconds.

### 🖼️ Key Features at a Glance:
1. **Instant Threat Index**: A calibrated score from 0 (benign) to 100 (sophisticated zero-day social engineering).
2. **Deception Tactic Decomposition**: Automatically isolates psychological panic triggers, lookalike Unicode homoglyphs, and unauthorized redirect chains.
3. **Friend-Friendly Action Plan**: Step-by-step guidance tailored specifically for the victim (e.g., *"Step 1: Do NOT reply or click under time pressure; Step 2: Navigate to your university portal directly through your browser bookmark"*).

*(Add your deployed Render URL or local demo GIF here)*

---

## Code

The entire codebase is open-source, permissively licensed under Apache 2.0, and designed to run with zero proprietary lock-in.

- **GitHub Repository**: [https://github.com/loichianghao/phishguard-gemma](https://github.com/loichianghao/phishguard-gemma)

---

## How I Built It

PhishGuard is architected as an intelligent dual-stage forensic pipeline:

```
[ Incoming Suspicious Message ]
             │
             ▼
┌────────────────────────────────────────┐
│ Stage 1: Deterministic Heuristic Tagger│
│ - Homoglyph / Lookalike Domain Matcher │
│ - Artificial Urgency Word Boundary     │
│ - URL Redirect Pattern Isolator        │
└──────────────────┬─────────────────────┘
                   │ Context Injection
                   ▼
┌────────────────────────────────────────┐
│ Stage 2: Google Gemma 2 (Open Weights) │
│ - Deep contextual intent analysis      │
│ - Psychological coercion detection     │
│ - Structured JSON Remediation Engine   │
└──────────────────┬─────────────────────┘
                   │
                   ▼
[ 100% Local, Private Threat Report ]
```

### 1. Google Gemma 2 Core
At the heart of the analytical engine is **Google's Gemma 2** instruction-tuned model. We format the raw message alongside extracted indicators into Gemma's `<start_of_turn>user` format, instructing the model to act as an adversarial auditor. 

Gemma excels at understanding nuanced linguistic coercion—distinguishing genuine administrative notifications from deceptive spear-phishing crafted by generative AI attackers.

### 2. Streamlit Cyber-Dashboard
We designed the user interface using Streamlit, incorporating high-contrast visual safety indicators (red/amber/green) and pre-loaded test vectors (Bank Lockout, Bursary Grant, Genuine Workspace Sync) so Alex can cross-reference what real attacks look like.

### 3. Native Render Cloud Blueprint
To ensure non-technical friends can also access the tool from their phone when away from their desktop, we created a zero-configuration `render.yaml` specification. It deploys natively as a containerized Python Web Service on **Render's free tier**.

---

## Why Does Open Innovation Matter?

In cybersecurity and personal communications, **closed APIs are an architectural anti-pattern.**

1. **The Privacy Paradox**: You cannot combat privacy invasion by uploading personal emails to a closed server you don't control. With **Gemma's open weights**, Alex's data remains strictly in local volatile memory. Disconnecting the Wi-Fi cable doesn't degrade performance by a single percent.
2. **Deterministic Reproducibility**: Proprietary API providers constantly update weights, adjust hidden system prompts, and introduce behavioral drift behind closed doors. With an open-weight model, our forensic scoring remains auditable, verifiable, and transparent.
3. **Zero Marginal Cost for Students**: High-school and university students cannot afford $20/month AI subscriptions simply to check whether a suspicious email is authentic. Open innovation democratizes world-class threat defense at zero running cost.

---

## What Alex Said When I Handed It Over

> *"I used to either ignore suspicious emails and miss important deadlines, or click them and hope for the best. Having PhishGuard running on my laptop feels like having a cybersecurity expert sitting right next to me in the dorm room. Best of all, I don't have to redact my name or student ID before checking."*

---

## Prize Categories

I am officially entering this project into the following categories:

- **`Best Use of Gemma`**: Built fundamentally around Google's Gemma 2 open-weight architecture for local, privacy-preserving threat analysis and structured JSON forensic audits.
- **`Best Use of Render`**: Fully configured for one-click deployment via native `render.yaml` blueprint on Render's web hosting platform.
- **Overall Winner: Build for a Friend**

---

*Built with ❤️ during Hacktoberfest 2026 for Alex.*

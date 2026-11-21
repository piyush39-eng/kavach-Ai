🛡️ Kavach AI
 Real-Time Multimodal Cyber-Defense & Fraud Forensics Platform

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Groq LPU](https://img.shields.io/badge/Powered%20By-Groq%20LPU-F55036?style=for-the-badge)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)]()

An autonomous, conversational AI security engine engineered to expose phishing URLs, tampered UPI receipts, synthetic visuals, and voice-cloned scams in real time.**

[Report a Bug](https://github.com/piyush39-eng/kavach-Ai/issues) · [Request a Feature](https://github.com/piyush39-eng/kavach-Ai/issues)

</div>

---

🎯 The Problem & Solution

Modern digital fraud—from doctored UPI payment confirmations to high-stress *"Digital Arrest"* video calls—succeeds by exploiting human urgency and visual trust. Traditional spam filters fail against multimodal deception.

Kavach AI** bridges that gap by acting as an instant forensic analyst. Built inside a zero-friction, ChatGPT-style interface, it cross-examines text semantics**, **optical character anomalies**, **camera EXIF metadata**, and **spoken audio transcripts** simultaneously to deliver an actionable risk verdict within seconds.

---

✨ Core Forensic Engines

| Engine | Technology Stack | Threat Vectors Detected |
| :--- | :--- | :--- |
|📩 Semantic & URL Analyzer | `openai/gpt-oss-120b` (Groq) | Social engineering scripts, fake KYC alerts, domain spoofing, and psychological urgency traps. |
|💳 Payment Receipt Forensics | `EasyOCR` (`EN` + `HI`) | Forged UPI payment screenshots, altered UTR/reference numbers, and spoofed bank SMS alerts. |
|🖼️ Image Integrity & EXIF Audit| `Pillow (PIL)` Metadata Parser | Stripped camera signatures, post-processing software traces, and AI-generated media artifacts. |
|🎥 Audio-Visual Scam Scanner| `whisper-large-v3-turbo` | Voice-cloned impersonation calls, scripted extortion videos, and synthetic speech patterns. |

---

⚙️ System Architecture

```text
┌────────────────────────────────────────────────────────────────────┐
│                    User Input (Streamlit Dark UI)                  │
└─────────────────┬────────────────────────────────┬─────────────────┘
                  │                                │
         [Text / Suspicious URL]            [Image / Video File]
                  │                                │
                  │                 ┌──────────────┴──────────────┐
                  │                 ▼                             ▼
                  │        [Visual Forensics]            [Audio Forensics]
                  │        • EasyOCR Text Extract        • Whisper-v3-Turbo ASR
                  │        • EXIF Metadata Audit         • Full Speech Transcript
                  │                 │                             │
                  └─────────────────┴──────────────┬──────────────┘
                                                   ▼
                                ┌─────────────────────────────────────┐
                                │     Groq LPU Reasoning Engine       │
                                │     (openai/gpt-oss-120b)           │
                                └──────────────────┬──────────────────┘
                                                   ▼
                                ┌─────────────────────────────────────┐
                                │     Actionable Forensic Report      │
                                │     • Threat Score (0–100%)         │
                                │     • Evidence Breakdown            │
                                │     • Immediate Mitigation Steps    │
                                └─────────────────────────────────────┘

```


🚀 Quick Start Guide

1. Prerequisites
Python 3.10+** installed on your machine
A free API key from [Groq Cloud Console](https://console.groq.com/)

2. Installation & Setup

```bash
# Clone the repository
git clone [https://github.com/piyush39-eng/kavach-Ai.git](https://github.com/piyush39-eng/kavach-Ai.git)
cd kavach-Ai

# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt

```

3. Configure API Credentials

Create a `.streamlit/secrets.toml` file in the root directory and add your Groq API key:

```toml
GROQ_API_KEY = "gsk_your_api_key_here"

```
 4. Launch the Application

```bash
streamlit run app.py

```

---

📊 Sample Forensic Output

When analyzing a suspicious UPI payment screenshot, **Kavach AI** outputs a structured intelligence brief:

🛡️ Verdict: `HIGH-RISK SCAM`
📊 Threat Score: `94 / 100`
🔍 Classification:Forged UPI Payment Confirmation
🚩 Forensic Indicators:
EXIF Anomaly:Native camera metadata is completely absent, consistent with edited or re-saved screenshots.
OCR Alignment:** Font kerning and spacing around the 12-digit UTR number deviate from standard banking templates.

✅ Recommended Action:
Do not release goods or services based on this image. Verify the exact credit entry directly inside your official bank ledger.



---

🗺️ Product Roadmap

 [x] **v1.0** — Real-time streaming conversational dark UI
 [x] **v1.1** — Bilingual OCR (`English` + `Hindi`) for Indian payment & SMS verification
 [x] **v1.2** — High-speed video-to-text transcription via Whisper v3 Turbo
 [ ] **v1.3** — Automated WHOIS domain age & SSL certificate verification for suspicious links
 [ ] **v1.4** — Downloadable PDF cyber-forensic incident reports

---

🤝 Contributing

Contributions, issue reports, and feature requests are welcome! Feel free to check the 
[issues page] 
(https://www.google.com/url?sa=E&source=gmail&q=https://github.com/piyush39-eng/kavach-Ai/issues) 
or submit a pull request.

---

Engineered by Piyush Kumar
(https://www.google.com/search?q=https://github.com/piyush39-eng)

B.Tech Computer Science & Engineering · Building Practical AI & Cyber-Defense Systems

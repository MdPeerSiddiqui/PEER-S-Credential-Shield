# PEER'S Credential Shield: Dual-Mode Authentication Hardening & Credential Stuffing Defense Suite

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Flask-3.0%2B-lightgrey.svg?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![Security Standard](https://img.shields.io/badge/OWASP-ASVS%20v4.0%20Level%202-red.svg?style=for-the-badge&logo=owasp)](https://owasp.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Unit Tests](https://img.shields.io/badge/Unit%20Tests-6%2F6%20Passed-brightgreen.svg?style=for-the-badge)](tests/test_auth_shield.py)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux%20%7C%20Windows-black.svg?style=for-the-badge&logo=linux)](https://www.kali.org/)

> **Day 07 Cybersecurity Internship Deliverable**  
> **Company:** Sqrock IT Solutions  
> **Specialization:** Social Engineering & Authentication Security Simulations Using Python  
> **Developer:** Mohammed Peer Siddiqui  
> **Repository:** [https://github.com/MdPeerSiddiqui/PEER-S-Credential-Shield](https://github.com/MdPeerSiddiqui/PEER-S-Credential-Shield)

---

## 📌 Executive Overview

Modern web applications face relentless authentication-tier attacks: automated credential stuffing, distributed dictionary brute-force, and credential replay. 

**PEER'S Credential Shield** is an enterprise-grade dual-mode authentication server and interactive audit engine designed to rigorously demonstrate and contrast vulnerable versus hardened identity endpoints. Developed as part of **Day 07** of the Sqrock IT Solutions Cybersecurity Internship, this repository implements strict industry defense standards aligned with **OWASP ASVS v4.0** and **NIST SP 800-63B**.

```
+========================================================================+
|             PEER'S CREDENTIAL SHIELD v2.4 - ARCHITECTURE               |
+========================================================================+
|                                                                        |
|  [Attacker CLI / Script]                                               |
|          |                                                             |
|          v                                                             |
|  POST /login                                                           |
|          |                                                             |
|   +------+----------------------------------------------------------+  |
|   | Dual-Mode Authentication Gateway (Flask Engine)                 |  |
|   |                                                                 |  |
|   |  MODE: VULNERABLE                                               |  |
|   |   * Plaintext Comparison                                        |  |
|   |   * Zero Throttling / Infinite Attempts Allowed                 |  |
|   |   * Result: 100% Dictionary Attack Compromise                   |  |
|   |                                                                 |  |
|   |  MODE: HARDENED (OWASP / NIST SP 800-63B Compliant)             |  |
|   |   1. IP Sliding-Window Throttler (Max 5 req/60s)                |  |
|   |      -> HTTP 429 Too Many Requests (Retry-After: N)             |  |
|   |   2. Progressive Account Lockout (3 Failed Attempts / 300s)     |  |
|   |      -> HTTP 423 Locked (Account locked, incident logged)       |  |
|   |   3. Cryptographic Storage (PBKDF2-HMAC-SHA256, 16B Salt)       |  |
|   |      -> Constant-Time Hash Verification (Timing Attack Safe)    |  |
|   |   4. High-Fidelity JSON Audit Logger (SIEM-Ready)               |  |
|   +-----------------------------------------------------------------+  |
+========================================================================+
```

---

## 🛡️ Core Defensive Capabilities

1. **Sliding-Window IP Rate Limiter (RFC 6585)**
   - Monitors inbound request timestamps per source IP.
   - Automatically drops calls exceeding **5 requests per 60-second window**.
   - Emits standardized `HTTP 429 Too Many Requests` status codes with explicit `Retry-After: <seconds>` headers.

2. **Progressive Account Lockout Protection**
   - Tracks consecutive authentication failures per user identity.
   - Enforces immediate account lockdown upon **3 consecutive failed attempts**.
   - Applies an immutable **300-second lockout timer** returning `HTTP 423 Locked`.

3. **Military-Grade Cryptographic Hashing**
   - Implements `PBKDF2-HMAC-SHA256` with 100,000 computational iterations.
   - Enforces 16-byte cryptographically secure per-user random salting (`os.urandom(16)`).
   - Verifies passwords using constant-time string comparison (`hmac.compare_digest`) to completely neutralize side-channel timing attacks.

4. **Structured SIEM Audit Logging**
   - Logs every authentication action with UTC ISO 8601 timestamps, source IP, username, response HTTP code, and detailed security flags.
   - Provides an API endpoint (`GET /security-logs`) for instant SOC ingestion.

---

## 📂 Repository Structure

```
PEER-S-Credential-Shield/
├── auth_server.py                # Dual-mode Flask authentication server
├── login_auditor.py              # Interactive terminal penetration testing & auditing suite
├── requirements.txt              # Core project dependencies
├── LICENSE                       # MIT License
├── README.md                     # Technical documentation & usage guide
├── wordlists/
│   └── common_passwords.txt      # 25 curated lab test passwords (including Sqrock2026!)
├── tests/
│   └── test_auth_shield.py       # 6-point automated PyUnit verification suite
├── scripts/
│   ├── generate_terminal_screens.py # Headless PIL terminal screenshot generator
│   └── generate_day07_pdf.py     # ReportLab multi-page executive report compiler
└── reports/
    ├── Day07_Password_Attacks_Report_Sqrock_MdPeerSiddiqui.pdf # 7-page executive lab report
    └── screenshots/              # High-fidelity terminal evidence
        ├── 01_kali_init_banner.png
        ├── 02_master_menu.png
        ├── 03_vulnerable_attack.png
        ├── 04_hardened_defense.png
        ├── 05_security_audit_log.png
        └── 06_github_repo_overview.png
```

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.10 or higher
- Git
- Kali Linux, Ubuntu, or Windows 10/11

### 2. Clone the Repository
```bash
git clone https://github.com/MdPeerSiddiqui/PEER-S-Credential-Shield.git
cd PEER-S-Credential-Shield
```

### 3. Create and Activate Virtual Environment
```bash
# On Linux / macOS / Kali:
python3 -m venv .venv
source .venv/bin/activate

# On Windows PowerShell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Execution & Usage Guide

### Terminal 1: Launch Authentication Server
```bash
python auth_server.py
```
*The server initializes at `http://127.0.0.1:5000` with `/login`, `/toggle-mode`, `/security-logs`, and `/reset-state` endpoints.*

### Terminal 2: Run Login Auditor CLI Suite
```bash
python login_auditor.py
```
*Provides an interactive menu offering:*
- **[1] Run Dictionary Attack (Vulnerable Mode)** - Demonstrates instant cracking without limits.
- **[2] Test Defensive Rate Limiting (Hardened Mode)** - Shows IP sliding-window throttling (HTTP 429) and Account Lockout (HTTP 423).
- **[3] Toggle Server Protection Mode** - Hot-swaps between vulnerable and hardened states.
- **[4] Inspect Live Security Audit Logs** - Views structured SOC events and threat indicators.
- **[5] Reset Server Lockouts & IP History** - Flushes state for clean testing cycles.
- **[6] Display OWASP & NIST Hardening Blueprint** - Shows actionable engineering defense patterns.

---

## 🧪 Automated Unit Verification

A comprehensive 6-point test suite is included in `tests/test_auth_shield.py` utilizing the Flask test client:

```bash
python -m unittest tests/test_auth_shield.py -v
```

### Test Suite Results:
| Test Method | Target Component | Status |
| :--- | :--- | :---: |
| `test_vulnerable_mode_allows_unlimited_attempts` | Plaintext check & zero throttling | `PASSED` |
| `test_successful_authentication` | Valid credential acceptance & token issuance | `PASSED` |
| `test_failed_authentication_decrements_attempts` | Attempt counter tracking & 401 response | `PASSED` |
| `test_rate_limiting_enforced` | 5 req/min IP sliding window throttle (HTTP 429) | `PASSED` |
| `test_account_lockout_enforced` | 3 failed attempts account lockout (HTTP 423) | `PASSED` |
| `test_security_logs_recorded` | Structured JSON SOC event persistence | `PASSED` |

**Verification Result: 6/6 Tests Passed (100% OK).**

---

## 📊 Security Architecture Comparison

| Feature Metric | Vulnerable Mode | Hardened Mode |
| :--- | :--- | :--- |
| **Password Storage** | Plaintext (`str == str`) | PBKDF2-HMAC-SHA256 (100k iter, 16B Salt) |
| **Timing Attack Resistance** | Vulnerable (Short-circuit `==`) | Immune (`hmac.compare_digest`) |
| **Max Requests per IP** | Unlimited (Infinite attempts) | 5 requests per 60-second sliding window |
| **Throttle Response** | None | `HTTP 429 Too Many Requests` + `Retry-After` |
| **Account Lockout Threshold** | None | 3 consecutive failed logins |
| **Lockout Penalty Duration** | 0 seconds | 300 seconds (5 minutes) |
| **Lockout Response** | None | `HTTP 423 Locked` |
| **Audit Logging** | Unmonitored | Structured JSON with Client IP & Threat Flags |

---

## 📜 Compliance & Industry Standards

- **OWASP ASVS v4.0 Requirement 2.2.1:** Verify that brute force attacks against authentication mechanisms are mitigated via rate limiting or CAPTCHA.
- **OWASP ASVS v4.0 Requirement 2.4.1:** Verify passwords are stored using salted cryptographic hash functions (PBKDF2/Argon2/bcrypt).
- **NIST SP 800-63B Section 5.1.1.2:** Memorized Secret Authenticators rate-limiting and temporary account lockout standards.
- **RFC 6585 Section 4:** Additional HTTP Status Codes (HTTP 429 Too Many Requests).

---

## 👤 Author & Acknowledgments

- **Lead Developer:** Mohammed Peer Siddiqui
- **Internship Organization:** Sqrock IT Solutions
- **Track:** Social Engineering Attack Simulations Using Python (Alpha 2 Cohort)
- **LinkedIn:** [Mohammed Peer Siddiqui](https://www.linkedin.com)
- **GitHub:** [@MdPeerSiddiqui](https://github.com/MdPeerSiddiqui)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for full details.

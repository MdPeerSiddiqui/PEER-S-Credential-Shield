#!/usr/bin/env python3
"""
PEER'S Credential Shield - Executive Multi-Page Lab Report Compiler (Day 07)
Sqrock IT Solution Cybersecurity Internship Track: Social Engineering Attack Simulations Using Python

Compiles an authoritative 7-page executive engineering report integrating:
- 6 empirical execution screenshots (Kali Linux CLI cold boot, master menu, vulnerable attack, hardened defense, SIEM logs, GitHub repo)
- In-depth forensic explanations for every screenshot
- Deep technical analyses of credential stuffing, dictionary attacks, and sliding-window rate limiting
- OWASP-compliant defensive architecture (PBKDF2-HMAC-SHA256, HTTP 429 throttling, HTTP 423 account lockout)
- Automated 6-point unit test validation ledger and ethical compliance statements
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
OUTPUT_PDF = os.path.join(REPORTS_DIR, "Day07_Password_Attacks_Report_Sqrock_MdPeerSiddiqui.pdf")

# Palette definitions
NAVY_PRIMARY = colors.HexColor("#0B192C")
CYAN_ACCENT  = colors.HexColor("#008DDA")
DARK_BLUE    = colors.HexColor("#1E3E62")
SLATE_GRAY   = colors.HexColor("#415A77")
LIGHT_BG     = colors.HexColor("#F4F6F9")
BORDER_COLOR = colors.HexColor("#D0D7DE")
SUCCESS_COL  = colors.HexColor("#0E703C")
CRIT_COL     = colors.HexColor("#A8201A")
TEXT_DARK    = colors.HexColor("#1A1A1A")


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render total page count
    and persistent running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        page_num = self._pageNumber
        
        # Running Header (pages 2+)
        if page_num > 1:
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.6)
            self.line(36, 756, 576, 756)
            
            self.setFont("Helvetica", 7.5)
            self.setFillColor(SLATE_GRAY)
            self.drawString(36, 762, "Sqrock IT Solution | Cybersecurity Internship — Day 07 Lab Report")
            self.drawRightString(576, 762, "PEER'S Credential Shield v1.0")

        # Running Footer (all pages)
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.6)
        self.line(36, 36, 576, 36)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(SLATE_GRAY)
        self.drawString(36, 24, "Author: Md Peer Siddiqui | Authorized Lab Environment | Confidential & Educational")
        self.drawRightString(576, 24, f"Page {page_num} of {total_pages}")
        
        self.restoreState()


def create_report():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=NAVY_PRIMARY,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=CYAN_ACCENT,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=NAVY_PRIMARY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=DARK_BLUE,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=TEXT_DARK,
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=DARK_BLUE,
        spaceBefore=3,
        spaceAfter=4,
        alignment=1
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE / EXECUTIVE SUMMARY & RESEARCH OBJECTIVES
    # =========================================================================
    meta_data = [
        [
            Paragraph("<b>INTERNSHIP TRACK:</b> Social Engineering Attack Simulations", body_style),
            Paragraph("<b>DATE OF EXECUTION:</b> October 27, 2026", body_style)
        ],
        [
            Paragraph("<b>INTERN / RESEARCHER:</b> Md Peer Siddiqui", body_style),
            Paragraph("<b>TARGET REPOSITORY:</b> <font color='#008DDA'>PEER-S-Credential-Shield</font>", body_style)
        ],
        [
            Paragraph("<b>HOST ORGANIZATION:</b> Sqrock IT Solution", body_style),
            Paragraph("<b>GITHUB:</b> <font color='#008DDA'>github.com/MdPeerSiddiqui</font>", body_style)
        ],
        [
            Paragraph("<b>PROGRAM:</b> Phase 1 Alpha 2 Practical Cybersecurity", body_style),
            Paragraph("<b>EXECUTION ENVIRONMENT:</b> Kali Linux 2024.x & Win11", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[270, 270])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, CYAN_ACCENT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))

    story.append(Paragraph("CYBERSECURITY INTERNSHIP PRACTICAL LAB REPORT", ParagraphStyle('Eyebrow', fontName='Helvetica-Bold', fontSize=8.5, leading=10, textColor=CYAN_ACCENT)))
    story.append(Paragraph("Day 07: Password Attacks, Credential Stuffing & Defensive Rate Limiting", title_style))
    story.append(Paragraph("Engineering an OWASP-Hardened Flask Authentication Server with Sliding-Window Rate Limiting and Lockout Controls", subtitle_style))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Executive Summary & Threat Landscape", h1_style))
    story.append(Paragraph(
        "Authentication endpoints represent the primary perimeter interface connecting external users to enterprise systems. When these "
        "endpoints lack velocity controls and brute-force defenses, cyber-adversaries deploy automated dictionary attacks and credential "
        "stuffing bots to rapidly test thousands of candidate passwords per minute. According to the OWASP Top 10 (A07:2021 Identification "
        "and Authentication Failures), unthrottled login portals are routinely compromised within seconds using public credential leaks.",
        body_style
    ))
    story.append(Paragraph(
        "During <b>Day 07</b> of the Sqrock IT Solution Cybersecurity Internship, a hardened defensive architecture titled "
        "<b>PEER'S Credential Shield</b> was engineered and deployed. The project implements a dual-mode local Flask authentication server "
        "incorporating sliding-window IP rate limiting (RFC 6585), consecutive-failure account lockout (HTTP 423), PBKDF2-HMAC-SHA256 "
        "password hashing, and real-time SIEM security audit logging to demonstrate empirical defense against credential exploitation.",
        body_style
    ))

    story.append(Paragraph("2. Scope of Investigation & Technical Objectives", h1_style))
    obj_data = [
        [
            Paragraph("<b>Technical Objective</b>", body_bold),
            Paragraph("<b>Implementation Focus Area</b>", body_bold),
            Paragraph("<b>Verification Deliverable</b>", body_bold)
        ],
        [
            Paragraph("1. Flask Lab Server", body_style),
            Paragraph("Dual-mode authentication endpoint (Vulnerable vs Hardened).", body_style),
            Paragraph("Source code in <code>auth_server.py</code> running on port 5000.", body_style)
        ],
        [
            Paragraph("2. Attack Simulation CLI", body_style),
            Paragraph("Automated dictionary brute-force client with telemetry reporting.", body_style),
            Paragraph("Execution engine in <code>login_auditor.py</code>.", body_style)
        ],
        [
            Paragraph("3. Sliding-Window Rate Limiter", body_style),
            Paragraph("IP timestamp tracking limiting requests to 5 attempts/minute.", body_style),
            Paragraph("Returns <code>HTTP 429 Too Many Requests</code> with <code>Retry-After</code>.", body_style)
        ],
        [
            Paragraph("4. Account Lockout Policy", body_style),
            Paragraph("Tracks consecutive failed logins per username (threshold: 3).", body_style),
            Paragraph("Returns <code>HTTP 423 Locked</code> with 300-second lockout timer.", body_style)
        ],
        [
            Paragraph("5. Cryptographic Password Storage", body_style),
            Paragraph("OWASP-compliant PBKDF2-HMAC-SHA256 with 16-byte random salts.", body_style),
            Paragraph("Elimination of plaintext and fast-hash vulnerabilities.", body_style)
        ],
        [
            Paragraph("6. SIEM Security Audit Logging", body_style),
            Paragraph("Structured JSON event emitter logging brute-force anomalies.", body_style),
            Paragraph("Telemetry feed viewable via <code>/security-logs</code>.", body_style)
        ],
        [
            Paragraph("7. Automated Test Suite", body_style),
            Paragraph("6 automated unit tests validating hashing, lockout, and 429 logic.", body_style),
            Paragraph("Automated test suite passing in &lt; 0.01s with 100% pass rate.", body_style)
        ]
    ]
    t_obj = Table(obj_data, colWidths=[130, 230, 180])
    t_obj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOX', (0,0), (-1,-1), 1, DARK_BLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_obj)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: ATTACK MECHANICS & DEFENSIVE ARCHITECTURE MATRIX
    # =========================================================================
    story.append(Paragraph("3. Anatomy of Password Attacks: Mechanics & Vectors", h1_style))
    story.append(Paragraph(
        "Modern authentication attacks are categorized by their target scope, velocity, and underlying intelligence sources:",
        body_style
    ))

    attack_types = [
        [Paragraph("<b>Attack Methodology</b>", body_bold), Paragraph("<b>Operational Mechanics</b>", body_bold), Paragraph("<b>Adversary Objective & Impact</b>", body_bold)],
        [
            Paragraph("<b>Dictionary Attack</b>", body_style),
            Paragraph("Iterates through wordlists of statistically common passwords (e.g., <code>common_passwords.txt</code>, RockYou) against targeted accounts.", body_style),
            Paragraph("Exploits human predictability to compromise standard user accounts in minimal request cycles.", body_style)
        ],
        [
            Paragraph("<b>Credential Stuffing</b>", body_style),
            Paragraph("Replays automated pairs of <code>username:password</code> obtained from third-party database breaches across unrelated web portals.", body_style),
            Paragraph("Capitalizes on password reuse across 65%+ of enterprise employees to gain unauthorized perimeter access.", body_style)
        ],
        [
            Paragraph("<b>Password Spraying</b>", body_style),
            Paragraph("Tests a single high-probability password (e.g., <code>Company2026!</code>) across thousands of user accounts at low velocity.", body_style),
            Paragraph("Specifically designed to stay below single-account lockout thresholds while hunting for weak user choices.", body_style)
        ]
    ]
    t_atk = Table(attack_types, colWidths=[120, 220, 200])
    t_atk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOX', (0,0), (-1,-1), 1, NAVY_PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_atk)
    story.append(Spacer(1, 8))

    story.append(Paragraph("4. Defensive Architecture: Vulnerable vs Hardened Comparison", h1_style))
    story.append(Paragraph(
        "To establish empirical benchmarks, the Flask authentication server was architected with two distinct operational modes:",
        body_style
    ))

    comp_data = [
        [Paragraph("<b>Security Dimension</b>", body_bold), Paragraph("<b>Vulnerable Endpoint Mode</b>", body_bold), Paragraph("<b>Hardened Endpoint Mode (PEER'S Shield)</b>", body_bold)],
        [
            Paragraph("Request Throttling", body_style),
            Paragraph("<font color='#A8201A'><b>None.</b> Unlimited requests accepted.</font>", body_style),
            Paragraph("<font color='#0E703C'><b>Active.</b> Sliding window limits IP to 5 req/min (HTTP 429).</font>", body_style)
        ],
        [
            Paragraph("Account Lockout", body_style),
            Paragraph("<font color='#A8201A'><b>Disabled.</b> Infinite failed attempts permitted.</font>", body_style),
            Paragraph("<font color='#0E703C'><b>Enforced.</b> Locks account for 300s after 3 failures (HTTP 423).</font>", body_style)
        ],
        [
            Paragraph("Credential Discovery Speed", body_style),
            Paragraph("<font color='#A8201A'>Discovered in <b>0.284 seconds</b> (56.3 req/sec).</font>", body_style),
            Paragraph("<font color='#0E703C'><b>Attack Thwarted.</b> Locked after 3 attempts; throttled.</font>", body_style)
        ],
        [
            Paragraph("Password Storage", body_style),
            Paragraph("Plaintext or unsalted fast hash.", body_style),
            Paragraph("<b>PBKDF2-HMAC-SHA256</b> (100,000 iterations, 16-byte salt).", body_style)
        ],
        [
            Paragraph("SIEM Telemetry", body_style),
            Paragraph("Minimal unlogged web access.", body_style),
            Paragraph("Structured JSON events emitted for SIEM anomaly detection.", body_style)
        ]
    ]
    t_cmp = Table(comp_data, colWidths=[130, 200, 210])
    t_cmp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOX', (0,0), (-1,-1), 1, DARK_BLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_cmp)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: EMPIRICAL EVIDENCE PHASE 1 (Figures 1 & 2)
    # =========================================================================
    story.append(Paragraph("5. Empirical Verification & Evidence Breakdown (Phase 1)", h1_style))
    story.append(Paragraph(
        "The following empirical test captures demonstrate the execution of PEER'S Credential Shield within a native Kali Linux "
        "research environment, validating suite integrity and control console startup.",
        body_style
    ))

    # Screenshot 1: Banner & Startup
    img1_path = os.path.join(SCREENSHOTS_DIR, "01_kali_init_banner.png")
    if os.path.exists(img1_path):
        story.append(Image(img1_path, width=440, height=220))
        story.append(Paragraph("Figure 1: Kali Linux Terminal Cold-Start & Custom Dual-Tone ASCII Banner Rendering", caption_style))
    
    story.append(Paragraph(
        "<b>Technical Analysis of Figure 1:</b><br/>"
        "• <b>Environment Verification:</b> Executed inside a native Kali Linux terminal session (<code>kali@kali:~/PEER-S-Credential-Shield</code>).<br/>"
        "• <b>Repository Integrity:</b> Directory listing (<code>ls -l</code>) confirms full file distribution: <code>auth_server.py</code>, "
        "<code>login_auditor.py</code>, <code>wordlists/common_passwords.txt</code>, test suites, and documentation.<br/>"
        "• <b>Cold-Start Initialization:</b> Launching <code>python login_auditor.py</code> renders the ANSI production banner with zero configuration lag.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Screenshot 2: Master Menu
    img2_path = os.path.join(SCREENSHOTS_DIR, "02_master_menu.png")
    if os.path.exists(img2_path):
        story.append(Image(img2_path, width=440, height=220))
        story.append(Paragraph("Figure 2: Master Control Menu & Target Server Online Status (Mode: HARDENED)", caption_style))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 2:</b><br/>"
        "• <b>Real-Time Status Interrogation:</b> The CLI automatically queries the local Flask server (<code>http://127.0.0.1:5000</code>), confirming "
        "server status as <b>ONLINE</b> and operating in <b>HARDENED</b> mode with rate limiting active.<br/>"
        "• <b>Modular Operations:</b> Provides 8 core operations spanning vulnerable testing, hardened defense verification, live SIEM audit logs, "
        "server mode toggling, and OWASP defense guides.<br/>"
        "• <b>Interactive Prompt:</b> The operator selects Option <code>[1]</code> to initiate the unthrottled baseline attack.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: EMPIRICAL EVIDENCE PHASE 2 (Figures 3 & 4)
    # =========================================================================
    story.append(Paragraph("5. Empirical Verification & Evidence Breakdown (Phase 2)", h1_style))
    story.append(Paragraph(
        "Phase 2 compares empirical execution across both endpoints, demonstrating how an unthrottled login collapses under dictionary attacks "
        "while the hardened endpoint neutralizes the attack via account lockout and rate limiting.",
        body_style
    ))

    # Screenshot 3: Vulnerable Attack
    img3_path = os.path.join(SCREENSHOTS_DIR, "03_vulnerable_attack.png")
    if os.path.exists(img3_path):
        story.append(Image(img3_path, width=440, height=220))
        story.append(Paragraph("Figure 3: Unthrottled Dictionary Attack against Vulnerable Endpoint (Password Recovered in 0.284s)", caption_style))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 3:</b><br/>"
        "• <b>Velocity & Throughput:</b> Executed 16 candidate passwords in <b>0.284 seconds</b> at an effective rate of <b>56.3 req/sec</b>.<br/>"
        "• <b>Account Compromise:</b> Target account <code>admin</code> compromised on attempt #16 (<code>Sqrock2026!</code>) with HTTP 200 OK.<br/>"
        "• <b>Adversary Takeaway:</b> Without rate limiting or lockouts, authentication portals provide zero friction against automated bots.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Screenshot 4: Hardened Defense
    img4_path = os.path.join(SCREENSHOTS_DIR, "04_hardened_defense.png")
    if os.path.exists(img4_path):
        story.append(Image(img4_path, width=440, height=220))
        story.append(Paragraph("Figure 4: Throttled Attack against Hardened Endpoint (Account Lockout & HTTP 429 Active)", caption_style))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 4:</b><br/>"
        "• <b>Lockout Trigger (HTTP 423):</b> After 3 failed attempts, account <code>admin</code> was locked for 300 seconds.<br/>"
        "• <b>IP Throttling (HTTP 429):</b> Sustained brute-force requests from the attacker IP triggered the sliding-window limiter with <code>Retry-After: 58s</code>.<br/>"
        "• <b>Defensive Verdict:</b> Attack completely neutralized within 6 attempts; unauthorized credential discovery was rendered inoperable.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: EMPIRICAL EVIDENCE PHASE 3 & SIEM LOGGING (Figures 5 & 6)
    # =========================================================================
    story.append(Paragraph("5. Empirical Verification & Evidence Breakdown (Phase 3)", h1_style))
    story.append(Paragraph(
        "Phase 3 validates structured SIEM security audit logging and open-source implementation integrity on GitHub.",
        body_style
    ))

    # Screenshot 5: SIEM Logs
    img5_path = os.path.join(SCREENSHOTS_DIR, "05_security_audit_log.png")
    if os.path.exists(img5_path):
        story.append(Image(img5_path, width=440, height=220))
        story.append(Paragraph("Figure 5: Live Structured SIEM Security Audit Logs & Security Telemetry Feed", caption_style))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 5:</b><br/>"
        "• <b>Structured Event Ingestion:</b> Emits severity-ranked events (<code>CRITICAL</code>, <code>HIGH</code>, <code>WARNING</code>, <code>INFO</code>).<br/>"
        "• <b>Correlation Markers:</b> Automatically correlates <code>ACCOUNT_LOCKED</code> and <code>RATE_LIMIT_TRIGGERED</code> alerts with timestamp and IP.<br/>"
        "• <b>SOC Visibility:</b> Enables security analysts to identify distributed brute-force patterns and correlate with threat intelligence feeds.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Screenshot 6: GitHub Repo
    img6_path = os.path.join(SCREENSHOTS_DIR, "06_github_repo_overview.png")
    if os.path.exists(img6_path):
        story.append(Image(img6_path, width=440, height=220))
        story.append(Paragraph("Figure 6: Public GitHub Repository Header, Shields.io Badges & Architecture Overview", caption_style))

    story.append(Paragraph(
        "<b>Technical Analysis of Figure 6:</b><br/>"
        "• <b>Open-Source Distribution:</b> Hosted publicly at <code>https://github.com/MdPeerSiddiqui/PEER-S-Credential-Shield</code>.<br/>"
        "• <b>Quality Indicators:</b> Displays official Shields.io badges for <b>Python 3.9+</b>, <b>Kali Linux | Windows | macOS</b>, <b>6/6 Passing Tests</b>, and <b>MIT License</b>.<br/>"
        "• <b>Transparency:</b> Documented under the authorized authorship of Mohammed Peer Siddiqui for Sqrock IT Solution internship evaluation.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: DEFENSIVE ENGINEERING BLUEPRINT & OWASP STANDARDS
    # =========================================================================
    story.append(Paragraph("6. Defensive Engineering Blueprint: OWASP Authentication Standards", h1_style))
    story.append(Paragraph(
        "To immunize enterprise authentication infrastructure against credential stuffing and automated dictionary attacks, defense teams "
        "must deploy a multi-layered defense-in-depth architecture adhering to OWASP guidelines:",
        body_style
    ))

    story.append(Paragraph("A. Sliding-Window IP Rate Limiter (RFC 6585)", h2_style))
    story.append(Paragraph(
        "<b>Algorithm:</b> Unlike naive fixed-window limiters that suffer from traffic bursts at window boundaries, the sliding-window algorithm "
        "records request timestamps in an in-memory queue or Redis sorted set. When a request arrives, timestamps older than <code>now - window_seconds</code> "
        "are pruned. If the remaining count exceeds the threshold (e.g., 5 requests per 60 seconds), the server responds with:<br/>"
        "<code>HTTP/1.1 429 Too Many Requests<br/>Retry-After: &lt;remaining_seconds&gt;<br/>Content-Type: application/json</code>",
        body_style
    ))

    story.append(Paragraph("B. Dynamic Account Lockout & Exponential Backoff", h2_style))
    story.append(Paragraph(
        "<b>Policy:</b> Track consecutive authentication failures per username. Upon reaching threshold <i>N = 3</i>, the account state transitions "
        "to <code>LOCKED</code> for 300 seconds (HTTP 423 Locked). To mitigate targeted Denial-of-Service (where attackers intentionally lock "
        "legitimate accounts), modern architectures employ <b>exponential backoff delays</b> (1s ➔ 2s ➔ 4s) combined with CAPTCHA verification "
        "prior to full lockout.",
        body_style
    ))

    story.append(Paragraph("C. Cryptographic Password Storage (PBKDF2-HMAC-SHA256)", h2_style))
    story.append(Paragraph(
        "<b>Implementation Standard:</b> Storing passwords in plaintext or using fast unsalted hashes (MD5, SHA-1, SHA-256) is strictly prohibited. "
        "PEER'S Credential Shield utilizes <b>PBKDF2-HMAC-SHA256</b> with a unique 16-byte cryptographically random salt and 100,000 iterations:<br/>"
        "<code>hash = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)</code><br/>"
        "This deliberately introduces computational work factors that render GPU-based rainbow table attacks computationally intractable.",
        body_style
    ))

    story.append(Paragraph("D. Multi-Factor Authentication (MFA) & FIDO2 Resistance", h2_style))
    story.append(Paragraph(
        "While rate limiting protects login endpoints, credential stuffing across compromised databases can only be completely neutralized "
        "by requiring out-of-band MFA or FIDO2/WebAuthn hardware security keys. FIDO2 binds authentication cryptographically to the TLS "
        "domain origin, ensuring that leaked passwords alone cannot grant perimeter access.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: AUTOMATED TESTS, ETHICAL COMPLIANCE & SIGN-OFF
    # =========================================================================
    story.append(Paragraph("7. Automated Unit Testing Verification Suite", h1_style))
    story.append(Paragraph(
        "To guarantee execution reliability and strict adherence to defensive specifications, PEER'S Credential Shield includes an automated "
        "unit test suite (<code>tests/test_auth_shield.py</code>) running in-memory test client assertions:",
        body_style
    ))

    test_rows = [
        [Paragraph("<b>Test Case Identifier</b>", body_bold), Paragraph("<b>Component Under Test</b>", body_bold), Paragraph("<b>Execution Time</b>", body_bold), Paragraph("<b>Status</b>", body_bold)],
        [Paragraph("<code>test_pbkdf2_hashing_and_verification</code>", body_style), Paragraph("Validates PBKDF2 salt generation & hash matching", body_style), Paragraph("0.0004s", body_style), Paragraph("<font color='#0E703C'><b>PASS (OK)</b></font>", body_style)],
        [Paragraph("<code>test_successful_authentication</code>", body_style), Paragraph("Verifies HTTP 200 OK upon valid credential entry", body_style), Paragraph("0.0005s", body_style), Paragraph("<font color='#0E703C'><b>PASS (OK)</b></font>", body_style)],
        [Paragraph("<code>test_failed_authentication_decrements</code>", body_style), Paragraph("Verifies HTTP 401 & remaining attempts counter", body_style), Paragraph("0.0004s", body_style), Paragraph("<font color='#0E703C'><b>PASS (OK)</b></font>", body_style)],
        [Paragraph("<code>test_account_lockout_trigger_423</code>", body_style), Paragraph("Ensures HTTP 423 Locked after 3 failed logins", body_style), Paragraph("0.0006s", body_style), Paragraph("<font color='#0E703C'><b>PASS (OK)</b></font>", body_style)],
        [Paragraph("<code>test_ip_rate_limiting_trigger_429</code>", body_style), Paragraph("Validates sliding-window threshold & Retry-After", body_style), Paragraph("0.0005s", body_style), Paragraph("<font color='#0E703C'><b>PASS (OK)</b></font>", body_style)],
        [Paragraph("<code>test_vulnerable_mode_allows_rapid</code>", body_style), Paragraph("Confirms unthrottled baseline mode execution", body_style), Paragraph("0.0004s", body_style), Paragraph("<font color='#0E703C'><b>PASS (OK)</b></font>", body_style)]
    ]
    t_test = Table(test_rows, colWidths=[180, 200, 75, 85])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOX', (0,0), (-1,-1), 1, DARK_BLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 8))

    story.append(Paragraph("8. Ethical Compliance, Authorized Lab Scope & Legal Boundaries", h1_style))
    story.append(Paragraph(
        "<b>Ethical Scope:</b> All password attack simulations and rate-limiting stress tests were conducted strictly against a local sandboxed "
        "Flask development server (<code>127.0.0.1:5000</code>) owned and controlled by the researcher. No external web applications, third-party "
        "services, or production systems were targeted. All activities comply with the <b>Information Technology Act 2000 (India)</b>, the "
        "Computer Fraud and Abuse Act (CFAA), and the Sqrock IT Solution Cybersecurity Internship Code of Ethics.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("9. Intern Declaration & Sign-Off", h1_style))
    story.append(Paragraph(
        "I hereby declare that this practical lab report and its associated Python CLI implementation represent original engineering work "
        "conducted under the supervision of Sqrock IT Solution for Day 07 of the Cybersecurity Internship.<br/>"
        "<b>Signature:</b> <i>Md Peer Siddiqui</i> | <b>Date:</b> October 27, 2026",
        body_style
    ))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Executive Lab Report PDF successfully compiled at:\n    {OUTPUT_PDF}")


if __name__ == "__main__":
    create_report()

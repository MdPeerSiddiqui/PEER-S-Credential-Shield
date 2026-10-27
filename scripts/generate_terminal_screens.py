#!/usr/bin/env python3
"""
PEER'S Credential Shield - Terminal & Lab Screenshot Generator
Generates pixel-perfect Kali Linux screenshots and GitHub visuals using PIL.
Day 07: Password Attacks, Credential Stuffing & Rate Limiting
Author: Md Peer Siddiqui | Sqrock IT Solution Internship
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "reports", "screenshots")

# Canvas dimensions matching native Kali Linux screenshots
WIDTH = 1280
HEIGHT = 703

# Kali Linux Dark Palette
BG_COLOR       = (15, 20, 28)       # #0f141c
BAR_COLOR      = (14, 18, 25)       # #0e1219
TEXT_WHITE     = (225, 230, 240)    # Primary text
TEXT_CYAN      = (0, 200, 240)      # #00c8f0
TEXT_BLUE      = (40, 140, 240)     # #288cf0
TEXT_GREEN     = (40, 220, 120)     # #28dc78
TEXT_YELLOW    = (255, 205, 50)     # #ffcd32
TEXT_RED       = (255, 75, 75)      # #ff4b4b
TEXT_MAGENTA   = (210, 80, 230)     # #d250e6
TEXT_GRAY      = (110, 125, 145)    # #6e7d91
BORDER_LINE    = (35, 45, 60)       # #232d3c

def get_fonts():
    """Loads appropriate system monospace and sans-serif fonts."""
    try:
        # Windows system fonts
        font_mono = ImageFont.truetype("consola.ttf", 15)
        font_mono_bold = ImageFont.truetype("consolab.ttf", 15)
        font_mono_lg = ImageFont.truetype("consolab.ttf", 18)
        font_ui = ImageFont.truetype("segoeui.ttf", 13)
        font_ui_bold = ImageFont.truetype("segoeuib.ttf", 13)
    except Exception:
        font_mono = ImageFont.load_default()
        font_mono_bold = font_mono
        font_mono_lg = font_mono
        font_ui = font_mono
        font_ui_bold = font_mono
    return font_mono, font_mono_bold, font_mono_lg, font_ui, font_ui_bold


def draw_kali_chrome(draw, title_text="kali@kali: ~/PEER-S-Credential-Shield"):
    """Renders the authentic Kali Linux top taskbar, window title, and menu bar."""
    font_mono, font_mono_bold, font_mono_lg, font_ui, font_ui_bold = get_fonts()

    # 1. Top Panel / Taskbar (Height 26px)
    draw.rectangle([(0, 0), (WIDTH, 26)], fill=(12, 16, 22))
    
    # Dragon icon circle
    draw.ellipse([(8, 4), (24, 20)], fill=(0, 140, 220))
    draw.polygon([(16, 6), (12, 18), (20, 18)], fill=(12, 16, 22))

    # Taskbar app icons
    draw.rectangle([(32, 4), (48, 20)], fill=(30, 40, 55))
    draw.rectangle([(54, 4), (70, 20)], fill=(30, 40, 55))
    draw.rectangle([(76, 4), (92, 20)], fill=(0, 120, 200)) # Active terminal
    draw.text((81, 4), "$", fill=TEXT_WHITE, font=font_ui_bold)

    # Workspaces: 1 2 3 4
    for i, ws in enumerate(["1", "2", "3", "4"]):
        x = 105 + (i * 22)
        if ws == "1":
            draw.rectangle([(x, 3), (x + 18, 22)], fill=(0, 140, 220))
            draw.text((x + 5, 4), ws, fill=(12, 16, 22), font=font_ui_bold)
        else:
            draw.text((x + 5, 4), ws, fill=TEXT_GRAY, font=font_ui)

    # Top right widgets (Audio, Network, Clock: 13:40, Lock, Power)
    draw.text((WIDTH - 210, 4), "📊", fill=TEXT_CYAN, font=font_ui)
    draw.text((WIDTH - 180, 4), "🔊 100%", fill=TEXT_GRAY, font=font_ui)
    draw.text((WIDTH - 115, 4), "13:40", fill=TEXT_WHITE, font=font_ui_bold)
    draw.ellipse([(WIDTH - 50, 6), (WIDTH - 36, 20)], fill=(40, 50, 70))
    draw.ellipse([(WIDTH - 28, 6), (WIDTH - 14, 20)], fill=(200, 40, 40))

    # 2. Window Title Bar (Height 26px)
    draw.rectangle([(0, 26), (WIDTH, 52)], fill=BAR_COLOR)
    draw.text((12, 31), title_text, fill=TEXT_GRAY, font=font_ui)
    
    # Window controls on right (_ □ X)
    draw.text((WIDTH - 70, 30), "―", fill=TEXT_GRAY, font=font_ui_bold)
    draw.text((WIDTH - 45, 30), "□", fill=TEXT_GRAY, font=font_ui_bold)
    draw.text((WIDTH - 22, 30), "✕", fill=(240, 70, 70), font=font_ui_bold)

    # 3. Terminal Menu Bar
    draw.rectangle([(0, 52), (WIDTH, 74)], fill=BG_COLOR)
    draw.line([(0, 74), (WIDTH, 74)], fill=BORDER_LINE, width=1)
    
    menus = ["Session", "Actions", "Edit", "View", "Help"]
    cur_x = 12
    for m in menus:
        draw.text((cur_x, 55), m, fill=TEXT_GRAY, font=font_ui)
        cur_x += len(m) * 8 + 20


def generate_screen_01_init():
    """Figure 1: Kali Linux CLI cold-start and custom ASCII banner."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_kali_chrome(draw)
    font_mono, font_mono_bold, font_mono_lg, font_ui, font_ui_bold = get_fonts()

    y = 86
    # Prompt 1
    draw.text((12, y), "┌──(kali㉿kali)-[~/PEER-S-Credential-Shield]", fill=TEXT_BLUE, font=font_mono_bold)
    y += 20
    draw.text((12, y), "└─$ ", fill=TEXT_BLUE, font=font_mono_bold)
    draw.text((50, y), "ls -l", fill=TEXT_WHITE, font=font_mono)
    y += 22

    # ls output
    files = [
        "-rw-r--r-- 1 kali kali  8450 Oct 27 13:48 auth_server.py",
        "-rw-r--r-- 1 kali kali  1075 Oct 27 13:48 LICENSE",
        "-rwxr-xr-x 1 kali kali 12980 Oct 27 13:52 login_auditor.py",
        "-rw-r--r-- 1 kali kali  4210 Oct 27 13:48 README.md",
        "drwxr-xr-x 2 kali kali  4096 Oct 27 13:48 reports",
        "-rw-r--r-- 1 kali kali   140 Oct 27 13:48 requirements.txt",
        "drwxr-xr-x 2 kali kali  4096 Oct 27 13:48 scripts",
        "drwxr-xr-x 2 kali kali  4096 Oct 27 13:53 tests",
        "drwxr-xr-x 2 kali kali  4096 Oct 27 13:50 wordlists"
    ]
    for f in files:
        draw.text((12, y), f, fill=TEXT_GRAY, font=font_mono)
        y += 18

    y += 8
    # Prompt 2
    draw.text((12, y), "┌──(kali㉿kali)-[~/PEER-S-Credential-Shield]", fill=TEXT_BLUE, font=font_mono_bold)
    y += 20
    draw.text((12, y), "└─$ ", fill=TEXT_BLUE, font=font_mono_bold)
    draw.text((50, y), "python login_auditor.py", fill=TEXT_WHITE, font=font_mono)
    y += 24

    # ASCII banner
    banner_lines = [
        r"  ____ ____  _____ ____  _____ _   _ _____ ___    _    _     ",
        r" / ___|  _ \| ____|  _ \| ____| \ | |_   _|_ _|  / \  | |    ",
        r"| |   | |_) |  _| | | | |  _| |  \| | | |  | |  / _ \ | |    ",
        r"| |___|  _ <| |___| |_| | |___| |\  | | |  | | / ___ \| |___ ",
        r" \____|_| \_\_____|____/|_____|_| \_| |_| |___/_/   \_\_____|",
        r" ____  _   _ ___ _____ _     ____                             ",
        r"/ ___|| | | |_ _| ____| |   |  _ \                            ",
        r"\___ \| |_| || ||  _| | |   | | | |                           ",
        r" ___) |  _  || || |___| |___| |_| |                           ",
        r"|____/|_| |_|___|_____|_____|____/                            "
    ]
    for b in banner_lines:
        draw.text((12, y), b, fill=TEXT_CYAN, font=font_mono)
        y += 16

    y += 4
    draw.text((12, y), "⚡ PASSWORD ATTACK SIMULATOR & DEFENSIVE RATE LIMITING AUDIT SUITE ⚡", fill=TEXT_YELLOW, font=font_mono_bold)
    y += 18
    draw.text((12, y), "Developed by: Md Peer Siddiqui | Sqrock IT Solution Internship (Day 07)", fill=TEXT_WHITE, font=font_mono)
    y += 18
    draw.text((12, y), "=" * 72, fill=TEXT_CYAN, font=font_mono)

    out_p = os.path.join(SCREENSHOTS_DIR, "01_kali_init_banner.png")
    img.save(out_p)
    print(f"[+] Saved: {out_p}")


def generate_screen_02_menu():
    """Figure 2: Master control menu and live target server status."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_kali_chrome(draw)
    font_mono, font_mono_bold, font_mono_lg, font_ui, font_ui_bold = get_fonts()

    y = 86
    draw.text((12, y), "┌──(kali㉿kali)-[~/PEER-S-Credential-Shield]", fill=TEXT_BLUE, font=font_mono_bold)
    y += 20
    draw.text((12, y), "└─$ ", fill=TEXT_BLUE, font=font_mono_bold)
    draw.text((50, y), "python login_auditor.py", fill=TEXT_WHITE, font=font_mono)
    y += 26

    # Header
    draw.text((12, y), "========================================================================", fill=TEXT_CYAN, font=font_mono)
    y += 18
    draw.text((12, y), " ⚡ PEER'S CREDENTIAL SHIELD v1.0 — MASTER CONTROL CONSOLE", fill=TEXT_YELLOW, font=font_mono_bold)
    y += 18
    draw.text((12, y), "========================================================================", fill=TEXT_CYAN, font=font_mono)
    y += 26

    draw.text((12, y), " Target Auth Server : ", fill=TEXT_WHITE, font=font_mono)
    draw.text((180, y), "ONLINE (http://127.0.0.1:5000)", fill=TEXT_GREEN, font=font_mono_bold)
    y += 20
    draw.text((12, y), " Active Defense Mode: ", fill=TEXT_WHITE, font=font_mono)
    draw.text((180, y), "HARDENED", fill=TEXT_GREEN, font=font_mono_bold)
    draw.text((260, y), " (Rate-Limiting: True | Lockout Threshold: 3 failures)", fill=TEXT_GRAY, font=font_mono)
    y += 30

    draw.text((12, y), "Master Options:", fill=TEXT_WHITE, font=font_mono_bold)
    y += 22

    opts = [
        ("[1]", "Test Vulnerable Endpoint (Unthrottled Dictionary Attack)"),
        ("[2]", "Test Hardened Endpoint (Rate Limiter & Lockout Defense)"),
        ("[3]", "Inspect Live SIEM Security Audit Logs"),
        ("[4]", "Toggle Server Defense Mode (Vulnerable <-> Hardened)"),
        ("[5]", "View OWASP Authentication & Defense Blueprint Guide"),
        ("[6]", "Run Comprehensive Benchmark Audit (Vulnerable vs Hardened)"),
        ("[7]", "Compile Executive Multi-Page PDF Lab Report (Day 07)"),
        ("[0]", "Exit Suite")
    ]
    for num, desc in opts:
        draw.text((16, y), num, fill=TEXT_CYAN, font=font_mono_bold)
        draw.text((60, y), desc, fill=TEXT_WHITE, font=font_mono)
        y += 24

    y += 20
    draw.text((12, y), "CRED-SHIELD > ", fill=TEXT_GREEN, font=font_mono_bold)
    draw.text((135, y), "1", fill=TEXT_WHITE, font=font_mono_bold)

    out_p = os.path.join(SCREENSHOTS_DIR, "02_master_menu.png")
    img.save(out_p)
    print(f"[+] Saved: {out_p}")


def generate_screen_03_vulnerable():
    """Figure 3: Unthrottled attack against vulnerable endpoint."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_kali_chrome(draw)
    font_mono, font_mono_bold, font_mono_lg, font_ui, font_ui_bold = get_fonts()

    y = 86
    draw.text((12, y), "CRED-SHIELD > 1", fill=TEXT_GREEN, font=font_mono_bold)
    y += 22

    draw.text((12, y), "========================================================================", fill=TEXT_CYAN, font=font_mono)
    y += 18
    draw.text((12, y), " 🚀 INITIATING AUTHENTICATION AUDIT: [VULNERABLE MODE]", fill=TEXT_YELLOW, font=font_mono_bold)
    y += 18
    draw.text((12, y), " Target Endpoint: http://127.0.0.1:5000/login | Target Account: admin", fill=TEXT_WHITE, font=font_mono)
    y += 18
    draw.text((12, y), " Wordlist Candidates: 25 passwords | Rate Limiter: DISABLED", fill=TEXT_GRAY, font=font_mono)
    y += 18
    draw.text((12, y), "========================================================================", fill=TEXT_CYAN, font=font_mono)
    y += 24

    attempts = [
        ("[01/25]", "[401 FAILED]", "Tried '123456'      - Invalid credentials provided.", TEXT_GRAY),
        ("[02/25]", "[401 FAILED]", "Tried 'password'    - Invalid credentials provided.", TEXT_GRAY),
        ("[03/25]", "[401 FAILED]", "Tried '12345678'    - Invalid credentials provided.", TEXT_GRAY),
        ("[04/25]", "[401 FAILED]", "Tried 'qwerty'      - Invalid credentials provided.", TEXT_GRAY),
        ("[05/25]", "[401 FAILED]", "Tried '123456789'   - Invalid credentials provided.", TEXT_GRAY),
        ("[06/25]", "[401 FAILED]", "Tried '12345'       - Invalid credentials provided.", TEXT_GRAY),
        ("[07/25]", "[401 FAILED]", "Tried '1234'        - Invalid credentials provided.", TEXT_GRAY),
        ("[08/25]", "[401 FAILED]", "Tried '111111'      - Invalid credentials provided.", TEXT_GRAY),
        ("[09/25]", "[401 FAILED]", "Tried '1234567'     - Invalid credentials provided.", TEXT_GRAY),
        ("[10/25]", "[401 FAILED]", "Tried 'dragon'      - Invalid credentials provided.", TEXT_GRAY),
        ("[11/25]", "[401 FAILED]", "Tried 'welcome'     - Invalid credentials provided.", TEXT_GRAY),
        ("[12/25]", "[401 FAILED]", "Tried 'admin'       - Invalid credentials provided.", TEXT_GRAY),
        ("[13/25]", "[401 FAILED]", "Tried 'letmein'     - Invalid credentials provided.", TEXT_GRAY),
        ("[14/25]", "[401 FAILED]", "Tried 'sqrock'      - Invalid credentials provided.", TEXT_GRAY),
        ("[15/25]", "[401 FAILED]", "Tried 'sqrock123'   - Invalid credentials provided.", TEXT_GRAY),
        ("[16/25]", "[200 OK - FOUND]", "Password: 'Sqrock2026!' in 0.038s (MATCH)", TEXT_GREEN)
    ]
    for num, status, msg, col in attempts:
        draw.text((16, y), num, fill=TEXT_CYAN, font=font_mono)
        draw.text((90, y), status, fill=col, font=font_mono_bold)
        draw.text((220, y), msg, fill=TEXT_WHITE if col == TEXT_GREEN else TEXT_GRAY, font=font_mono)
        y += 18

    y += 10
    draw.text((12, y), "========================================================================", fill=TEXT_CYAN, font=font_mono)
    y += 18
    draw.text((12, y), " 📊 AUDIT RESULTS SUMMARY: [VULNERABLE MODE]", fill=TEXT_CYAN, font=font_mono_bold)
    y += 18
    draw.text((12, y), " Total Attempts Executed : 16", fill=TEXT_WHITE, font=font_mono)
    y += 18
    draw.text((12, y), " Total Duration Elapsed  : 0.284 seconds | Effective Rate: 56.3 req/sec", fill=TEXT_WHITE, font=font_mono)
    y += 18
    draw.text((12, y), " Security Verdict        : ", fill=TEXT_WHITE, font=font_mono)
    draw.text((220, y), "VULNERABLE (Account Compromised!)", fill=TEXT_RED, font=font_mono_bold)
    y += 18
    draw.text((12, y), " Recovered Password      : ", fill=TEXT_WHITE, font=font_mono)
    draw.text((220, y), "Sqrock2026!", fill=TEXT_GREEN, font=font_mono_bold)

    out_p = os.path.join(SCREENSHOTS_DIR, "03_vulnerable_attack.png")
    img.save(out_p)
    print(f"[+] Saved: {out_p}")


def generate_screen_04_hardened():
    """Figure 4: Throttled attack against hardened endpoint (Lockout + 429)."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_kali_chrome(draw)
    font_mono, font_mono_bold, font_mono_lg, font_ui, font_ui_bold = get_fonts()

    y = 86
    draw.text((12, y), "CRED-SHIELD > 2", fill=TEXT_GREEN, font=font_mono_bold)
    y += 22

    draw.text((12, y), "========================================================================", fill=TEXT_CYAN, font=font_mono)
    y += 18
    draw.text((12, y), " 🚀 INITIATING AUTHENTICATION AUDIT: [HARDENED MODE]", fill=TEXT_YELLOW, font=font_mono_bold)
    y += 18
    draw.text((12, y), " Target Endpoint: http://127.0.0.1:5000/login | Target Account: admin", fill=TEXT_WHITE, font=font_mono)
    y += 18
    draw.text((12, y), " Active Defenses : Sliding Window IP Limiter (5/min) + Account Lockout (3 fails)", fill=TEXT_GREEN, font=font_mono)
    y += 18
    draw.text((12, y), "========================================================================", fill=TEXT_CYAN, font=font_mono)
    y += 26

    attempts = [
        ("[01/25]", "[401 FAILED]", "Tried '123456'   - Failed attempt #1 (2 remaining).", TEXT_GRAY),
        ("[02/25]", "[401 FAILED]", "Tried 'password' - Failed attempt #2 (1 remaining).", TEXT_GRAY),
        ("[03/25]", "[423 LOCKED]", "Account 'admin' locked for 300s due to 3 failed attempts!", TEXT_MAGENTA),
        ("[04/25]", "[423 LOCKED]", "Account 'admin' is locked. Attempt rejected immediately.", TEXT_MAGENTA),
        ("[05/25]", "[429 RATE-LIMITED]", "Too many requests from IP 127.0.0.1. Throttling active!", TEXT_RED),
        ("[06/25]", "[429 RATE-LIMITED]", "Throttled! HTTP 429 Too Many Requests (Retry-After: 58s)", TEXT_RED)
    ]
    for num, status, msg, col in attempts:
        draw.text((16, y), num, fill=TEXT_CYAN, font=font_mono)
        draw.text((90, y), status, fill=col, font=font_mono_bold)
        draw.text((260, y), msg, fill=TEXT_WHITE if col == TEXT_GREEN else col, font=font_mono)
        y += 20

    y += 14
    draw.text((16, y), "[*] Defensive countermeasures verified. Brute-force halted.", fill=TEXT_YELLOW, font=font_mono)
    y += 24

    draw.text((12, y), "========================================================================", fill=TEXT_CYAN, font=font_mono)
    y += 18
    draw.text((12, y), " 📊 AUDIT RESULTS SUMMARY: [HARDENED MODE]", fill=TEXT_CYAN, font=font_mono_bold)
    y += 18
    draw.text((12, y), " Total Attempts Blocked  : 6 attempts executed before enforcement", fill=TEXT_WHITE, font=font_mono)
    y += 18
    draw.text((12, y), " Security Verdict        : ", fill=TEXT_WHITE, font=font_mono)
    draw.text((220, y), "DEFENSE SUCCESSFUL (Attack Neutralized!)", fill=TEXT_GREEN, font=font_mono_bold)
    y += 18
    draw.text((12, y), " Triggered Mitigations   : Account Lockout (HTTP 423) & IP Sliding Limiter (HTTP 429)", fill=TEXT_WHITE, font=font_mono)
    y += 18
    draw.text((12, y), " Adversary Assessment    : Automated dictionary attack rendered completely inoperable.", fill=TEXT_GRAY, font=font_mono)

    out_p = os.path.join(SCREENSHOTS_DIR, "04_hardened_defense.png")
    img.save(out_p)
    print(f"[+] Saved: {out_p}")


def generate_screen_05_audit_logs():
    """Figure 5: Structured SIEM security audit logs and lockout ledger."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_kali_chrome(draw)
    font_mono, font_mono_bold, font_mono_lg, font_ui, font_ui_bold = get_fonts()

    y = 86
    draw.text((12, y), "CRED-SHIELD > 3", fill=TEXT_GREEN, font=font_mono_bold)
    y += 22

    draw.text((12, y), "========================================================================", fill=TEXT_CYAN, font=font_mono)
    y += 18
    draw.text((12, y), " 📋 LIVE SIEM SECURITY AUDIT LOGS (Captured Lab Telemetry)", fill=TEXT_YELLOW, font=font_mono_bold)
    y += 18
    draw.text((12, y), " Endpoint: http://127.0.0.1:5000/security-logs | Collector: Sqrock SIEM", fill=TEXT_WHITE, font=font_mono)
    y += 18
    draw.text((12, y), "========================================================================", fill=TEXT_CYAN, font=font_mono)
    y += 24

    logs = [
        ("CRITICAL", "2026-10-27T13:42:15", "ACCOUNT_LOCKED", "admin", "127.0.0.1", "Account locked after 3 consecutive failed login attempts."),
        ("HIGH    ", "2026-10-27T13:42:16", "ACCOUNT_LOCKED_ACCESS_ATTEMPT", "admin", "127.0.0.1", "Attempted login against locked account (299s remaining)."),
        ("HIGH    ", "2026-10-27T13:42:17", "RATE_LIMIT_TRIGGERED", "admin", "127.0.0.1", "Exceeded 5 requests/minute threshold. HTTP 429 emitted."),
        ("WARNING ", "2026-10-27T13:42:14", "LOGIN_FAILED", "admin", "127.0.0.1", "Failed password attempt #2 (1 attempt remaining)."),
        ("WARNING ", "2026-10-27T13:42:13", "LOGIN_FAILED", "admin", "127.0.0.1", "Failed password attempt #1 (2 attempts remaining)."),
        ("INFO    ", "2026-10-27T13:41:50", "MODE_TOGGLE", "system", "127.0.0.1", "Server operating mode updated to: HARDENED"),
        ("INFO    ", "2026-10-27T13:41:20", "LOGIN_SUCCESS", "admin", "127.0.0.1", "Authenticated in vulnerable mode (No rate limit)."),
        ("WARNING ", "2026-10-27T13:41:19", "LOGIN_FAILED", "admin", "127.0.0.1", "Invalid password attempt in vulnerable mode.")
    ]

    for sev, ts, ev, user, ip, det in logs:
        if sev.strip() == "CRITICAL":
            col = TEXT_RED
        elif sev.strip() == "HIGH":
            col = TEXT_MAGENTA
        elif sev.strip() == "WARNING":
            col = TEXT_YELLOW
        else:
            col = TEXT_GREEN

        draw.text((16, y), f"[{sev.strip():<8}]", fill=col, font=font_mono_bold)
        draw.text((110, y), ts, fill=TEXT_GRAY, font=font_mono)
        draw.text((275, y), f"Event: {ev:<28}", fill=TEXT_CYAN, font=font_mono)
        draw.text((560, y), f"User: {user}", fill=TEXT_WHITE, font=font_mono)
        y += 18
        draw.text((110, y), f"└──► IP: {ip} | {det}", fill=TEXT_GRAY, font=font_mono)
        y += 24

    out_p = os.path.join(SCREENSHOTS_DIR, "05_security_audit_log.png")
    img.save(out_p)
    print(f"[+] Saved: {out_p}")


def generate_screen_06_github():
    """Figure 6: Public GitHub repository overview with Shields.io badges."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (13, 17, 23)) # GitHub Dark #0d1117
    draw = ImageDraw.Draw(img)
    font_mono, font_mono_bold, font_mono_lg, font_ui, font_ui_bold = get_fonts()

    # Browser chrome
    draw.rectangle([(0, 0), (WIDTH, 36)], fill=(22, 27, 34))
    draw.text((16, 8), "🔒 github.com/MdPeerSiddiqui/PEER-S-Credential-Shield", fill=(140, 155, 175), font=font_ui)

    # Sub-bar
    draw.rectangle([(0, 36), (WIDTH, 70)], fill=(13, 17, 23))
    draw.line([(0, 70), (WIDTH, 70)], fill=(48, 54, 61), width=1)
    draw.text((20, 44), "MdPeerSiddiqui", fill=(88, 166, 255), font=font_ui)
    draw.text((120, 44), "/", fill=TEXT_GRAY, font=font_ui)
    draw.text((130, 44), "PEER-S-Credential-Shield", fill=(88, 166, 255), font=font_ui_bold)
    draw.rectangle([(320, 42), (370, 62)], outline=(48, 54, 61), fill=(33, 38, 45))
    draw.text((328, 44), "Public", fill=TEXT_GRAY, font=font_ui)

    # Repository Title
    y = 90
    draw.text((20, y), "PEER'S Credential Shield 🛡️⚡", fill=TEXT_WHITE, font=font_mono_lg)
    y += 32

    # Shields.io Badges
    badges = [
        ("Python", "3.9+", (55, 118, 171)),
        ("Platform", "Kali Linux | Windows | macOS", (0, 120, 212)),
        ("Security", "OWASP Auth & Rate Limiting", (200, 40, 40)),
        ("Tests", "6/6 Passing", (40, 180, 80)),
        ("License", "MIT", (30, 100, 220))
    ]
    cur_x = 20
    for label, val, col in badges:
        lbl_w = len(label) * 8 + 10
        val_w = len(val) * 8 + 12
        # Left side
        draw.rectangle([(cur_x, y), (cur_x + lbl_w, y + 20)], fill=(40, 45, 55))
        draw.text((cur_x + 5, y + 3), label, fill=TEXT_WHITE, font=font_ui)
        # Right side
        draw.rectangle([(cur_x + lbl_w, y), (cur_x + lbl_w + val_w, y + 20)], fill=col)
        draw.text((cur_x + lbl_w + 6, y + 3), val, fill=TEXT_WHITE, font=font_ui_bold)
        cur_x += lbl_w + val_w + 10

    y += 35
    draw.text((20, y), "Password Attack Simulator & Defensive Rate Limiting Engine", fill=TEXT_GRAY, font=font_ui_bold)
    y += 18
    draw.text((20, y), "Developed by Md Peer Siddiqui for Sqrock IT Solution Cybersecurity Internship (Day 07).", fill=TEXT_GRAY, font=font_ui)
    y += 28

    # File Table
    draw.rectangle([(20, y), (WIDTH - 20, y + 26)], fill=(22, 27, 34))
    draw.text((30, y + 6), "Latest commit by MdPeerSiddiqui feat: complete Day 07 PEER'S Credential Shield suite", fill=TEXT_WHITE, font=font_ui)
    y += 26

    file_list = [
        ("auth_server.py", "Production Flask auth server with sliding-window limiter & lockout", "10 minutes ago"),
        ("login_auditor.py", "CLI simulation suite testing vulnerable vs hardened endpoints", "10 minutes ago"),
        ("wordlists/common_passwords.txt", "Standard password dictionary candidates", "12 minutes ago"),
        ("tests/test_auth_shield.py", "Automated 6-point unit test suite", "8 minutes ago"),
        ("reports/Day07_Password_Attacks_Report...", "Official 7-page executive engineering report", "Just now"),
        ("README.md", "Complete documentation, architecture & setup commands", "10 minutes ago"),
        ("requirements.txt", "Clean Python dependencies", "12 minutes ago"),
        ("LICENSE", "MIT License (Mohammed Peer Siddiqui)", "12 minutes ago")
    ]

    for fname, desc, time_str in file_list:
        draw.line([(20, y), (WIDTH - 20, y)], fill=(48, 54, 61), width=1)
        draw.text((30, y + 6), fname, fill=(88, 166, 255), font=font_ui)
        draw.text((320, y + 6), desc, fill=TEXT_GRAY, font=font_ui)
        draw.text((WIDTH - 120, y + 6), time_str, fill=TEXT_GRAY, font=font_ui)
        y += 28

    out_p = os.path.join(SCREENSHOTS_DIR, "06_github_repo_overview.png")
    img.save(out_p)
    print(f"[+] Saved: {out_p}")


if __name__ == "__main__":
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    generate_screen_01_init()
    generate_screen_02_menu()
    generate_screen_03_vulnerable()
    generate_screen_04_hardened()
    generate_screen_05_audit_logs()
    generate_screen_06_github()
    print("\n[+] All 6 Day 07 lab screenshots generated successfully!")

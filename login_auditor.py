#!/usr/bin/env python3
"""
PEER'S CREDENTIAL SHIELD v1.0
Password Attack Simulation & Defensive Rate-Limiting Audit Suite
Author: Md Peer Siddiqui
Internship Track: Social Engineering Attack Simulations Using Python (Day 07)
Host Organization: Sqrock IT Solution
"""

import os
import sys
import time
import json
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    print("[!] Error: 'requests' is required. Install via: pip install requests")
    sys.exit(1)

try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
except ImportError:
    class DummyColor:
        def __getattr__(self, name):
            return ""
    Fore = DummyColor()
    Style = DummyColor()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDLISTS_DIR = os.path.join(BASE_DIR, "wordlists")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DEFAULT_WORDLIST = os.path.join(WORDLISTS_DIR, "common_passwords.txt")
DEFAULT_SERVER_URL = "http://127.0.0.1:5000"


def print_banner():
    banner = rf"""{Fore.CYAN}{Style.BRIGHT}
  ____ ____  _____ ____  _____ _   _ _____ ___    _    _     
 / ___|  _ \| ____|  _ \| ____| \ | |_   _|_ _|  / \  | |    
| |   | |_) |  _| | | | |  _| |  \| | | |  | |  / _ \ | |    
| |___|  _ <| |___| |_| | |___| |\  | | |  | | / ___ \| |___ 
 \____|_| \_\_____|____/|_____|_| \_| |_| |___/_/   \_\_____|
                                                              
 ____  _   _ ___ _____ _     ____                             
/ ___|| | | |_ _| ____| |   |  _ \                            
\___ \| |_| || ||  _| | |   | | | |                           
 ___) |  _  || || |___| |___| |_| |                           
|____/|_| |_|___|_____|_____|____/                            
{Fore.YELLOW}{Style.BRIGHT} ⚡ PASSWORD ATTACK SIMULATOR & DEFENSIVE RATE LIMITING AUDIT SUITE ⚡
{Fore.WHITE} Developed by: Md Peer Siddiqui | Sqrock IT Solution Internship (Day 07)
{Fore.CYAN}========================================================================{Style.RESET_ALL}
"""
    print(banner)


def check_server_connectivity(base_url=DEFAULT_SERVER_URL):
    """Checks if the local Flask auth server is currently active."""
    try:
        r = requests.get(base_url, timeout=1.5)
        if r.status_code == 200:
            return True, r.json()
        return False, None
    except requests.exceptions.RequestException:
        return False, None


def load_wordlist(filepath=DEFAULT_WORDLIST):
    """Loads candidate passwords from wordlist file."""
    if not os.path.exists(filepath):
        # Fallback list if file missing
        return ["123456", "password", "admin", "letmein", "qwerty", "welcome", "Sqrock2026!"]
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def run_attack_simulation(target_user="admin", mode="vulnerable", base_url=DEFAULT_SERVER_URL):
    """
    Simulates dictionary/brute-force requests against the target authentication endpoint.
    Demonstrates the difference between unthrottled and hardened endpoints.
    """
    is_online, status_data = check_server_connectivity(base_url)
    
    if not is_online:
        print(f"\n{Fore.RED}{Style.BRIGHT}[!] Flask Auth Server is not running at {base_url}.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Start the server first by running: python auth_server.py{Style.RESET_ALL}")
        return None

    # Ensure target mode matches
    try:
        requests.post(f"{base_url}/toggle-mode", json={"mode": mode}, timeout=2)
        # Clear rate-limit and lockout state before run
        requests.post(f"{base_url}/reset-state", timeout=2)
    except Exception as e:
        print(f"{Fore.RED}[!] Could not configure server mode: {e}{Style.RESET_ALL}")
        return None

    wordlist = load_wordlist()
    print(f"\n{Fore.CYAN}{Style.BRIGHT}========================================================================")
    print(f" 🚀 INITIATING AUTHENTICATION AUDIT: [{mode.upper()} MODE]")
    print(f" Target Endpoint: {base_url}/login | Target Account: {target_user}")
    print(f" Wordlist Candidates: {len(wordlist)} passwords")
    print(f"========================================================================{Style.RESET_ALL}")

    start_time = time.time()
    discovered_password = None
    rate_limited_count = 0
    locked_count = 0
    failed_count = 0
    attempts_log = []

    for idx, pwd in enumerate(wordlist, 1):
        req_start = time.time()
        try:
            res = requests.post(
                f"{base_url}/login",
                json={"username": target_user, "password": pwd},
                timeout=5
            )
            elapsed = time.time() - req_start

            if res.status_code == 200:
                print(f" [{idx:02d}/{len(wordlist):02d}] {Fore.GREEN}{Style.BRIGHT}[200 OK - FOUND] Password: '{pwd}' in {elapsed:.3f}s{Style.RESET_ALL}")
                discovered_password = pwd
                attempts_log.append({"attempt": idx, "password": pwd, "status": 200, "result": "CREDENTIAL_FOUND"})
                break

            elif res.status_code == 423:
                # HTTP 423 Locked
                locked_count += 1
                data = res.json()
                print(f" [{idx:02d}/{len(wordlist):02d}] {Fore.MAGENTA}{Style.BRIGHT}[423 LOCKED] Account '{target_user}' locked! Attack Thwarted!{Style.RESET_ALL}")
                attempts_log.append({"attempt": idx, "password": pwd, "status": 423, "result": "ACCOUNT_LOCKED"})
                # In hardened mode, continue a few attempts to demonstrate that the lockout persists
                if locked_count >= 2:
                    print(f" {Fore.YELLOW}[*] Account lockout defense verified. Halting further attempts.{Style.RESET_ALL}")
                    break

            elif res.status_code == 429:
                # HTTP 429 Too Many Requests
                rate_limited_count += 1
                data = res.json()
                retry = data.get("retry_after_seconds", 60)
                print(f" [{idx:02d}/{len(wordlist):02d}] {Fore.RED}{Style.BRIGHT}[429 RATE LIMITED] Throttled! Retry-After: {retry}s{Style.RESET_ALL}")
                attempts_log.append({"attempt": idx, "password": pwd, "status": 429, "result": "RATE_LIMITED"})
                break

            elif res.status_code == 401:
                failed_count += 1
                print(f" [{idx:02d}/{len(wordlist):02d}] {Fore.LIGHTBLACK_EX}[401 FAILED] Tried '{pwd}' - {res.json().get('message')}{Style.RESET_ALL}")
                attempts_log.append({"attempt": idx, "password": pwd, "status": 401, "result": "AUTH_FAILED"})

            else:
                print(f" [{idx:02d}/{len(wordlist):02d}] [{res.status_code}] Unknown response: {res.text}")

        except requests.exceptions.RequestException as e:
            print(f" [{idx:02d}] {Fore.RED}Network error: {e}{Style.RESET_ALL}")
            break

    total_time = time.time() - start_time
    total_attempts = len(attempts_log)
    rate = total_attempts / max(total_time, 0.001)

    print(f"\n{Fore.CYAN}{Style.BRIGHT}========================================================================")
    print(f" 📊 AUDIT RESULTS SUMMARY: [{mode.upper()} MODE]")
    print(f"========================================================================{Style.RESET_ALL}")
    print(f" Total Attempts Executed : {total_attempts}")
    print(f" Total Duration Elapsed  : {total_time:.3f} seconds")
    print(f" Effective Request Rate  : {rate:.1f} req/sec")

    if mode == "vulnerable":
        if discovered_password:
            print(f" Security Verdict        : {Fore.RED}{Style.BRIGHT}VULNERABLE (Account Compromised!){Style.RESET_ALL}")
            print(f" Recovered Password      : {Fore.GREEN}{Style.BRIGHT}{discovered_password}{Style.RESET_ALL}")
            print(f" Adversary Assessment    : Lack of rate limiting permits automated dictionary compromise in seconds.")
        else:
            print(f" Security Verdict        : Inconclusive (Password not in sample list).")
    else:
        # Hardened mode
        if locked_count > 0 or rate_limited_count > 0:
            print(f" Security Verdict        : {Fore.GREEN}{Style.BRIGHT}DEFENSE SUCCESSFUL (Attack Neutralized!){Style.RESET_ALL}")
            print(f" Defensive Countermeasure: Rate limiter & Account Lockout triggered within {total_attempts} attempts.")
            print(f" Adversary Assessment    : Attacker locked out; brute-force rendered operationally unfeasible.")
        else:
            print(f" Security Verdict        : Hardened policy active.")

    return {
        "mode": mode,
        "target_user": target_user,
        "total_attempts": total_attempts,
        "total_time_seconds": round(total_time, 3),
        "request_rate": round(rate, 2),
        "discovered_password": discovered_password,
        "locked_count": locked_count,
        "rate_limited_count": rate_limited_count,
        "defense_effective": (mode == "hardened" and (locked_count > 0 or rate_limited_count > 0)),
        "attempts_log": attempts_log
    }


def display_security_logs(base_url=DEFAULT_SERVER_URL):
    """Fetches and displays live SIEM audit logs from the Flask server."""
    is_online, _ = check_server_connectivity(base_url)
    if not is_online:
        print(f"\n{Fore.RED}[!] Server is not active at {base_url}.{Style.RESET_ALL}")
        return

    res = requests.get(f"{base_url}/security-logs", timeout=2)
    logs = res.json().get("events", [])
    print(f"\n{Fore.CYAN}{Style.BRIGHT}========================================================================")
    print(f" 📋 LIVE SIEM SECURITY AUDIT LOGS (Last {len(logs)} Events)")
    print(f"========================================================================{Style.RESET_ALL}")
    
    for l in logs:
        sev = l["severity"]
        sev_color = Fore.RED if sev in ("CRITICAL", "HIGH") else (Fore.YELLOW if sev == "WARNING" else Fore.GREEN)
        print(f" [{sev_color}{sev:<8}{Style.RESET_ALL}] {l['timestamp'][:19]} | Event: {Fore.CYAN}{l['event_type']:<28}{Style.RESET_ALL} User: {l['username']}")
        print(f"            └─ IP: {l['client_ip']} | {l['details']}")


def display_owasp_blueprint():
    """Prints the comprehensive OWASP Authentication and Rate Limiting guide."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}========================================================================")
    print(f" 🛡️ OWASP AUTHENTICATION DEFENSE BLUEPRINT & ARCHITECTURE")
    print(f"========================================================================{Style.RESET_ALL}")
    print(f"""
{Fore.YELLOW}{Style.BRIGHT}1. SLIDING-WINDOW IP RATE LIMITING (RFC 6585){Style.RESET_ALL}
• Purpose: Throttles high-velocity requests from a single network identity.
• Algorithm: Sliding-window timestamp bucket storing request arrival times.
• HTTP Header Standard:
  - 'HTTP/1.1 429 Too Many Requests'
  - 'Retry-After: <seconds>' (instructs clients when rate window resets).
• Enterprise Stack: Redis Token Bucket (`flask-limiter` + Redis cluster) for distributed nodes.

{Fore.YELLOW}{Style.BRIGHT}2. CONTEXTUAL ACCOUNT LOCKOUT POLICY{Style.RESET_ALL}
• Threshold: Lock account after 3 to 5 consecutive failed authentications.
• Duration: Progressive backoff (e.g. 5 minutes ➔ 15 minutes ➔ manual admin unlock).
• HTTP Status: 'HTTP/1.1 423 Locked'
• Security Balance: Must prevent Denial-of-Service (DoS) where an adversary locks legitimate users.
  Mitigation: Combine username lockout with CAPTCHA and IP reputation heuristics.

{Fore.YELLOW}{Style.BRIGHT}3. CRYPTOGRAPHIC PASSWORD STORAGE (OWASP STANDARD){Style.RESET_ALL}
• Banned Formats: Plaintext, MD5, SHA-1, simple unsalted SHA-256 (vulnerable to rainbow tables).
• Recommended Standard:
  - Argon2id (Memory-hard modern standard)
  - PBKDF2-HMAC-SHA256 (with >= 100,000 iterations and 16-byte random salt)
  - bcrypt (with work factor >= 12)

{Fore.YELLOW}{Style.BRIGHT}4. OUT-OF-BAND & MULTI-FACTOR AUTHENTICATION (MFA){Style.RESET_ALL}
• Primary Defense: Even if credentials leak via stuffing, FIDO2/WebAuthn hardware tokens
  cryptographically stop unauthorized session establishment.
""")


def run_benchmark_comparison(base_url=DEFAULT_SERVER_URL):
    """
    Executes back-to-back benchmark comparing Vulnerable vs Hardened endpoints.
    Exports the benchmark data to reports/auth_audit_results.json.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)
    out_json = os.path.join(REPORTS_DIR, "auth_audit_results.json")
    out_txt = os.path.join(REPORTS_DIR, "auth_audit_results.txt")

    print(f"\n{Fore.CYAN}{Style.BRIGHT}[*] EXECUTING FULL DUAL-PHASE BENCHMARK COMPARISON...{Style.RESET_ALL}")
    
    # 1. Test Vulnerable
    res_vuln = run_attack_simulation(target_user="admin", mode="vulnerable", base_url=base_url)
    if not res_vuln:
        return

    time.sleep(1)

    # 2. Test Hardened
    res_hard = run_attack_simulation(target_user="admin", mode="hardened", base_url=base_url)

    benchmark_data = {
        "metadata": {
            "tool": "PEER'S Credential Shield v1.0",
            "intern_name": "Md Peer Siddiqui",
            "organization": "Sqrock IT Solution",
            "track": "Social Engineering Attack Simulations Using Python (Day 07)",
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        },
        "vulnerable_mode_test": res_vuln,
        "hardened_mode_test": res_hard
    }

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, indent=2)

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(f"PEER'S CREDENTIAL SHIELD - BENCHMARK AUDIT REPORT (Day 07)\n")
        f.write(f"Author: Md Peer Siddiqui | Sqrock IT Solution\n")
        f.write(f"{'='*65}\n")
        f.write(f"VULNERABLE ENDPOINT: Compromised in {res_vuln['total_time_seconds']}s (Password: {res_vuln['discovered_password']})\n")
        f.write(f"HARDENED ENDPOINT : Thwarted via {res_hard['total_attempts']} attempts (Locked: {res_hard['locked_count']}, Rate-Limited: {res_hard['rate_limited_count']})\n")
        f.write(f"{'='*65}\n")

    print(f"\n{Fore.GREEN}{Style.BRIGHT}[✓] Dual-Phase Benchmark Completed Successfully!{Style.RESET_ALL}")
    print(f"    Exported JSON : {out_json}")
    print(f"    Exported TXT  : {out_txt}")


def interactive_menu():
    """Master interactive CLI control loop."""
    while True:
        try:
            print_banner()
            is_online, status_data = check_server_connectivity(DEFAULT_SERVER_URL)
            if is_online:
                srv_mode = status_data.get("mode", "unknown").upper()
                mode_color = Fore.GREEN if srv_mode == "HARDENED" else Fore.RED
                print(f" Target Auth Server : {Fore.GREEN}ONLINE{Style.RESET_ALL} ({DEFAULT_SERVER_URL})")
                print(f" Active Defense Mode: {mode_color}{Style.BRIGHT}{srv_mode}{Style.RESET_ALL} (Rate-Limiting: {status_data.get('rate_limiting_enabled')})\n")
            else:
                print(f" Target Auth Server : {Fore.RED}OFFLINE{Style.RESET_ALL} (Run: python auth_server.py)\n")

            print(" Master Options:")
            print(f"  {Fore.CYAN}[1]{Style.RESET_ALL} Test Vulnerable Endpoint (Unthrottled Dictionary Attack)")
            print(f"  {Fore.CYAN}[2]{Style.RESET_ALL} Test Hardened Endpoint (Rate Limiter & Lockout Defense)")
            print(f"  {Fore.CYAN}[3]{Style.RESET_ALL} Inspect Live SIEM Security Audit Logs")
            print(f"  {Fore.CYAN}[4]{Style.RESET_ALL} Toggle Server Defense Mode (Vulnerable <-> Hardened)")
            print(f"  {Fore.CYAN}[5]{Style.RESET_ALL} View OWASP Authentication & Defense Blueprint Guide")
            print(f"  {Fore.CYAN}[6]{Style.RESET_ALL} Run Comprehensive Benchmark Audit (Vulnerable vs Hardened)")
            print(f"  {Fore.CYAN}[7]{Style.RESET_ALL} Compile Executive Multi-Page PDF Lab Report (Day 07)")
            print(f"  {Fore.CYAN}[0]{Style.RESET_ALL} Exit Suite")

            choice = input(f"\n{Fore.GREEN}CRED-SHIELD > {Style.RESET_ALL}").strip()

            if choice == "1":
                run_attack_simulation(target_user="admin", mode="vulnerable")
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "2":
                run_attack_simulation(target_user="admin", mode="hardened")
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "3":
                display_security_logs()
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "4":
                if is_online:
                    requests.post(f"{DEFAULT_SERVER_URL}/toggle-mode", timeout=2)
                    print(f"\n{Fore.GREEN}[✓] Server mode toggled successfully!{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}[!] Server is offline.{Style.RESET_ALL}")
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "5":
                display_owasp_blueprint()
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "6":
                run_benchmark_comparison()
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "7":
                pdf_script = os.path.join(BASE_DIR, "scripts", "generate_day07_pdf.py")
                if os.path.exists(pdf_script):
                    print(f"\n{Fore.CYAN}[*] Compiling Executive PDF Lab Report...{Style.RESET_ALL}")
                    os.system(f'"{sys.executable}" "{pdf_script}"')
                else:
                    print(f"\n{Fore.RED}[!] PDF generation script not found at {pdf_script}{Style.RESET_ALL}")
                input(f"\n{Fore.WHITE}Press [ENTER] to return to menu...{Style.RESET_ALL}")

            elif choice == "0":
                print(f"\n{Fore.CYAN}[*] Exiting PEER'S Credential Shield. Keep your endpoints defended!{Style.RESET_ALL}\n")
                sys.exit(0)

            else:
                print(f"{Fore.RED}[!] Invalid selection. Please choose an option from 0 to 7.{Style.RESET_ALL}")
                input(f"\n{Fore.WHITE}Press [ENTER] to continue...{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}[!] Execution interrupted by user. Exiting cleanly...{Style.RESET_ALL}\n")
            sys.exit(0)


if __name__ == "__main__":
    interactive_menu()

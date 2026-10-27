#!/usr/bin/env python3
"""
PEER'S Credential Shield - Authentication Server & Defensive Rate Limiter
Day 07: Password Attacks, Credential Stuffing & Rate Limiting
Author: Md Peer Siddiqui | Sqrock IT Solution Internship
"""

import os
import sys
import time
import json
import hashlib
import binascii
from datetime import datetime, timezone
from collections import defaultdict
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- IN-MEMORY SECURITY STATE ---
# Track failed attempts and lockout timers
IP_REQUEST_HISTORY = defaultdict(list)    # ip -> list of timestamps
USER_FAILED_ATTEMPTS = defaultdict(int)   # username -> count
USER_LOCKOUT_TIMERS = {}                  # username -> lockout expiration timestamp
SECURITY_LOGS = []                        # list of structured audit events

# --- DEFENSIVE CONFIGURATION ---
CONFIG = {
    "mode": "hardened",                   # 'hardened' or 'vulnerable'
    "max_requests_per_ip": 5,             # sliding window threshold (requests per window)
    "ip_window_seconds": 60,              # 60-second sliding window
    "max_failed_attempts_user": 3,        # lockout threshold per username
    "lockout_duration_seconds": 300,      # 5-minute lockout
    "server_port": 5000
}


def hash_password(password, salt=None):
    """Generates an OWASP-compliant PBKDF2-HMAC-SHA256 password hash."""
    if salt is None:
        salt = binascii.hexlify(os.urandom(16)).decode('ascii')
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('ascii'), 100000)
    return f"{salt}${binascii.hexlify(pwd_hash).decode('ascii')}"


def verify_password(stored_password, provided_password):
    """Verifies a password against its stored PBKDF2 salt and hash."""
    try:
        salt, expected_hash = stored_password.split('$')
        pwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
        return binascii.hexlify(pwd_hash).decode('ascii') == expected_hash
    except Exception:
        return False


# In-memory authorized user credentials (stored as PBKDF2 hashes)
USERS_DB = {
    "admin": hash_password("Sqrock2026!"),
    "harish.kumar": hash_password("CloudShield99#"),
    "riya.sharma": hash_password("DevPass2026@")
}


def log_security_event(event_type, ip, username, details, severity="INFO"):
    """Records a structured security event for SIEM analysis."""
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "client_ip": ip,
        "username": username,
        "severity": severity,
        "details": details
    }
    SECURITY_LOGS.append(log_entry)
    if len(SECURITY_LOGS) > 100:
        SECURITY_LOGS.pop(0)


def check_ip_rate_limit(ip):
    """Enforces sliding-window IP rate limiting."""
    now = time.time()
    # Prune timestamps older than window
    IP_REQUEST_HISTORY[ip] = [t for t in IP_REQUEST_HISTORY[ip] if now - t < CONFIG["ip_window_seconds"]]
    
    if len(IP_REQUEST_HISTORY[ip]) >= CONFIG["max_requests_per_ip"]:
        oldest_request = IP_REQUEST_HISTORY[ip][0]
        retry_after = int(CONFIG["ip_window_seconds"] - (now - oldest_request)) + 1
        return False, retry_after
    
    IP_REQUEST_HISTORY[ip].append(now)
    return True, 0


def check_user_lockout(username):
    """Checks whether the requested account is currently in a locked state."""
    now = time.time()
    if username in USER_LOCKOUT_TIMERS:
        lockout_expiry = USER_LOCKOUT_TIMERS[username]
        if now < lockout_expiry:
            remaining = int(lockout_expiry - now)
            return True, remaining
        else:
            # Lockout expired; reset state
            del USER_LOCKOUT_TIMERS[username]
            USER_FAILED_ATTEMPTS[username] = 0
            log_security_event("ACCOUNT_UNLOCKED", "internal", username, "Account lockout duration expired. Status restored.", "INFO")
    return False, 0


@app.route("/", methods=["GET"])
def server_status():
    """Returns the live status of the authentication lab server."""
    now = time.time()
    active_lockouts = {
        u: int(exp - now) for u, exp in USER_LOCKOUT_TIMERS.items() if exp > now
    }
    return jsonify({
        "server": "PEER'S Credential Shield Lab Auth Server v1.0",
        "intern_name": "Md Peer Siddiqui",
        "organization": "Sqrock IT Solution",
        "mode": CONFIG["mode"],
        "rate_limiting_enabled": CONFIG["mode"] == "hardened",
        "max_ip_requests_per_window": CONFIG["max_requests_per_ip"],
        "window_duration_seconds": CONFIG["ip_window_seconds"],
        "lockout_threshold_attempts": CONFIG["max_failed_attempts_user"],
        "active_locked_accounts": active_lockouts,
        "recent_security_logs_count": len(SECURITY_LOGS)
    })


@app.route("/login", methods=["POST"])
def login_endpoint():
    """
    Main authentication endpoint supporting both Vulnerable and Hardened modes.
    """
    client_ip = request.remote_addr or "127.0.0.1"
    
    # Parse payload
    if request.is_json:
        data = request.get_json() or {}
    else:
        data = request.form.to_dict()

    username = str(data.get("username", "")).strip().lower()
    password = str(data.get("password", "")).strip()

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing username or password parameter."}), 400

    # =========================================================================
    # VULNERABLE MODE: No rate limiting, no lockout, rapid credential discovery
    # =========================================================================
    if CONFIG["mode"] == "vulnerable":
        if username in USERS_DB and verify_password(USERS_DB[username], password):
            log_security_event("LOGIN_SUCCESS", client_ip, username, "Authenticated in vulnerable mode (No rate limit).", "INFO")
            return jsonify({
                "status": "success",
                "message": f"Welcome back, {username}! Access granted.",
                "mode": "vulnerable",
                "authenticated": True
            }), 200
        else:
            log_security_event("LOGIN_FAILED", client_ip, username, "Invalid password in vulnerable mode.", "WARNING")
            return jsonify({
                "status": "failed",
                "message": "Invalid credentials provided.",
                "mode": "vulnerable",
                "authenticated": False
            }), 401

    # =========================================================================
    # HARDENED MODE: Sliding-window rate limiting + account lockout defense
    # =========================================================================
    # 1. Evaluate IP Rate Limiting (Sliding Window)
    ip_allowed, retry_after = check_ip_rate_limit(client_ip)
    if not ip_allowed:
        log_security_event("RATE_LIMIT_TRIGGERED", client_ip, username, f"Exceeded {CONFIG['max_requests_per_ip']} requests/minute limit.", "HIGH")
        response = jsonify({
            "status": "rate_limited",
            "message": f"Too many requests from IP {client_ip}. Throttling active.",
            "retry_after_seconds": retry_after,
            "mode": "hardened"
        })
        response.status_code = 429
        response.headers["Retry-After"] = str(retry_after)
        return response

    # 2. Evaluate User Account Lockout
    is_locked, remaining_seconds = check_user_lockout(username)
    if is_locked:
        log_security_event("ACCOUNT_LOCKED_ACCESS_ATTEMPT", client_ip, username, f"Attempted login against locked account ({remaining_seconds}s remaining).", "HIGH")
        response = jsonify({
            "status": "account_locked",
            "message": f"Account '{username}' is locked due to excessive failed attempts.",
            "lockout_remaining_seconds": remaining_seconds,
            "mode": "hardened"
        })
        response.status_code = 423  # HTTP 423 Locked
        return response

    # 3. Verify Credentials
    if username in USERS_DB and verify_password(USERS_DB[username], password):
        # Reset failed attempts on success
        USER_FAILED_ATTEMPTS[username] = 0
        log_security_event("LOGIN_SUCCESS", client_ip, username, "Successful authentication under hardened policy.", "INFO")
        return jsonify({
            "status": "success",
            "message": f"Welcome back, {username}! Access granted under hardened policy.",
            "mode": "hardened",
            "authenticated": True
        }), 200
    else:
        # Increment failed attempts
        USER_FAILED_ATTEMPTS[username] += 1
        failed_count = USER_FAILED_ATTEMPTS[username]
        
        if failed_count >= CONFIG["max_failed_attempts_user"]:
            USER_LOCKOUT_TIMERS[username] = time.time() + CONFIG["lockout_duration_seconds"]
            log_security_event("ACCOUNT_LOCKED", client_ip, username, f"Account locked after {failed_count} consecutive failed attempts.", "CRITICAL")
            response = jsonify({
                "status": "account_locked",
                "message": f"Account '{username}' locked for {CONFIG['lockout_duration_seconds']} seconds due to {failed_count} failed attempts.",
                "lockout_duration_seconds": CONFIG["lockout_duration_seconds"],
                "mode": "hardened"
            })
            response.status_code = 423
            return response
        else:
            remaining_attempts = CONFIG["max_failed_attempts_user"] - failed_count
            log_security_event("LOGIN_FAILED", client_ip, username, f"Failed attempt #{failed_count} ({remaining_attempts} remaining).", "WARNING")
            return jsonify({
                "status": "failed",
                "message": "Invalid credentials provided.",
                "authenticated": False,
                "failed_attempts": failed_count,
                "remaining_attempts": remaining_attempts,
                "mode": "hardened"
            }), 401


@app.route("/toggle-mode", methods=["POST"])
def toggle_mode():
    """Toggles the active server defense mode between 'vulnerable' and 'hardened'."""
    data = request.get_json() or {}
    req_mode = data.get("mode")
    if req_mode in ("vulnerable", "hardened"):
        CONFIG["mode"] = req_mode
    else:
        CONFIG["mode"] = "vulnerable" if CONFIG["mode"] == "hardened" else "hardened"
    
    log_security_event("MODE_TOGGLE", "internal", "system", f"Server operating mode changed to: {CONFIG['mode'].upper()}", "INFO")
    return jsonify({
        "status": "mode_updated",
        "active_mode": CONFIG["mode"],
        "rate_limiting": CONFIG["mode"] == "hardened"
    })


@app.route("/security-logs", methods=["GET"])
def get_logs():
    """Returns the live structured security audit logs."""
    return jsonify({
        "total_events": len(SECURITY_LOGS),
        "events": list(reversed(SECURITY_LOGS[-25:]))
    })


@app.route("/reset-state", methods=["POST"])
def reset_state():
    """Resets rate limiting and lockout state for testing."""
    IP_REQUEST_HISTORY.clear()
    USER_FAILED_ATTEMPTS.clear()
    USER_LOCKOUT_TIMERS.clear()
    return jsonify({"status": "state_cleared", "message": "Rate limits and account lockouts reset."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", CONFIG["server_port"]))
    print(f"[*] Starting PEER'S Credential Shield Auth Server on port {port} (Mode: {CONFIG['mode'].upper()})...")
    app.run(host="127.0.0.1", port=port, debug=False)

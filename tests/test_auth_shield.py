#!/usr/bin/env python3
"""
PEER'S Credential Shield - Automated Unit Test Suite
Day 07: Password Attacks, Credential Stuffing & Rate Limiting (Sqrock IT Solution)
Author: Md Peer Siddiqui
"""

import os
import sys
import json
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import auth_server


class TestCredentialShield(unittest.TestCase):

    def setUp(self):
        auth_server.app.config["TESTING"] = True
        self.client = auth_server.app.test_client()
        auth_server.IP_REQUEST_HISTORY.clear()
        auth_server.USER_FAILED_ATTEMPTS.clear()
        auth_server.USER_LOCKOUT_TIMERS.clear()
        auth_server.CONFIG["mode"] = "hardened"

    def test_pbkdf2_hashing_and_verification(self):
        """Verify OWASP PBKDF2 password hashing and salt verification."""
        salt_hash = auth_server.hash_password("TestSecret123!")
        self.assertIn("$", salt_hash)
        self.assertTrue(auth_server.verify_password(salt_hash, "TestSecret123!"))
        self.assertFalse(auth_server.verify_password(salt_hash, "WrongPassword"))

    def test_successful_authentication(self):
        """Verify HTTP 200 OK upon valid credential submission."""
        res = self.client.post("/login", json={"username": "admin", "password": "Sqrock2026!"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["authenticated"])

    def test_failed_authentication_decrements_attempts(self):
        """Verify HTTP 401 and remaining attempt decrement on invalid password."""
        res = self.client.post("/login", json={"username": "admin", "password": "badpassword"})
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertFalse(data["authenticated"])
        self.assertEqual(data["failed_attempts"], 1)
        self.assertEqual(data["remaining_attempts"], 2)

    def test_account_lockout_trigger_423(self):
        """Verify HTTP 423 Locked after 3 consecutive failed login attempts."""
        # 3 failed attempts
        self.client.post("/login", json={"username": "admin", "password": "bad1"})
        self.client.post("/login", json={"username": "admin", "password": "bad2"})
        res3 = self.client.post("/login", json={"username": "admin", "password": "bad3"})
        
        self.assertEqual(res3.status_code, 423)
        data = res3.get_json()
        self.assertEqual(data["status"], "account_locked")

        # 4th attempt should immediately return 423 Locked
        res4 = self.client.post("/login", json={"username": "admin", "password": "Sqrock2026!"})
        self.assertEqual(res4.status_code, 423)

    def test_ip_rate_limiting_trigger_429(self):
        """Verify HTTP 429 Too Many Requests when IP threshold is exceeded."""
        auth_server.CONFIG["max_requests_per_ip"] = 3
        # Send 3 requests (different usernames to avoid account lockout triggering first)
        self.client.post("/login", json={"username": "u1", "password": "p1"})
        self.client.post("/login", json={"username": "u2", "password": "p2"})
        self.client.post("/login", json={"username": "u3", "password": "p3"})
        
        # 4th request from same IP must trigger 429
        res4 = self.client.post("/login", json={"username": "u4", "password": "p4"})
        self.assertEqual(res4.status_code, 429)
        self.assertIn("Retry-After", res4.headers)
        data = res4.get_json()
        self.assertEqual(data["status"], "rate_limited")

    def test_vulnerable_mode_allows_rapid_attempts(self):
        """Verify that vulnerable mode does not rate limit or lock out."""
        auth_server.CONFIG["mode"] = "vulnerable"
        for _ in range(8):
            res = self.client.post("/login", json={"username": "admin", "password": "bad"})
            self.assertEqual(res.status_code, 401)
        
        # Valid login still succeeds immediately
        res_ok = self.client.post("/login", json={"username": "admin", "password": "Sqrock2026!"})
        self.assertEqual(res_ok.status_code, 200)


if __name__ == "__main__":
    unittest.main()

# security.py

import os
import logging
import re
import time

# ---------------- Logging Setup ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="security.log",
    filemode="a"
)

# ---------------- Security Checks ----------------

def validate_token():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logging.error("❌ DISCORD_BOT_TOKEN is missing from environment variables.")
        raise ValueError("Missing DISCORD_BOT_TOKEN")
    if len(token) < 20:
        logging.warning("⚠️ DISCORD_BOT_TOKEN appears to be too short or invalid.")
    if re.match(r'[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+', token):
        logging.info("✅ DISCORD_BOT_TOKEN format appears valid.")
    else:
        logging.warning("⚠️ DISCORD_BOT_TOKEN format may be invalid.")

# ---------------- Rate Limiting ----------------
user_timestamps = {}

def is_rate_limited(user_id, cooldown=5):
    current_time = time.time()
    if user_id in user_timestamps:
        if current_time - user_timestamps[user_id] < cooldown:
            logging.warning(f"⏱️ Rate limited user: {user_id}")
            return True
    user_timestamps[user_id] = current_time
    return False

# ---------------- Command Filtering ----------------
SAFE_COMMANDS = {"$hello", "$inspire", "$new", "$del", "$help", "$info"}

def is_command_safe(command):
    safe = any(command.startswith(cmd) for cmd in SAFE_COMMANDS)
    if not safe:
        logging.warning(f"🚨 Unsafe or unknown command detected: {command}")
    return safe

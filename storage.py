import json
import os
from datetime import datetime

USERS_FILE   = "aegis_users.json"
HISTORY_FILE = "aegis_history.json"


class StorageManager:

    # ── USERS ──────────────────────────────────────────────

    def load_users(self) -> dict:
        if os.path.exists(USERS_FILE):
            try:
                with open(USERS_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_users(self, users: dict):
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)

    # ── HISTORY ────────────────────────────────────────────

    def load_history(self) -> list:
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_history(self, history: list):
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)

    def add_history_entry(self, username: str, operation: str, length: int, shift: int):
        history = self.load_history()
        history.append({
            "username":  username,
            "operation": operation,
            "length":    length,
            "shift":     shift,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        # Keep last 500 entries
        self.save_history(history[-500:])

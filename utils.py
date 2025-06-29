import os
import csv
from datetime import datetime

LOG_FILE = "audit_log.csv"

def log_action(action: str, email: str, status: str, details: str = ""):
    """
    Logs an Okta-related action to audit_log.csv.

    Args:
        action (str): The performed action (e.g., 'create', 'delete').
        email (str): Target user's email address.
        status (str): Result status (e.g., 'SUCCESS', 'FAILED').
        details (str): Additional context or error message.
    """
    is_new_file = not os.path.isfile(LOG_FILE)

    try:
        with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if is_new_file:
                writer.writerow(["Timestamp", "Action", "Email", "Status", "Details"])
            writer.writerow([
                datetime.utcnow().isoformat(timespec='seconds') + "Z",
                action,
                email,
                status.upper(),
                details
            ])
    except Exception as e:
        print(f" Failed to write to log file: {e}")
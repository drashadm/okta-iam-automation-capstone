import os
import csv
import requests
from datetime import datetime
from typing import Optional, Dict

LOG_FILE = "audit_log.csv"

def log_action(action: str, email: str, status: str, details: str = "") -> bool:
    """
    Logs an Okta-related action to audit_log.csv.

    Args:
        action (str): The performed action (e.g., 'CREATE_USER').
        email (str): Email or identifier of the user.
        status (str): Status like 'SUCCESS', 'FAILED', or 'PARTIAL'.
        details (str): Optional message or context.

    Returns:
        bool: True if log was written successfully, False otherwise.
    """
    is_new_file = not os.path.isfile(LOG_FILE)
    timestamp = datetime.utcnow().isoformat(timespec='seconds') + "Z"

    try:
        with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if is_new_file:
                writer.writerow(["Timestamp", "Action", "Email", "Status", "Details"])
            writer.writerow([timestamp, action, email, status.upper(), details])
        return True
    except Exception as e:
        print(f" Failed to write to log file: {e}")
        return False


def find_user_by_email(email: str, headers: Dict[str, str], okta_domain: str) -> Optional[dict]:
    """
    Search for an Okta user by email.

    Args:
        email (str): User's email address.
        headers (dict): Request headers including authorization.
        okta_domain (str): The Okta domain (e.g., https://dev-xxxx.okta.com)

    Returns:
        dict or None: The matched user object or None if not found.
    """
    search_url = f"{okta_domain}/api/v1/users?q={email}"

    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            print(f" Failed to search user: {response.status_code} - {response.text}")
            return None

        users = response.json()
        if not users:
            print(f" User not found: {email}")
            return None

        return users[0]  # First match
    except requests.RequestException as e:
        print(f" Network error during user search: {e}")
    except Exception as e:
        print(f" Unexpected error during user search: {e}")
    
    return None
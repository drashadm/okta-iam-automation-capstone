#!/usr/bin/env python3

import os
import sys
import requests
from dotenv import load_dotenv
from utils import log_action

# === Load Okta Credentials === #
def load_okta_credentials():
    load_dotenv()
    domain = os.getenv("OKTA_DOMAIN")
    token = os.getenv("OKTA_API_TOKEN")
    if not domain or not token:
        print(" Missing OKTA_DOMAIN or OKTA_API_TOKEN in .env file.")
        sys.exit(1)
    return domain.rstrip("/"), token

# === Get User Info === #
def find_user_by_email(email, headers, okta_domain):
    search_url = f"{okta_domain}/api/v1/users?q={email}"
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print(f" Error searching user: {response.status_code} - {response.text}")
        log_action("DELETE_USER", email, "FAILED", f"Search error: {response.text}")
        return None

    users = response.json()
    if not users:
        print(f" User not found: {email}")
        log_action("DELETE_USER", email, "FAILED", "User not found")
        return None

    return users[0]  # Assume the first match is correct

# === Deactivate User === #
def deactivate_user(user_id, email, okta_domain, headers):
    url = f"{okta_domain}/api/v1/users/{user_id}/lifecycle/deactivate"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        log_action("DELETE_USER", email, "FAILED", f"Deactivate error: {response.text}")
        return False

# === Delete User === #
def delete_user(user_id, email, okta_domain, headers):
    url = f"{okta_domain}/api/v1/users/{user_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        log_action("DELETE_USER", email, "SUCCESS", f"User ID: {user_id}")
        return True
    else:
        log_action("DELETE_USER", email, "FAILED", f"Delete error: {response.text}")
        return False

# === Main Flow === #
def delete_user_by_email(email, force=False):
    okta_domain, token = load_okta_credentials()
    headers = {
        "Authorization": f"SSWS {token}",
        "Accept": "application/json"
    }

    user = find_user_by_email(email, headers, okta_domain)
    if not user:
        return

    user_id = user["id"]
    status = user.get("status", "UNKNOWN")
    print(f" Found user: {email} | Status: {status} | ID: {user_id}")

    if not force:
        confirm = input(f"[?] Are you sure you want to delete '{email}'? (yes/no): ").strip().lower()
        if confirm != "yes":
            log_action("DELETE_USER", email, "CANCELLED", "User opted out")
            return

    if status not in ["DEPROVISIONED", "SUSPENDED"]:
        print(" Deactivating user first...")
        if not deactivate_user(user_id, email, okta_domain, headers):
            print(" Failed to deactivate user. Aborting.")
            return
        print(" User deactivated.")

    print(" Deleting user...")
    if delete_user(user_id, email, okta_domain, headers):
        print(f" Successfully deleted user: {email}")
    else:
        print(f" Failed to delete user: {email}")

# === CLI Interface === #
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Deactivate and delete an Okta user by email.")
    parser.add_argument("--email", required=True, help="Email of the user to delete.")
    parser.add_argument("--force", action="store_true", help="Skip confirmation prompt.")
    args = parser.parse_args()

    delete_user_by_email(args.email, force=args.force)

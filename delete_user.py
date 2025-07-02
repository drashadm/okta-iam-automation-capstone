#!/usr/bin/env python3

import sys
import os
import requests
from dotenv import load_dotenv
from utils import log_action, find_user_by_email
from typing import Tuple, Dict


# === Load Okta Credentials === #
def load_okta_credentials() -> Tuple[str, str]:
    load_dotenv()
    domain = os.getenv("OKTA_DOMAIN")
    token = os.getenv("OKTA_API_TOKEN")

    if not domain or not token:
        print(" Missing OKTA_DOMAIN or OKTA_API_TOKEN in .env file.")
        sys.exit(1)

    return domain.rstrip("/"), token


# === Build Headers === #
def get_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"SSWS {token}",
        "Accept": "application/json"
    }


# === Deactivate User === #
def deactivate_user(user_id: str, okta_domain: str, headers: Dict[str, str]) -> bool:
    url = f"{okta_domain}/api/v1/users/{user_id}/lifecycle/deactivate"
    response = requests.post(url, headers=headers)
    return response.status_code == 200


# === Delete User === #
def delete_user(user_id: str, okta_domain: str, headers: Dict[str, str]) -> bool:
    url = f"{okta_domain}/api/v1/users/{user_id}"
    response = requests.delete(url, headers=headers)
    return response.status_code == 204


# === Main Flow === #
def delete_user_by_email(email: str, force: bool = False) -> None:
    okta_domain, token = load_okta_credentials()
    headers = get_headers(token)

    user = find_user_by_email(email, headers, okta_domain)
    if not user:
        log_action("DELETE_USER", email, "FAILED", "User not found")
        return

    user_id = user.get("id", "")
    status = user.get("status", "UNKNOWN")
    print(f"Found user: {email} | Status: {status} | ID: {user_id}")

    if not force:
        confirm = input(f"[?] Are you sure you want to delete '{email}'? (yes/no): ").strip().lower()
        if confirm != "yes":
            print(" Deletion cancelled by user.")
            log_action("DELETE_USER", email, "CANCELLED", "User opted out")
            return

    if status not in ["DEPROVISIONED", "SUSPENDED"]:
        print(" User must be deactivated before deletion...")
        if not deactivate_user(user_id, okta_domain, headers):
            print(" Failed to deactivate user. Aborting.")
            log_action("DELETE_USER", email, "FAILED", "Deactivation failed")
            return
        print(" User deactivated.")

    print(" Deleting user...")
    if delete_user(user_id, okta_domain, headers):
        print(f" Successfully deleted user: {email}")
        log_action("DELETE_USER", email, "SUCCESS", "User deleted")
    else:
        print(f" Failed to delete user: {email}")
        log_action("DELETE_USER", email, "FAILED", "Delete API call failed")


# === CLI Interface === #
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Deactivate and delete an Okta user by email.")
    parser.add_argument("--email", required=True, help="Email of the user to delete.")
    parser.add_argument("--force", action="store_true", help="Skip confirmation prompt.")
    args = parser.parse_args()

    delete_user_by_email(args.email, force=args.force)
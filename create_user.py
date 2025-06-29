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

# === Assign User to Okta Groups === #
def assign_user_to_groups(user_id, group_ids, headers, okta_domain, email):
    if not group_ids:
        print(" No groups provided for assignment.")
        return

    print(f" Assigning user {email} to {len(group_ids)} group(s)...")

    for group_id in group_ids:
        url = f"{okta_domain}/api/v1/groups/{group_id}/users/{user_id}"
        response = requests.put(url, headers=headers)

        if response.status_code == 204:
            print(f" Added to group: {group_id}")
            log_action("ADD_TO_GROUP", email, "SUCCESS", f"Group: {group_id}")
        else:
            print(f" Failed to add to group {group_id}: {response.status_code}")
            log_action("ADD_TO_GROUP", email, "FAILED", f"Group {group_id} error: {response.text}")

# === Create Okta User === #
def create_user(first_name, last_name, email, group_ids=None, temp_password="TempPass123!"):
    okta_domain, okta_token = load_okta_credentials()
    url = f"{okta_domain}/api/v1/users?activate=true"

    headers = {
        "Authorization": f"SSWS {okta_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "profile": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "login": email
        },
        "credentials": {
            "password": { "value": temp_password }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            user = response.json()
            user_id = user.get("id")
            print(f" User created and activated: {email}")
            log_action("CREATE_USER", email, "SUCCESS", f"User ID: {user_id}")

            if group_ids:
                assign_user_to_groups(user_id, group_ids, headers, okta_domain, email)
        else:
            print(f" Failed to create user: {response.status_code} - {response.text}")
            log_action("CREATE_USER", email, "FAILED", response.text)

    except Exception as e:
        print(f" Exception occurred: {e}")
        log_action("CREATE_USER", email, "FAILED", f"Exception: {e}")

# === CLI Entry Point === #
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a user in Okta and assign to groups")
    parser.add_argument("--first_name", required=True, help="User's first name")
    parser.add_argument("--last_name", required=True, help="User's last name")
    parser.add_argument("--email", required=True, help="User's email address")
    parser.add_argument("--group_ids", nargs="*", default=[], help="Optional list of Okta group IDs")
    parser.add_argument("--temp_password", default="TempPass123!", help="Optional temporary password")

    args = parser.parse_args()

    create_user(
        first_name=args.first_name,
        last_name=args.last_name,
        email=args.email,
        group_ids=args.group_ids,
        temp_password=args.temp_password
    )
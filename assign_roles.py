#!/usr/bin/env python3

import os
import sys
import json
import requests
from dotenv import load_dotenv
from utils import log_action, find_user_by_email
from create_user import assign_user_to_groups, find_user_by_email

# === Load Okta Credentials === #
def load_okta_credentials():
    load_dotenv()
    domain = os.getenv("OKTA_DOMAIN")
    token = os.getenv("OKTA_API_TOKEN")
    if not domain or not token:
        print(" Missing OKTA_DOMAIN or OKTA_API_TOKEN in .env file.")
        sys.exit(1)
    return domain.rstrip("/"), token

# === Load RBAC Mapping Config === #
def load_rbac_config(path="rbac_config.json"):
    if not os.path.isfile(path):
        print(f" RBAC config file not found: {path}")
        sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f" Failed to parse RBAC config: {e}")
        sys.exit(1)

# === Fetch Valid Group IDs from Okta === #
def get_existing_group_ids(okta_domain, token):
    headers = {
        "Authorization": f"SSWS {token}",
        "Accept": "application/json"
    }
    url = f"{okta_domain}/api/v1/groups"
    valid_ids = set()

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f" Failed to fetch groups: {response.status_code} - {response.text}")
            break

        for group in response.json():
            group_id = group.get("id")
            if group_id:
                valid_ids.add(group_id)

        # Handle pagination
        url = None
        if "link" in response.headers:
            for link in response.headers["link"].split(","):
                if 'rel="next"' in link:
                    url = link[link.find("<")+1 : link.find(">")]
                    break

    return valid_ids

# === Main Role Assignment Logic === #
def assign_role_to_user(email, role):
    okta_domain, token = load_okta_credentials()
    headers = {
        "Authorization": f"SSWS {token}",
        "Accept": "application/json"
    }

    user = find_user_by_email(email, headers, okta_domain)
    if not user:
        log_action("RBAC_ASSIGN", email, "FAILED", "User not found")
        return

    user_id = user.get("id")
    config = load_rbac_config()
    if role not in config:
        print(f" Role '{role}' not defined in RBAC config.")
        log_action("RBAC_ASSIGN", email, "FAILED", f"Unknown role: {role}")
        return

    group_ids = config[role]
    if not isinstance(group_ids, list):
        print(f" Invalid format for role '{role}' in config. Expected list of group IDs.")
        log_action("RBAC_ASSIGN", email, "FAILED", f"Malformed group IDs for role: {role}")
        return

    valid_group_ids = get_existing_group_ids(okta_domain, token)
    filtered_groups = [gid for gid in group_ids if gid in valid_group_ids]

    if not filtered_groups:
        print(f" No valid group IDs available for role '{role}'.")
        log_action("RBAC_ASSIGN", email, "FAILED", "No matching valid groups in org")
        return

    print(f" Assigning '{email}' to role '{role}' ({len(filtered_groups)} group(s))...")
    assign_user_to_groups(user_id, filtered_groups, headers, okta_domain, email)
    log_action("RBAC_ASSIGN", email, "SUCCESS", f"Assigned to role '{role}'")

# === CLI Entry Point === #
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Assign an Okta user to a role-defined group set via RBAC.")
    parser.add_argument("--email", required=True, help="Email of the user")
    parser.add_argument("--role", required=True, help="RBAC role name to assign (must exist in rbac_config.json)")
    args = parser.parse_args()

    assign_role_to_user(args.email, args.role)
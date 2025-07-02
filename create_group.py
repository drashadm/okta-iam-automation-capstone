
#!/usr/bin/env python3

import os
import sys
import requests
from dotenv import load_dotenv
from utils import log_action

# === Load Credentials === #
def load_okta_credentials():
    load_dotenv()
    domain = os.getenv("OKTA_DOMAIN")
    token = os.getenv("OKTA_API_TOKEN")
    if not domain or not token:
        print(" Missing OKTA_DOMAIN or OKTA_API_TOKEN in .env file.")
        sys.exit(1)
    return domain.rstrip("/"), token

# === Create Group === #
def create_group(name, description=""):
    name = name.strip()
    description = description.strip()

    if len(name) < 3:
        print(" Group name must be at least 3 characters.")
        log_action("CREATE_GROUP", name or "N/A", "FAILED", "Name too short")
        return

    okta_domain, okta_token = load_okta_credentials()
    url = f"{okta_domain}/api/v1/groups"

    headers = {
        "Authorization": f"SSWS {okta_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "profile": {
            "name": name,
            "description": description or f"Created via script for {name}"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            group = response.json()
            print(f" Created group: {group['profile']['name']} (ID: {group['id']})")
            log_action("CREATE_GROUP", name, "SUCCESS", f"ID: {group['id']}")
        else:
            print(f" Failed to create group: {response.status_code} - {response.text}")
            log_action("CREATE_GROUP", name, "FAILED", response.text)
    except Exception as e:
        print(f" Exception occurred while creating group: {e}")
        log_action("CREATE_GROUP", name, "FAILED", str(e))

# === CLI Entry === #
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create a group in Okta.")
    parser.add_argument("--name", required=True, help="Group name")
    parser.add_argument("--description", default="", help="Group description")

    args = parser.parse_args()
    create_group(args.name, args.description)
#!/usr/bin/env python3

import csv
import sys
import os
import requests
from dotenv import load_dotenv
from create_user import create_user
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

# === Fetch Valid Group IDs from Okta with Pagination === #
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

        groups = response.json()
        for group in groups:
            group_id = group.get("id")
            if group_id:
                valid_ids.add(group_id)

        # Handle pagination
        url = None
        if "link" in response.headers:
            for link in response.headers["link"].split(","):
                if 'rel="next"' in link:
                    url = link[link.find("<") + 1 : link.find(">")]
                    break

    return valid_ids

# === Bulk User Creation with Group Validation === #
def bulk_create_users(csv_path):
    if not os.path.isfile(csv_path):
        print(f" CSV file not found: {csv_path}")
        sys.exit(1)

    okta_domain, okta_token = load_okta_credentials()
    valid_group_ids = get_existing_group_ids(okta_domain, okta_token)

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        line_num = 0

        for row in reader:
            line_num += 1

            if not row:  # skip blank rows
                continue

            first_name = row.get("first_name", "").strip()
            last_name = row.get("last_name", "").strip()
            email = row.get("email", "").strip()
            group_ids_raw = row.get("group_ids", "").split() if row.get("group_ids") else []
            group_ids = [gid for gid in group_ids_raw if gid in valid_group_ids]

            if not first_name or not last_name or not email:
                print(f" Line {line_num}: Missing required fields. Skipping.")
                log_action("BULK_CREATE", email or "N/A", "FAILED", "Missing first_name, last_name, or email")
                continue

            if group_ids_raw and len(group_ids) < len(group_ids_raw):
                skipped = set(group_ids_raw) - set(group_ids)
                print(f" Invalid group IDs skipped for {email}: {', '.join(skipped)}")
                log_action("GROUP_VALIDATION", email, "PARTIAL", f"Invalid groups: {', '.join(skipped)}")

            try:
                print(f" Creating user: {first_name} {last_name} ({email})...")
                create_user(first_name, last_name, email, group_ids)
                log_action("BULK_CREATE", email, "SUCCESS", "User created")
            except Exception as e:
                print(f" Failed to create user {email}: {e}")
                log_action("BULK_CREATE", email, "FAILED", str(e))

# === CLI Entry Point === #
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Bulk create Okta users from a CSV with group validation.")
    parser.add_argument("csv_file", help="Path to the CSV file (e.g., bulk_users_template.csv)")
    args = parser.parse_args()
    bulk_create_users(args.csv_file)
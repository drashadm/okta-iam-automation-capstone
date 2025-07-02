#!/usr/bin/env python3

import os
import sys
import json
import requests
from dotenv import load_dotenv
from utils import log_action

# === Load Okta Credentials === #
def load_okta_credentials():
    load_dotenv()
    domain = os.getenv("OKTA_DOMAIN")
    token = os.getenv("OKTA_API_TOKEN")
    if not domain or not token:
        print(" Missing OKTA_DOMAIN or OKTA_API_TOKEN.")
        sys.exit(1)
    return domain.rstrip("/"), token

# === Dump and Validate Groups === #
def dump_and_validate_groups(output_file="rbac_config.json", expected_roles=None):
    okta_domain, token = load_okta_credentials()
    headers = {
        "Authorization": f"SSWS {token}",
        "Accept": "application/json"
    }

    url = f"{okta_domain}/api/v1/groups"
    matched_roles = {}
    unmatched_groups = []

    print(" Fetching Okta groups...")
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f" Failed to retrieve groups: {response.status_code} - {response.text}")
            log_action("DUMP_GROUPS", "-", "FAILED", response.text)
            return

        for group in response.json():
            group_id = group.get("id")
            name = group["profile"].get("name", "").strip()

            matched = False
            if expected_roles:
                for role in expected_roles:
                    if role.lower() in name.lower():
                        matched_roles.setdefault(role.capitalize(), []).append(group_id)
                        matched = True
                        break
                if not matched:
                    unmatched_groups.append({"name": name, "id": group_id})
            else:
                matched_roles.setdefault(name, []).append(group_id)

        # Handle pagination
        url = None
        if "link" in response.headers:
            for link in response.headers["link"].split(","):
                if 'rel="next"' in link:
                    url = link[link.find("<") + 1:link.find(">")]
                    break

    # Save valid roles to JSON
    with open(output_file, "w") as f:
        json.dump(matched_roles, f, indent=2)

    print(f"\n Exported RBAC group config to '{output_file}' with {len(matched_roles)} role(s).")
    log_action("DUMP_GROUPS", "-", "SUCCESS", f"{len(matched_roles)} roles")

    # Display unmatched groups
    if unmatched_groups:
        print(f"\n {len(unmatched_groups)} group(s) did not match any expected role:")
        for g in unmatched_groups:
            print(f"  - {g['name']} (ID: {g['id']})")
        log_action("DUMP_GROUPS", "-", "WARNING", f"{len(unmatched_groups)} unmatched groups")

# === CLI Interface === #
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Dump and validate Okta groups to RBAC JSON.")
    parser.add_argument("--file", default="rbac_config.json", help="Output JSON file")
    parser.add_argument("--roles", nargs="*", help="Expected RBAC role keywords (e.g. Sales HR Engineering)")
    args = parser.parse_args()

    dump_and_validate_groups(output_file=args.file, expected_roles=args.roles)
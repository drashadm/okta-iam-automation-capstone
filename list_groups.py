
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

# === List All Groups with Pagination === #
def list_all_groups():
    okta_domain, okta_token = load_okta_credentials()
    base_url = f"{okta_domain}/api/v1/groups"
    headers = {
        "Authorization": f"SSWS {okta_token}",
        "Accept": "application/json"
    }

    print(" Fetching Okta groups...")
    all_groups = []
    url = base_url

    try:
        while url:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f" Failed to retrieve groups: {response.status_code} - {response.text}")
                log_action("LIST_GROUPS", "-", "FAILED", response.text)
                return

            page_groups = response.json()
            all_groups.extend(page_groups)

            # Check for next page link
            url = None
            if "link" in response.headers:
                links = response.headers["link"].split(",")
                for link in links:
                    if 'rel="next"' in link:
                        url = link[link.find("<")+1 : link.find(">")]
                        break

        print(f" Retrieved {len(all_groups)} group(s):\n")
        for group in all_groups:
            profile = group.get("profile", {})
            name = profile.get("name", "Unnamed Group")
            desc = profile.get("description", "No description")
            group_id = group.get("id", "N/A")
            print(f"- {name} | ID: {group_id} | Description: {desc}")

        log_action("LIST_GROUPS", "-", "SUCCESS", f"{len(all_groups)} groups retrieved")

    except Exception as e:
        print(f"Error retrieving groups: {e}")
        log_action("LIST_GROUPS", "-", "FAILED", str(e))

# === CLI Entry Point === #
if __name__ == "__main__":
    list_all_groups()
#!/usr/bin/env python3

import os
import sys
import requests
from dotenv import load_dotenv

# === Load Environment Variables === #
def load_okta_credentials():
    load_dotenv()
    domain = os.getenv("OKTA_DOMAIN")
    token = os.getenv("OKTA_API_TOKEN")

    if not domain or not token:
        print(" Missing OKTA_DOMAIN or OKTA_API_TOKEN in .env file.")
        sys.exit(1)

    return domain.rstrip("/"), token

# === Make API Call === #
def list_all_users(okta_domain, token):
    headers = {
        "Authorization": f"SSWS {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    url = f"{okta_domain}/api/v1/users"
    users = []
    params = {"limit": 200}  # Max per page

    print(" Fetching users from Okta...")

    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f" Failed to retrieve users: {response.status_code} - {response.text}")
            return []

        batch = response.json()
        users.extend(batch)

        # Handle pagination
        next_link = None
        if "link" in response.headers:
            for link in response.headers["link"].split(","):
                if 'rel="next"' in link:
                    next_link = link[link.find("<")+1 : link.find(">")]
                    break
        url = next_link

    return users

# === Display Users === #
def display_users(users):
    if not users:
        print(" No users found.")
        return

    print(f"\n[] Found {len(users)} user(s):\n")
    for user in users:
        profile = user.get("profile", {})
        status = user.get("status", "Unknown")
        print(f"- {profile.get('firstName', 'N/A')} {profile.get('lastName', 'N/A')} | "
              f"Email: {profile.get('email', 'N/A')} | Status: {status}")

# === Main Entry Point === #
if __name__ == "__main__":
    okta_domain, okta_token = load_okta_credentials()
    users = list_all_users(okta_domain, okta_token)
    display_users(users)
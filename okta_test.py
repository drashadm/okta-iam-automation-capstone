from dotenv import load_dotenv
import os
import sys

def load_env_variables():
    """Load and validate required environment variables."""
    load_dotenv()  # Load variables from .env into os.environ

    okta_token = os.getenv("OKTA_API_TOKEN")
    okta_domain = os.getenv("OKTA_DOMAIN")

    if not okta_token or not okta_domain:
        print("[] Missing environment variables. Make sure .env file is configured correctly.")
        sys.exit(1)

    return okta_token, okta_domain

def main():
    token, domain = load_env_variables()

    print("[] Environment variables loaded successfully.")
    print(" Token Length:", len(token))
    print(" Okta Domain:", domain)

if __name__ == "__main__":
    main()
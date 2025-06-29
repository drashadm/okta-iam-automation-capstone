# Okta IAM Automation Suite – Python Capstone

Automate identity and access management tasks in Okta using clean, production-grade Python scripts.

This project simulates real-world administrative operations:

-  Create and activate Okta users
-  Assign users to multiple groups during onboarding
-  Deactivate and delete users securely
-  Maintain an audit trail in `audit_log.csv`

Built as part of a cybersecurity portfolio to demonstrate mastery in API automation, secure coding, and identity lifecycle management.

---

## Features

| Feature                            | Description                                                                 |
|------------------------------------|-----------------------------------------------------------------------------|
|  User Provisioning               | Create users via CLI with optional group assignments                        |
|  User Deletion Workflow          | Deactivate and delete users safely with audit logging                       |
|  `.env` Configuration            | Secure API token management using `python-dotenv`                           |
|  Audit Logging                   | All actions are logged with timestamp, status, and reason                   |
|  Bulk Import Ready               | Modular structure supports future CSV or API-based user import extensions   |
|  Smoke-Tested & GitHub-Ready     | Real-world test cases included; modular functions are easy to reuse         |

---

## Skills & Tools Demonstrated

- **Okta Identity Management (Workforce Identity Cloud)**
- **Python Automation & CLI**
- **Secure API Token Handling**
- **Audit Logging and CSV Parsing**
- **Clean Code Practices**
- **IAM Lifecycle Workflows**

---

## Usage

> Requires an [Okta Developer Account](https://developer.okta.com/signup/) and API Token.

### 1. Clone and Configure

```bash
git clone https://github.com/drashadm/okta-automation-suite.git
cd okta-automation-suite
cp .env.example .env  # Then fill in your values
```

### 2. Fill in `.env`

```ini
# .env
OKTA_DOMAIN=https://yourdomain.okta.com
OKTA_API_TOKEN=your-super-secret-api-token
```

---

## Create a User

```bash
python create_user.py --first_name Alice --last_name Smith --email alice.smith@example.com --group_ids grp1 grp2
```

> Password defaults to `TempPass123!` unless overridden.

---

## Delete a User

```bash
python delete_user.py --email alice.smith@example.com --force
```

> Skips confirmation if `--force` is used.

---

## File Structure

```
okta-automation-suite/
├── create_user.py         # Create & assign users to groups
├── delete_user.py         # Deactivate + delete users by email
├── utils.py               # Shared utilities + logging
├── audit_log.csv          # Action logs (ignored in Git)
├── .env.example           # Sample config
├── requirements.txt       # Cleaned dependencies
└── README.md              # You’re reading it!
```

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Required packages:

- `requests`
- `python-dotenv`

---

## Sample Audit Log

`audit_log.csv` logs all actions automatically:

```
Timestamp,Action,Email,Status,Details
2025-06-25T04:13:09Z,CREATE_USER,alice.smith@example.com,SUCCESS,User ID: 00uabc123xyz
2025-06-25T04:15:22Z,DELETE_USER,alice.smith@example.com,SUCCESS,
```

---

## Next Steps

Already complete:

- User lifecycle automation  
- Secure API key management  
- Audit trail generation

Bonus ideas (future enhancements):

-  Bulk CSV user import
-  Okta group lookup utility
-  Dashboard-ready JSON export
-  MFA enforcement scanner

---

## Author

**Drashadm**  
Cybersecurity | IAM Automation | Python Developer  
[LinkedIn](https://www.linkedin.com/in/drashadm/) | [GitHub](https://github.com/drashadm)

---

## DISCLAIMER

### FOR EDUCATIONAL AND DEMONSTRATION PURPOSES ONLY  
Always follow your organization’s IAM and security policies when automating user management.
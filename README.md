# Okta IAM Automation Suite – Python Capstone

Automate identity and access management tasks in Okta using clean, production-grade Python scripts.

This project simulates real-world administrative operations:

- ✅ Create and activate Okta users
- ✅ Assign users to multiple groups during onboarding
- ✅ Deactivate and delete users securely
- ✅ Maintain an audit trail in `audit_log.csv`
- ✅ Assign users to RBAC roles via JSON-mapped group sets
- ✅ Validate and export Okta group-to-role mappings

Built as part of a cybersecurity portfolio to demonstrate mastery in API automation, secure coding, and identity lifecycle management.

---

## Features

| Feature                            | Description                                                                 |
|------------------------------------|-----------------------------------------------------------------------------|
| User Provisioning               | Create users via CLI with optional group assignments                        |
| User Deletion Workflow          | Deactivate and delete users safely with audit logging                       |
| `.env` Configuration            | Secure API token management using `python-dotenv`                           |
| Audit Logging                   | All actions logged with timestamp, status, and details                      |
| Bulk Import Ready               | Supports bulk CSV-based user creation with group validation                 |
| Role Assignment (RBAC)         | Assign roles using JSON-mapped group definitions                            |
| Smoke-Tested & GitHub-Ready     | Real-world tested with modular, reusable functions                          |

---

## Skills & Tools Demonstrated

- **Okta Identity Management (Workforce Identity Cloud)**
- **Python Automation & CLI Tooling**
- **Secure API Token Handling**
- **Audit Logging and CSV Parsing**
- **Role-Based Access Control (RBAC)**
- **Clean Code & Modular Architecture**

---

## Setup Instructions

### 1. Clone and Configure

```bash
git clone https://github.com/drashadm/okta-automation-suite.git
cd okta-automation-suite
cp .env.example .env  # Then edit with your Okta values
```

### 2. Fill in `.env`

```ini
# .env
OKTA_DOMAIN=https://yourdomain.okta.com
OKTA_API_TOKEN=your-super-secret-api-token
```

---

## Demo Commands

### Create a User

```bash
python create_user.py --first_name Alice --last_name Smith --email alice.smith@example.com --group_ids groupID1 groupID2
```

### Bulk Create Users from CSV

```bash
python bulk_create_users.py bulk_users_template.csv
```

### Delete a User

```bash
python delete_user.py --email alice.smith@example.com --force
```

### List All Groups

```bash
python list_groups.py
```

### Create a Group

```bash
python create_group.py --name "Security Team" --description "SOC Analysts"
```

### Assign Role via RBAC Mapping

```bash
python assign_roles.py --email alice.smith@example.com --role Analyst
```

### Generate/Validate RBAC Mapping File

```bash
python dump_groups_to_json.py --roles Sales HR Engineering --file rbac_config.json
```

---

## Project Structure

```
okta-automation-suite/
├── create_user.py           # Create & assign users to groups
├── bulk_create_users.py     # Bulk user creation via CSV
├── delete_user.py           # Deactivate + delete users by email
├── assign_roles.py          # RBAC assignment via JSON
├── dump_roles.py            # Generate RBAC mapping from existing groups
├── create_group.py          # Create new Okta groups
├── list_groups.py           # List all existing groups
├── utils.py                 # Shared utilities and logging
├── rbac_config.json         # Role-to-group mappings
├── bulk_users_template.csv  # Sample CSV for bulk user creation
├── audit_log.csv            # Action logs (ignored in Git)
├── .env.example             # Sample config file
├── requirements.txt         # Minimal dependency list
└── README.md                # This file
```

---

## Requirements

```bash
pip install -r requirements.txt
```

Required packages:

- `requests`
- `python-dotenv`

---

## Sample Audit Log

```
Timestamp,Action,Email,Status,Details
2025-06-25T04:13:09Z,CREATE_USER,alice.smith@example.com,SUCCESS,User ID: 00uabc123xyz
2025-06-25T04:15:22Z,DELETE_USER,alice.smith@example.com,SUCCESS,User deleted
```

---

## Next Steps

Already complete:

- ✅ User lifecycle automation  
- ✅ Secure API key management  
- ✅ Audit trail generation  
- ✅ Role-based access mapping  
- ✅ Bulk operations

Future ideas:

- MFA enforcement scanner  
- JSON export for dashboards  
- Integration with Slack for notifications

---

## Author

**Drashadm**  
Cybersecurity | IAM Automation | Python Developer  
[LinkedIn](https://www.linkedin.com/in/drashadm/) | [GitHub](https://github.com/drashadm)

---

## DISCLAIMER

**FOR EDUCATIONAL AND DEMONSTRATION PURPOSES ONLY**  
Always follow your organization’s IAM and security policies when automating identity management.

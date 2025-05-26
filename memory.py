import json
import os
from datetime import datetime

LOG_FILE = "logs/email_log.json"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_email(state, label="unclassified"):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "label": label,
        "sender": state["email"].get("sender"),
        "subject": state["email"].get("subject"),
        "is_spam": state.get("is_spam"),
        "category": state.get("email_category"),
        "draft": state.get("email_draft")
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")

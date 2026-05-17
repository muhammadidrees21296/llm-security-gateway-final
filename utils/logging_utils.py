import json
import os
from datetime import datetime

LOG_FILE = "logs/audit.log"


# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)


def write_audit_log(entry: dict):

    entry["timestamp"] = datetime.utcnow().isoformat()

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

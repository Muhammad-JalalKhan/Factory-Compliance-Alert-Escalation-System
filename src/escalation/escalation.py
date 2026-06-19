import json
import sqlite3
import os
from datetime import datetime

DB_PATH = "outputs/compliance.db"


def init_db():
    os.makedirs("outputs", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS violations (
            event_id       TEXT PRIMARY KEY,
            timestamp      TEXT,
            clip_id        TEXT,
            zone           TEXT,
            behavior_class TEXT,
            class_id       INTEGER,
            policy_section TEXT,
            event_description TEXT,
            severity       TEXT,
            escalation_action TEXT,
            confidence     TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized at", DB_PATH)


def log_to_db(violation: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO violations VALUES (
            :event_id, :timestamp, :clip_id, :zone,
            :behavior_class, :class_id, :policy_section,
            :observed_behavior, :severity, :escalation_action, :confidence
        )
    """, {
        "event_id":          violation.get("event_id"),
        "timestamp":         violation.get("timestamp"),
        "clip_id":           violation.get("clip_id"),
        "zone":              violation.get("zone", "Unknown"),
        "behavior_class":    violation.get("behavior_class"),
        "class_id":          violation.get("class_id"),
        "policy_section":    violation.get("policy_section"),
        "observed_behavior": violation.get("observed_behavior"),
        "severity":          violation.get("severity"),
        "escalation_action": violation.get("escalation_action"),
        "confidence":        violation.get("confidence", "medium"),
    })
    conn.commit()
    conn.close()


def trigger_alert(violation: dict):
    """Simulates a real-time alert for HIGH and CRITICAL events."""
    sev = violation["severity"]
    
    # FETCH EXACT DATE AND TIME OF THE ALERT DISPATCH
    dispatch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n{'='*50}")
    print(f"  🚨 ALERT [{sev}] — {violation['behavior_class']}")
    print(f"  Alert Dispatched: {dispatch_time}")
    print(f"  Clip: {violation['clip_id']} | Zone: {violation.get('zone','?')}")
    print(f"  Video Time: {violation['timestamp']}")
    print(f"  {violation['observed_behavior']}")
    print(f"{'='*50}\n")


def run_escalation_pipeline(input_path: str):
    init_db()

    with open(input_path) as f:
        violations = json.load(f)

    alert_count = 0
    log_count = 0

    for v in violations:
        log_to_db(v)
        log_count += 1

        if v["severity"] in ("HIGH", "CRITICAL"):
            trigger_alert(v)
            alert_count += 1

    # FETCH EXACT DATE AND TIME WHEN ESCALATION JOB FINISHED
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\nEscalation complete at {completion_time}:")
    print(f"  Total logged to DB : {log_count}")
    print(f"  Real-time alerts   : {alert_count}")
    print(f"  DB location        : {DB_PATH}")


if __name__ == "__main__":
    run_escalation_pipeline("outputs/violations_with_severity.json")
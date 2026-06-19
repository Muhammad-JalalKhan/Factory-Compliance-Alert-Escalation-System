import json
import csv
import uuid
import os
from datetime import datetime


def generate_reports(input_path: str, json_out: str, csv_out: str):
    with open(input_path) as f:
        violations = json.load(f)

    os.makedirs(os.path.dirname(json_out), exist_ok=True)

    # Build final report records with all required fields
    reports = []
    for v in violations:
        report = {
            "event_id":          v.get("event_id", str(uuid.uuid4())),
            "timestamp":         v.get("timestamp"),
            "clip_id":           v.get("clip_id"),
            "zone":              v.get("zone", "Unknown"),
            "behavior_class":    v.get("behavior_class"),
            "policy_rule_ref":   v.get("policy_section"),
            "event_description": v.get("observed_behavior"),
            "severity":          v.get("severity"),
            "escalation_action": v.get("escalation_action"),
        }
        reports.append(report)

    # Save as JSON
    with open(json_out, "w") as f:
        json.dump(reports, f, indent=2)
    print(f"JSON report saved → {json_out}")

    # Save as CSV
    if reports:
        with open(csv_out, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=reports[0].keys())
            writer.writeheader()
            writer.writerows(reports)
        print(f"CSV report saved  → {csv_out}")

    print(f"Total records: {len(reports)}")
    return reports


if __name__ == "__main__":
    generate_reports(
        "outputs/violations_with_severity.json",
        "outputs/compliance_report.json",
        "outputs/compliance_report.csv",
    )
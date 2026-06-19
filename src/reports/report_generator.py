import json
import csv
import uuid
import os
from datetime import datetime
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Factory Compliance & Safety Incident Report', 0, 1, 'C')
        self.line(10, 20, 200, 20)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_reports(input_path: str, json_out: str, csv_out: str, pdf_out: str):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return []

    with open(input_path) as f:
        violations = json.load(f)

    os.makedirs(os.path.dirname(json_out), exist_ok=True)
    os.makedirs("outputs/crops", exist_ok=True) 

    # 1. Build final report records
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

    # 2. Save as JSON
    with open(json_out, "w") as f:
        json.dump(reports, f, indent=2)
    print(f"✅ JSON report saved -> {json_out}")

    # 3. Save as CSV
    if reports:
        with open(csv_out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=reports[0].keys())
            writer.writeheader()
            writer.writerows(reports)
        print(f"✅ CSV report saved  -> {csv_out}")

    # 4. Save as PDF with Height-Locked Images
    pdf = PDFReport()
    pdf.add_page()
    
    for rep in reports:
        
        # SMART PAGINATION: An incident takes ~90mm of space. 
        # If we are past 190mm on the page, jump to the next page to prevent splitting.
        if pdf.get_y() > 190:
            pdf.add_page()
            
        # Title per incident
        pdf.set_font("Arial", 'B', 12)
        if rep['severity'] in ['HIGH', 'CRITICAL']:
            pdf.set_text_color(220, 0, 0) # Red for critical
        else:
            pdf.set_text_color(200, 100, 0) # Orange for medium/low
            
        pdf.cell(0, 8, f"Incident: {rep['behavior_class']} [{rep['severity']}]", ln=True)
        pdf.set_text_color(0, 0, 0) # Reset to black
        
        # Details
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, f"Event ID: {rep['event_id']}", ln=True)
        pdf.cell(0, 6, f"Time: {rep['timestamp']}", ln=True)
        pdf.cell(0, 6, f"Location: {rep['zone']} (Video: {rep['clip_id']})", ln=True)
        pdf.cell(0, 6, f"Action Taken: {rep['escalation_action']}", ln=True)
        
        # Multi-line description
        pdf.multi_cell(0, 6, f"Description: {rep['event_description']}")
        pdf.ln(2)

        # Image Handling
        img_path = f"outputs/crops/{rep['event_id']}.jpg"
        if os.path.exists(img_path):
            
            # Final check just in case the description was massive
            if pdf.get_y() > 230:
                pdf.add_page()
                
            y_before = pdf.get_y()
            
            # FIX: Lock the HEIGHT to 50mm (h=50), and let FPDF auto-scale the width.
            # This prevents tall human bounding boxes from ruining the page layout.
            pdf.image(img_path, x=10, y=y_before, h=50) 
            
            # Safely move cursor down exactly 55mm (50mm image + 5mm padding)
            pdf.set_y(y_before + 55) 
        else:
            pdf.set_text_color(150, 150, 150)
            pdf.cell(0, 10, "[No Image Captured for this Event]", ln=True)
            pdf.set_text_color(0, 0, 0)

        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Divider line
        pdf.ln(5)

    pdf.output(pdf_out)
    print(f"✅ PDF report saved  -> {pdf_out}")
    print(f"Total records processed: {len(reports)}")

    return reports

if __name__ == "__main__":
    generate_reports(
        "outputs/violations_with_severity.json",
        "outputs/compliance_report.json",
        "outputs/compliance_report.csv",
        "outputs/compliance_report.pdf" 
    )
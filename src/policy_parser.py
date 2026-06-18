import os
import json
import fitz  # PyMuPDF
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load environment variables from the .env file automatically
load_dotenv()

def extract_text_from_pdf(pdf_path):
    """Step 1: Open the PDF and read all its text content."""
    print(f"Reading text from {pdf_path}...")
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def parse_rules_with_openrouter(policy_text):
    """Step 2: Send text to OpenRouter using a free, high-performing model."""
    print("Sending policy text to OpenRouter API...")
    
    # 2. Safely pull the key loaded from the .env file
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Could not find OPENROUTER_API_KEY! Please ensure your .env file exists and contains the key.")
    
    # Initialize OpenAI client with OpenRouter's custom base URL
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    
    prompt = f"""
    You are an expert EHS compliance AI system. Analyze the following factory policy manual text.
    Extract the rules for the 4 specific behavioral domains:
    1. Pedestrian Walkway
    2. Equipment Interaction
    3. Electrical Panel Cover Management
    4. Forklift Load Management

    Format your answer strictly as a raw JSON array of objects. Do not include markdown code blocks (like ```json), do not include words before or after the JSON.
    
    Each JSON object must follow this exact schema:
    {{
        "behavior_class": "Name of the unsafe behavior class",
        "policy_rule_ref": "The exact Section number (e.g., Section 3.3.2)",
        "unsafe_indicator": "The visual cue that a violation is occurring",
        "safe_indicator": "The visual cue of the compliant paired behavior",
        "severity_hint": "One of: LOW, MEDIUM, HIGH, CRITICAL based on warning callouts"
    }}

    Here is the policy manual text:
    {policy_text}
    """

    # Using Meta's Llama 3 8B Instruct (Highly reliable free model on OpenRouter)
    response = client.chat.completions.create(
        model="qwen/qwen3.5-9b",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def main():
    pdf_filename = "Compliance_Policy_Manual.pdf"
    output_json_path = os.path.join("outputs", "extracted_rules.json")
    
    # Read the PDF
    if not os.path.exists(pdf_filename):
        print(f"Error: Could not find {pdf_filename} in the root directory!")
        return
        
    pdf_text = extract_text_from_pdf(pdf_filename)
    
    # Extract rules using OpenRouter
    try:
        raw_json_string = parse_rules_with_openrouter(pdf_text)
        
        # Strip away any markdown formatting if the model accidentally included it
        raw_json_string = raw_json_string.strip()
        if raw_json_string.startswith("```json"):
            raw_json_string = raw_json_string.split("```json")[1].split("```")[0].strip()
        elif raw_json_string.startswith("```"):
            raw_json_string = raw_json_string.split("```")[1].split("```")[0].strip()
        
        # Validate that it's flawless JSON before saving
        parsed_rules = json.loads(raw_json_string)
        
        # Cache to the local outputs directory
        os.makedirs("outputs", exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(parsed_rules, f, indent=2)
            
        print(f"Success! Extracted rules safely saved to {output_json_path}")
        
    except Exception as e:
        print(f"An error occurred during parsing: {e}")

if __name__ == "__main__":
    main()
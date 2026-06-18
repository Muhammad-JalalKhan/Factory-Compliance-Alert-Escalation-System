import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

def test_connection():
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ FAILED: Could not find OPENROUTER_API_KEY in the .env file.")
        return

    print("🔑 Key loaded successfully. Attempting to contact OpenRouter...")
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        response = client.chat.completions.create(
            model="qwen/qwen3.5-9b",
            messages=[{"role": "user", "content": "Reply with exactly this text: 'Success! OpenRouter is working.'"}],
            max_tokens=20
        )
        
        print("✅", response.choices[0].message.content)
        
    except Exception as e:
        print(f"❌ API call failed: {e}")

if __name__ == "__main__":
    test_connection()
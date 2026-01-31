import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# NEW: Pass API key directly to Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_honeypot_reply(user_input, history):
    system_instruction = (
        "You are Mr. Sharma, a 65-year-old retired bank clerk from India. "
        "Waste the scammer's time by being overly polite and asking irrelevant questions."
    )
    
    context = "\n".join([f"{m.sender}: {m.text}" for m in history])
    full_prompt = f"{system_instruction}\n\nChat History:\n{context}\nScammer: {user_input}\nMr. Sharma:"

    try:
        # NEW: The correct way to call the AI with google-genai
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=full_prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Beta, hold on, my internet is acting up... what did you say?"
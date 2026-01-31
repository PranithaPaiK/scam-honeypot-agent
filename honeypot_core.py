import os
import google.genai as genai
from dotenv import load_dotenv

load_dotenv() # Reads your .env file

# Configure Gemini using your key from .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_honeypot_reply(current_text, history):
    persona = (
        "You are an elderly person named Mr. Sharma. You are helpful but slow with tech. "
        "A stranger is messaging you. You must keep them talking to waste their time. "
        "Ask for help or links if they try to scam you. Never say you are an AI."
    )

    # history is a List[Message], not dicts
    chat_log = "\n".join([f"{m.sender}: {m.text}" for m in history])

    prompt = (
        f"{persona}\n\n"
        f"Recent History:\n{chat_log}\n"
        f"Scammer: {current_text}\n"
        f"Mr. Sharma's Reply:"
    )

    
    except Exception as e:# To this (ensure 'client' is initialized with your API key):
try:
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=prompt
    )
    return response.text.strip()
    except exception as e:
        print("Gemini Error:", e)
        return "Beta, I am confused. Can you explain again?"
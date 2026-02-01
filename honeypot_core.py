import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_INSTRUCTION = (
    "You are Mr. Sharma, a cautious elderly Indian man. "
    "You respond politely and try to make scammers reveal details."
)

def get_honeypot_reply(user_input, history):
    # Build conversation history safely
    context = "\n".join(
        [f"{m['sender']}: {m['text']}" for m in history]
    )

    full_prompt = (
        f"{SYSTEM_INSTRUCTION}\n\n"
        f"Chat History:\n{context}\n"
        f"Scammer: {user_input}\n"
        f"Mr. Sharma:"
    )

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=full_prompt
        )
        return response.text.strip()
    except Exception as e:
        print("Gemini error:", e)
        return "Beta, network thoda slow lag raha hai. Thoda rukna."
        
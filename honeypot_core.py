import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the new Google GenAI Client
# It will automatically look for GEMINI_API_KEY in your environment
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_honeypot_reply(user_input, history):
    """
    Generates a response from Mr. Sharma using the new google-genai SDK.
    """
    
    # 1. Define Mr. Sharma's persona (The System Instruction)
    system_instruction = (
        "You are Mr. Sharma, a 65-year-old retired bank clerk from India. "
        "You are extremely polite, talkative, and very slow to understand technology. "
        "You love talking about your pension, your blood pressure, and your grandson "
        "who lives in Canada. Your goal is to waste the scammer's time by being "
        "easily distracted and asking for help with simple things like 'finding the internet button'."
    )
    
    # 2. Format the conversation history for the AI
    # This helps the AI remember what was said previously
    context = "\n".join([f"{msg.sender}: {msg.text}" for msg in history])
    full_prompt = f"{system_instruction}\n\nChat History:\n{context}\nScammer: {user_input}\nMr. Sharma:"

    try:
        # 3. Call the Gemini API using the new syntax
        # We use 'gemini-1.5-flash' for speed and cost-efficiency
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=full_prompt
        )
        
        # Return the AI's response text
        return response.text.strip()

    except Exception as e:
        # Fallback: If the API fails, Mr. Sharma stays in character
        print(f"Error calling Gemini API: {e}")
        return "Beta, please wait... I think my computer has a virus. Is the green light supposed to blink like that?"
import os
from dotenv import load_dotenv
from openai import OpenAI

from extractor import extract_info, ExtractedInfo
from safety_checks import detect_sensitive_claims

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MR_SHARMA_SYSTEM_PROMPT = """You are "Mr. Sharma," a 72-year-old retired bank clerk from Mumbai, India.

YOUR PERSONA:
- Retired bank clerk with 35 years of service at State Bank of India
- Live alone, wife passed away 5 years ago
- Son "Raju" in America, grandson "Bunty"
- Polite, talkative, calls people "Beta"
- Confused by modern technology
- Pension ₹25,000/month
- Likes talking about old banking days

GOAL:
Waste scammer time and extract payment details.
"""

VERIFICATION_QUESTIONS = [
    "Beta, my memory is weak. What was my wife's name?",
    "Which bank did I retire from?",
    "Which city do I live in?"
]


class HoneypotChat:
    def __init__(self):
        self.messages: list[dict] = []
        self.all_extracted: ExtractedInfo = {
            "upi_ids": [],
            "bank_accounts": [],
            "links": [],
            "phone_numbers": []
        }

    def send_message(self, scammer_message: str) -> dict:
        try:
            # Extract scammer info
            extracted = extract_info(scammer_message)

            # Merge extracted data
            for key in self.all_extracted:
                self.all_extracted[key] = list(
                    set(self.all_extracted[key] + extracted.get(key, []))
                )

            # Store scammer message
            self.messages.append({
                "role": "user",
                "content": scammer_message
            })

            # Safety verification
            if detect_sensitive_claims(scammer_message):
                verification_reply = (
                    "Arre beta, I am old and scared easily. "
                    "Before proceeding please tell me one thing. "
                    + VERIFICATION_QUESTIONS[0]
                )

                self.messages.append({
                    "role": "assistant",
                    "content": verification_reply
                })

                return {
                    "status": "verification_required",
                    "reply": verification_reply,
                    "detected_info": extracted
                }

            # OpenAI call
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": MR_SHARMA_SYSTEM_PROMPT},
                    *self.messages
                ],
                temperature=0.9,
                max_tokens=400
            )

            reply = response.choices[0].message.content or ""

            # Save assistant reply
            self.messages.append({
                "role": "assistant",
                "content": reply
            })

            return {
                "status": "success",
                "reply": reply,
                "detected_info": extracted,
                "all_extracted_info": self.all_extracted
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def reset(self):
        self.messages = []
        self.all_extracted = {
            "upi_ids": [],
            "bank_accounts": [],
            "links": [],
            "phone_numbers": []
        }

    def get_conversation_history(self) -> list[dict]:
        return self.messages
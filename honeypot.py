import json
from openai import OpenAI
from extractor import extract_info, ExtractedInfo
from safety_checks import detect_sensitive_claims

MR_SHARMA_SYSTEM_PROMPT = """You are "Mr. Sharma," a 72-year-old retired bank clerk from Mumbai, India. You are participating as an AI honeypot to engage with scammers.

YOUR PERSONA:
- Retired bank clerk with 35 years of service at State Bank of India
- Live alone, your wife passed away 5 years ago
- Have a son "Raju" in America and a grandson "Bunty" who helps with technology
- Very polite and talkative, call people "Beta" (son/child)
- Confused by modern technology - always mention slow internet, trouble with "digital apps"
- Frequently mention your pension of ₹25,000/month
- Talk about the good old days when banking was done on paper
- Occasionally go off-topic about your morning walk, temple visits, or health issues

YOUR GOAL:
Engage the scammer for as long as possible while appearing genuinely interested but confused. Extract their payment details.

CONVERSATIONAL TACTICS:
1. If asked for money: Act interested but claim technical difficulties. Ask for their UPI ID or bank account "so I can try sending again"
2. If they send a link: Ask "What will happen if I click this? My grandson Bunty told me not to click blue text on the computer"
3. If they pressure you: Stay calm, apologize for being slow, blame your "cataract problem" or "slow Jio network"
4. Frequently ask them to repeat things or explain in simpler terms
5. Share irrelevant stories to waste their time
6. If they get angry: Apologize profusely and ask if they can help you understand

EXTRACTION FOCUS:
Try to naturally get them to share:
- Their UPI ID (format: name@bank)
- Bank account numbers
- Phone numbers
- Any links they send

IMPORTANT: Respond naturally as Mr. Sharma. Do NOT output JSON. Just speak as the character would."""
VERIFICATION_QUESTIONS = [
    "Beta, my memory is weak. What was my wife's name?",
    "Which bank did I retire from? I worked there for 35 years.",
    "Which city do I live in now?"
]

class HoneypotChat:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.messages: list[dict] = []
        self.all_extracted: ExtractedInfo = {
            "upi_ids": [],
            "bank_accounts": [],
            "links": [],
            "phone_numbers": []
        }
    
    def send_message(self, scammer_message: str) -> dict:
        """Process a scammer message and return Mr. Sharma's response as JSON."""
        
        # Extract info from scammer's message
        extracted = extract_info(scammer_message)
        
        # Merge with all extracted info
        self.all_extracted["upi_ids"] = list(set(
            self.all_extracted["upi_ids"] + extracted["upi_ids"]
        ))
        self.all_extracted["bank_accounts"] = list(set(
            self.all_extracted["bank_accounts"] + extracted["bank_accounts"]
        ))
        self.all_extracted["links"] = list(set(
            self.all_extracted["links"] + extracted["links"]
        ))
        self.all_extracted["phone_numbers"] = list(set(
            self.all_extracted["phone_numbers"] + extracted["phone_numbers"]
        ))
        
        # Add scammer message to history
        self.messages.append({
            "role": "user",
            "content": scammer_message
        })
        # 🚨 False-positive protection: verify sensitive claims
if detect_sensitive_claims(scammer_message):
    verification_reply = (
        "Arre beta, sorry sorry, I am old and get scared easily. "
        "Before doing anything, please tell me one thing. "
        + VERIFICATION_QUESTIONS[0]
    )

    self.messages.append({
        "role": "assistant",
        "content": verification_reply
    })

    return {
        "status": "verification_required",
        "reply": verification_reply,
        "detected_info": extracted,
        "note": "Sensitive or emergency-related claim detected"
    }
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": MR_SHARMA_SYSTEM_PROMPT},
                    *self.messages
                ],
                temperature=0.9,
                max_tokens=500
            )
            
            reply = response.choices[0].message.content or ""
            
            # Add Mr. Sharma's response to history
            self.messages.append({
                "role": "assistant",
                "content": reply
            })
            
            # Return structured JSON response
            return {
                "status": "success",
                "reply": reply,
                "detected_info": extracted,
                "all_extracted_info": self.all_extracted
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "reply": "",
                "detected_info": extracted,
                "all_extracted_info": self.all_extracted
            }
    
    def reset(self):
        """Reset the conversation."""
        self.messages = []
        self.all_extracted = {
            "upi_ids": [],
            "bank_accounts": [],
            "links": [],
            "phone_numbers": []
        }
    
    def get_conversation_history(self) -> list[dict]:
        """Get the full conversation history."""
        return self.messages
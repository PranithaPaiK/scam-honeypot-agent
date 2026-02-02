import os
import json
from dotenv import load_dotenv
from honeypot import HoneypotChat
from complaint_generator import generate_cybercrime_complaint

# Load environment variables
load_dotenv()

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print(json.dumps({
            "status": "error",
            "error": "OPENAI_API_KEY not found in .env file"
        }, indent=2))
        return
    
    # Initialize the honeypot
    honeypot = HoneypotChat(api_key)
    
    print("=" * 60)
    print("🍯 MR. SHARMA AI HONEYPOT 🍯")
    print("=" * 60)
    print("Type scam messages to test the honeypot.")
    print("Commands: 'quit' to exit, 'reset' to start new conversation")
    print("All responses are in JSON format.")
    print("=" * 60)
    print()
    
    while True:
        try:
            # Get scammer input
            scammer_input = input("📞 Scammer: ").strip()
            
            if not scammer_input:
                continue
            
            if scammer_input.lower() == "quit":
                if scammer_input.lower() == "quit":
    complaint = generate_cybercrime_complaint(
        honeypot.all_extracted,
        honeypot.get_conversation_history()
    )

    print(json.dumps({
        "status": "session_ended",
        "total_extracted": honeypot.all_extracted,
        "cybercrime_complaint_draft": complaint
    }, indent=2, ensure_ascii=False))
    break
            
            if scammer_input.lower() == "reset":
                honeypot.reset()
                print(json.dumps({
                    "status": "reset",
                    "message": "Conversation reset successfully"
                }, indent=2))
                print()
                continue
            
            # Get Mr. Sharma's response
            response = honeypot.send_message(scammer_input)
            
            # Print JSON response
            print()
            print("📋 JSON Response:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            print()
            print(f"👴 Mr. Sharma: {response.get('reply', '')}")
            print()
            
        except KeyboardInterrupt:
            print("\n")
            print(json.dumps({
                "status": "interrupted",
                "total_extracted": honeypot.all_extracted
            }, indent=2))
            break
        except Exception as e:
            print(json.dumps({
                "status": "error",
                "error": str(e)
            }, indent=2))


if __name__ == "__main__":
    main()
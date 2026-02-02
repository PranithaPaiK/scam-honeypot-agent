from datetime import datetime

def generate_cybercrime_complaint(all_extracted: dict, conversation: list[dict]) -> str:
    date = datetime.now().strftime("%d-%m-%Y %H:%M")
    
    conversation_summary = "\n".join([
        f"{msg['role'].upper()}: {msg['content'][:120]}"
        for msg in conversation if msg["role"] == "user"
    ])
    
    complaint = f"""
CYBER CRIME COMPLAINT DRAFT
--------------------------
Date: {date}

Victim Profile:
Senior Citizen (Retired Bank Employee)

Type of Scam:
Suspected Online Financial Fraud / Social Engineering

Extracted Scam Details:
UPI IDs: {', '.join(all_extracted.get('upi_ids', [])) or 'Not provided'}
Bank Accounts: {', '.join(all_extracted.get('bank_accounts', [])) or 'Not provided'}
Phone Numbers: {', '.join(all_extracted.get('phone_numbers', [])) or 'Not provided'}
Suspicious Links: {', '.join(all_extracted.get('links', [])) or 'Not provided'}

Conversation Summary:
{conversation_summary}

Remarks:
Conversation collected using an AI honeypot designed for scammer intelligence
and elderly protection.

Submitted for investigation.
"""
    return complaint.strip()
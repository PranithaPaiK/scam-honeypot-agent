import re

def extract_all_intelligence(text):
    # [span_3](start_span)These fields are required by the evaluation platform[span_3](end_span)
    intel = {
        "bankAccounts": re.findall(r'\b\d{9,18}\b', text), # 9-18 digit numbers
        "upiIds": re.findall(r'[a-zA-Z0-9.\-_]+@[a-zA-Z]{2,}', text), # Standard UPI pattern
        "phishingLinks": re.findall(r'https?://\S+', text), # Any URL
        "phoneNumbers": re.findall(r'\+?\d{10,12}', text), # Phone patterns
        "suspiciousKeywords": []
    }
    
    # [span_4](start_span)Check for mandatory keywords[span_4](end_span)
    keywords = ["urgent", "verify", "blocked", "refund", "suspend", "kyc"]
    for word in keywords:
        if word in text.lower():
            intel["suspiciousKeywords"].append(word)
            
    return intel
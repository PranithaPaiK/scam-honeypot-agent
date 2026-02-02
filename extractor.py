import re
import json
from typing import TypedDict

class ExtractedInfo(TypedDict):
    upi_ids: list[str]
    bank_accounts: list[str]
    links: list[str]
    phone_numbers: list[str]

def extract_info(message: str) -> ExtractedInfo:
    """Extract UPI IDs, bank accounts, links, and phone numbers from a message."""
    
    # UPI ID pattern (e.g., name@okaxis, user@paytm)
    upi_pattern = r'[a-zA-Z0-9._-]+@[a-zA-Z]{2,}'
    
    # Bank account pattern (9-18 digit numbers)
    bank_account_pattern = r'\b\d{9,18}\b'
    
    # URL pattern
    url_pattern = r'https?://[^\s]+|www\.[^\s]+'
    
    # Indian phone number pattern
    phone_pattern = r'(?:\+91[\-\s]?)?[6-9]\d{9}'
    
    upi_ids = list(set(re.findall(upi_pattern, message, re.IGNORECASE)))
    bank_accounts = list(set(re.findall(bank_account_pattern, message)))
    links = list(set(re.findall(url_pattern, message, re.IGNORECASE)))
    phone_numbers = list(set(re.findall(phone_pattern, message)))
    
    return {
        "upi_ids": upi_ids,
        "bank_accounts": bank_accounts,
        "links": links,
        "phone_numbers": phone_numbers
    }
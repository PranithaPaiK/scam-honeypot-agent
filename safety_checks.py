def detect_sensitive_claims(message: str) -> bool:
    """
    Detects messages that could indicate a real emergency or family claim.
    """
    sensitive_keywords = [
        "son", "daughter", "father", "mother",
        "hospital", "emergency", "accident",
        "relative", "family", "medical"
    ]
    
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in sensitive_keywords)
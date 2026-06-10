"""
Kafka Consumer with HMAC Verification
Consumes transaction events and verifies message integrity
"""
import json
import hmac
import hashlib
import os

HMAC_SECRET = os.environ.get("HMAC_SECRET", "dev-hmac-secret-change-in-prod")

def verify_signature(payload: dict, received_signature: str) -> bool:
    """Verify HMAC-SHA256 signature to detect tampered messages."""
    message_str = json.dumps(payload, sort_keys=True)
    expected_signature = hmac.new(
        HMAC_SECRET.encode(),
        message_str.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Use hmac.compare_digest to prevent timing attacks
    return hmac.compare_digest(expected_signature, received_signature)

def process_message(envelope: dict):
    """Process a received Kafka message after verifying integrity."""
    payload = envelope.get("payload", {})
    signature = envelope.get("signature", "")
    
    if not verify_signature(payload, signature):
        print(f"[KAFKA] ALERT: Message signature verification FAILED - possible tampering!")
        return False
    
    event_type = payload.get("event_type")
    data = payload.get("data", {})
    
    print(f"[KAFKA] Verified and processing event: {event_type}")
    
    if event_type == "TRANSFER":
        print(f"[KAFKA] Transfer: {data.get('from')} -> {data.get('to')}: ${data.get('amount')}")
    elif event_type == "FAILED_AUTH":
        print(f"[KAFKA] Security alert: Failed auth for {data.get('username')}, attempts: {data.get('attempts')}")
    
    return True

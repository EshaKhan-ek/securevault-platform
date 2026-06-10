"""
Kafka Producer with HMAC Message Signing
Publishes transaction events to Kafka with integrity verification
"""
import json
import hmac
import hashlib
import time
import os

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")
HMAC_SECRET = os.environ.get("HMAC_SECRET", "dev-hmac-secret-change-in-prod")

def sign_message(payload: dict) -> str:
    """Sign message payload with HMAC-SHA256 for integrity verification."""
    message_str = json.dumps(payload, sort_keys=True)
    signature = hmac.new(
        HMAC_SECRET.encode(),
        message_str.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature

def publish_transaction_event(event_type: str, data: dict):
    """
    Publish a transaction event to Kafka.
    Message includes HMAC signature to prevent tampering.
    """
    payload = {
        "event_type": event_type,
        "timestamp": time.time(),
        "data": data
    }
    
    signature = sign_message(payload)
    envelope = {
        "payload": payload,
        "signature": signature,
        "version": "1.0"
    }
    
    # In production: KafkaProducer sends to 'transactions' topic
    # producer.send('transactions', value=json.dumps(envelope).encode())
    print(f"[KAFKA] Published {event_type}: {json.dumps(envelope, indent=2)}")
    return envelope


# Example events:
# publish_transaction_event("TRANSFER", {"from": "esha", "to": "admin", "amount": 100})
# publish_transaction_event("LOGIN", {"username": "esha", "ip": "192.168.1.1"})
# publish_transaction_event("FAILED_AUTH", {"username": "esha", "attempts": 3})

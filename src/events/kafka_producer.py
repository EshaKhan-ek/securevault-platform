import json
import hmac
import hashlib
import os
from datetime import datetime

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
HMAC_SECRET = os.environ.get("KAFKA_HMAC_SECRET", "securevault-hmac-key-2026")
LOGIN_TOPIC = "auth.login.events"

def sign_event(payload: dict) -> str:
    message = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hmac.new(HMAC_SECRET.encode("utf-8"), message, hashlib.sha256).hexdigest()

def build_event(event_type: str, username: str, ip: str, success: bool) -> dict:
    payload = {
        "event_type": event_type,
        "username": username,
        "source_ip": ip,
        "success": success,
        "timestamp": datetime.utcnow().isoformat(),
        "service": "auth-service"
    }
    payload["hmac_signature"] = sign_event(payload)
    return payload

def produce_login_event(username: str, ip: str, success: bool):
    event = build_event("LOGIN_ATTEMPT", username, ip, success)
    try:
        from kafka import KafkaProducer
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            security_protocol="SASL_SSL",
            sasl_mechanism="SCRAM-SHA-512",
        )
        producer.send(LOGIN_TOPIC, value=event)
        producer.flush()
        print(f"[Kafka] Event produced: {event['event_type']} for {username}")
    except Exception as e:
        print(f"[Kafka] Broker unavailable (stub mode): {e}")
        print(f"[Kafka] Would have sent: {json.dumps(event, indent=2)}")

if __name__ == "__main__":
    print("=== Kafka Producer Stub — HMAC Signing Demo ===\n")
    test_event = build_event("LOGIN_ATTEMPT", "esha", "192.168.1.10", True)
    print(json.dumps(test_event, indent=2))

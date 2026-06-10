"""Demo: run this to test Kafka producer/consumer with HMAC signing"""
from producer import publish_transaction_event
from consumer import process_message

print("=== KAFKA HMAC SIGNING DEMO ===\n")

# Produce a message
print("1. Publishing transaction event...")
envelope = publish_transaction_event("TRANSFER", {
    "from": "esha",
    "to": "admin", 
    "amount": 100.0
})

print("\n2. Consuming and verifying...")
result = process_message(envelope)
print(f"Signature valid: {result}")

print("\n3. Testing tampered message detection...")
envelope["payload"]["data"]["amount"] = 99999.0  # Tamper!
result = process_message(envelope)
print(f"Tampered message accepted: {result}  <- Should be False")

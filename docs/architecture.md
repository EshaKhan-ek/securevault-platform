# SecureVault Bank — Architecture Blueprint
Author: Esha Khan (Lead Developer)
Framework: C4 Model + Zero Trust (NIST SP 800-207)

---

## Zero Trust Principles

| Principle | Implementation |
|---|---|
| Never trust, always verify | Every endpoint requires RS256 JWT Bearer token |
| Least privilege | RBAC: customers blocked from admin endpoints (403) |
| Assume breach | Each service validates tokens independently |
| Micro-segmentation | Services on separate ports, no shared state |
| Short-lived credentials | JWT TTL 30 min, Redis rate limit 5/60s |

---

## C4 Level 1 — System Context

SecureVault Bank is a cloud-native banking platform serving two actor types:

- **Customer** — authenticates via HTTPS, sends/receives money, views transaction history
- **Admin** — authenticates via HTTPS, views all users and transactions (RBAC enforced)

External systems:

| System | Role |
|---|---|
| Redis | Rate limiting and distributed cache |
| Apache Kafka | Event streaming (HMAC-signed events, SASL_SSL) |
| HashiCorp Vault | Secrets management — RSA private key injection |

---

## C4 Level 2 — Container Diagram

| Container | Port | Technology | Security Controls |
|---|---|---|---|
| auth-service | 8001 | FastAPI, Python | RS256 JWT, bcrypt, Redis rate limit |
| user-service | 8002 | FastAPI, Python | JWT verify, RBAC, reads RSA public key |
| transaction-service | 8003 | FastAPI, Python | JWT verify, ABAC, input validation, publishes Kafka events |
| Redis | 6379 | Redis 7 Alpine | Rate limiting store, session TTL |
| Apache Kafka | 9092 | Kafka + SASL_SSL | HMAC-signed event streaming |
| HashiCorp Vault | 8200 | Vault | RSA private key storage and injection |
| SQLite (per service) | — | SQLite3 | Persistent user, balance, transaction store |

Flow:
- Client logs in/registers via auth-service
- auth-service checks Redis rate limit, verifies bcrypt hash, retrieves RSA private key from Vault, signs JWT
- user-service and transaction-service verify JWT using shared RSA public key
- transaction-service publishes events to Kafka on each transfer
- All balances, users, and transactions persist in SQLite databases mounted via Docker volumes

---

## C4 Level 3 — Auth Service Component Diagram

Components inside auth-service (:8001):

| Component | File | Responsibility |
|---|---|---|
| FastAPI Router | main.py | Handles /register /login /verify /logout endpoints |
| Security Module | security.py | RS256 JWT create/verify, bcrypt hash/verify |
| Data Models | models.py | Pydantic validation — alphanumeric username, min 8 char password, role whitelist |
| User Database | database.py | SQLite-backed user store (username, hashed_password, role, balance) |
| Vault Client | vault_client.py | Reads RSA private key from HashiCorp Vault secret path |
| Redis Rate Limiter | main.py | INCR + EXPIRE per IP — blocks after 5 failed attempts in 60s |

---

## C4 Level 4 — JWT Login Sequence

1. Client sends POST /auth/login
2. auth-service checks Redis: failed attempts for IP — blocks if >= 5 (HTTP 429)
3. auth-service retrieves hashed password from SQLite database
4. bcrypt.verify(plain, hashed) — constant-time comparison
5. On failure: Redis INCR attempts, EXPIRE 60s → HTTP 401
6. On 5th failure: HTTP 429 Too many login attempts
7. On success: auth-service fetches RSA private key from HashiCorp Vault
8. jwt.encode(RS256, sub + role + exp 30min) → HTTP 200 with access_token + role
9. Client sends GET /auth/verify with Bearer token
10. auth-service verifies token using RSA public key → returns username, role, valid: true

---

## Docker Security

| Control | Implementation |
|---|---|
| Multi-stage build | Builder stage installs deps; clean production stage copies only artifacts |
| Non-root user | adduser appuser, USER appuser in all Dockerfiles |
| Key permissions | chmod 400 private.pem, chown appuser |
| Security updates | apt-get upgrade in production stage |
| HEALTHCHECK | All 3 services probe /health every 30s |
| Persistent storage | Docker named volumes for SQLite DB files per service |
| Data directory | /app/data created and chown'd to appuser before USER switch |

---

## SABSA Alignment

| Layer | Implementation |
|---|---|
| Contextual | Protect customer financial data and transaction integrity |
| Conceptual | Zero Trust, CIA Triad, risk-based access control |
| Logical | RS256 JWT, RBAC/ABAC, bcrypt, SQLite persistence |
| Physical | Docker multi-stage, non-root, Trivy scanning, named volumes |
| Component | FastAPI, Redis, Kafka HMAC stub, HashiCorp Vault, SQLite |
| Operational | HEALTHCHECK, Trivy reports, structured error responses |

---

## Framework Mapping

| Control | NIST CSF | OWASP ASVS | MITRE ATT&CK |
|---|---|---|---|
| RS256 JWT | PR.AC-1 | V2 | T1078 mitigated |
| bcrypt | PR.DS-2 | V2.4 | T1110 mitigated |
| Rate limiting | PR.AC-4 | V2.2 | T1110.001 mitigated |
| RBAC | PR.AC-3 | V4 | T1068 mitigated |
| Input validation | PR.DS-6 | V5 | T1190 mitigated |
| Memory safety | PR.IP-2 | V5.4 | T1203 mitigated |
| Non-root Docker | PR.AC-6 | V14.2 | T1611 mitigated |
| SQLite persistence | PR.DS-1 | V8 | T1005 mitigated |
| Vault secret injection | PR.AC-1 | V6.4 | T1552 mitigated |
| Kafka HMAC signing | PR.DS-6 | V13 | T1040 mitigated |

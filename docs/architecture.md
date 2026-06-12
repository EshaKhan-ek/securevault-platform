# SecureVault Bank — Architecture Blueprint
Author: Esha Khan (Lead Developer)
Framework: C4 Model + Zero Trust (NIST SP 800-207)

## Zero Trust Principles

| Principle | Implementation |
|---|---|
| Never trust, always verify | Every endpoint requires RS256 JWT Bearer token |
| Least privilege | RBAC: customers blocked from admin endpoints (403) |
| Assume breach | Each service validates tokens independently |
| Micro-segmentation | Services on separate ports, no shared state |
| Short-lived credentials | JWT TTL 30 min, Redis rate limit 5/60s |

## C4 Level 1 — System Context
- Customer authenticates, sends/receives money, views history
- Admin views all users and transactions (RBAC enforced)
- Redis: rate limiting store
- Kafka: event broker (SASL_SSL + HMAC signing)

## C4 Level 2 — Containers
| Container | Port | Security |
|---|---|---|
| auth-service | 8001 | RS256 JWT, bcrypt, Redis rate limit |
| user-service | 8002 | JWT verify, RBAC |
| transaction-service | 8003 | JWT verify, ABAC, input validation |
| redis | 6379 | Rate limiting, session TTL |

## C4 Level 3 — Auth Service Components
- main.py: FastAPI routes (/register /login /verify /logout)
- security.py: RS256 token create/verify, bcrypt hashing
- database.py: User store
- models.py: Pydantic validators (username alphanumeric, password min 8)
- Rate limiter: Redis INCR + EXPIRE per IP

## C4 Level 4 — Login Sequence
1. Client POST /auth/login
2. Redis: check failed attempts for IP (block if >= 5)
3. bcrypt.verify(plain, hashed) — constant-time comparison
4. On fail: Redis INCR attempts, EXPIRE 60s → 401
5. On 5th fail: 429 Too many login attempts
6. On success: jwt.encode(RS256, sub+role+exp) → 200

## Docker Security
| Control | Implementation |
|---|---|
| Multi-stage build | Builder + clean production stage |
| Non-root user | adduser appuser, USER appuser |
| Key permissions | chmod 400 private.pem, chown appuser |
| Security updates | apt-get upgrade in production stage |
| HEALTHCHECK | All 3 services probe /health every 30s |

## SABSA Alignment
| Layer | Implementation |
|---|---|
| Contextual | Protect customer financial data |
| Conceptual | Zero Trust, CIA Triad, risk-based access |
| Logical | RS256 JWT, RBAC/ABAC, bcrypt |
| Physical | Docker multi-stage, non-root, Trivy scanning |
| Component | FastAPI, Redis, Kafka HMAC stub |
| Operational | HEALTHCHECK, Trivy reports, structured errors |

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

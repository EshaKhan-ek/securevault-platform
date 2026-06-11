# SecureVault Bank — Architecture Blueprint

## Overview
SecureVault Bank is a cloud-native, microservices-based banking platform built with
Zero Trust security principles and Defence-in-Depth architecture.

## Zero Trust Implementation (NIST SP 800-207)
- Never trust, always verify — every request requires a valid JWT token
- Least privilege — customers cannot access admin endpoints (RBAC enforced)
- Micro-segmentation — each service runs in its own Docker container
- All inter-service communication uses the same JWT verification

## Security Frameworks Applied

| Framework | Application |
|---|---|
| OWASP ASVS v5 | Input validation, authentication strength, session management |
| NIST CSF | Identify, Protect, Detect, Respond, Recover controls |
| NIST SP 800-207 | Zero Trust architecture principles |
| SABSA | Business-driven security architecture, risk-based design |
| ISO/IEC 27034 | Secure software development lifecycle integration |
| MITRE ATT&CK | Threat modelling against known attack techniques |
| CIS Docker Benchmark | Container hardening standards |

## Defence-in-Depth Layers

### Layer 1 — Network
- Services isolated in Docker network
- Only required ports exposed
- Redis not exposed externally

### Layer 2 — Application
- JWT RS256 (asymmetric) — private key never leaves auth service
- bcrypt cost factor 12 — brute force resistant
- Redis rate limiting — 5 attempts per IP per 60 seconds
- Input validation on all endpoints via Pydantic

### Layer 3 — Data
- Passwords stored as bcrypt hashes only
- Secrets injected via Vault agent — never in source code
- Private key excluded from Docker image layers

### Layer 4 — Container
- Multi-stage Docker builds — minimal attack surface
- Non-root user (UID 1001) in all containers
- Read-only filesystem where possible
- Trivy scanning — no CRITICAL CVEs in application code

## Services

| Service | Port | Tech | Security |
|---|---|---|---|
| auth-service | 8001 | FastAPI, JWT RS256, bcrypt | Redis rate limiting, Vault key injection |
| user-service | 8002 | FastAPI, RBAC | JWT verification, admin/customer separation |
| transaction-service | 8003 | FastAPI, ABAC | Input validation, balance checks, Kafka events |
| Redis | 6379 | Redis 7 Alpine | Rate limiting backend |
| Kafka | 9092 | Apache Kafka | HMAC-signed transaction events |
| Vault | 8200 | HashiCorp Vault | Dynamic secret management |

## SABSA Mapping
- Business Attribute: Confidentiality of customer financial data
- Risk: Unauthorized access to account balances
- Control: JWT RS256 + RBAC — only authenticated users see their own data
- Assurance: Trivy scanning + SonarQube static analysis

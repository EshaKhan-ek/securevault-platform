# SecureVault Bank
End-to-End Secure Cloud-Native DevSecOps Platform

## Team
| Name | Role |
|---|---|
| Esha Khan | Lead Developer |
| Zainab | Security Analyst |
| Husna | DevSecOps Engineer |
| Zarmeena | Red/Blue Team |

## Services
| Service | Port | Description |
|---|---|---|
| auth-service | 8001 | JWT RS256, bcrypt, Redis rate limiting |
| user-service | 8002 | RBAC — admin and customer roles |
| transaction-service | 8003 | Send money, balance, input validation |

## Quick Start
```bash
# Run all services locally
cd src/auth_service && source venv/bin/activate && uvicorn main:app --port 8001 &
cd src/user_service && source venv/bin/activate && uvicorn main:app --port 8002 &
cd src/transaction_service && source venv/bin/activate && uvicorn main:app --port 8003 &

# Or run with Docker
docker-compose up -d
```

## Security Features
- JWT RS256 asymmetric signing
- bcrypt password hashing
- Redis rate limiting (5 attempts / 60s)
- RBAC (admin / customer roles)
- ABAC on transaction amounts
- Multi-stage hardened Docker images
- Trivy image scanning
- HashiCorp Vault secret injection
- Kafka HMAC-signed events
- Memory safety demos (buffer overflow, format string, use-after-free)

## Branch Structure
| Branch | Purpose |
|---|---|
| main | Production-ready code |
| dev | Integration branch |
| feature/auth-service | JWT auth implementation |
| feature/user-service | RBAC user management |
| feature/transaction-service | Secure transactions |
| feature/memory-safety | C memory vulnerability demos |
| feature/docker-hardening | Hardened Dockerfiles + Trivy |
| feature/vault-integration | HashiCorp Vault stub |
| feature/kafka-stub | Kafka HMAC producer/consumer |
| docs/architecture | C4 diagrams + blueprint |

## Reports
All security reports are in `/reports`:
- `trivy-auth.txt` — Docker image scan results
- `trivy-user.txt` — Docker image scan results
- `trivy-transaction.txt` — Docker image scan results
- `sonarqube-findings.md` — Static analysis findings and fixes

## Security Frameworks Applied
OWASP ASVS v5 · NIST CSF · NIST SP 800-207 (Zero Trust) · SABSA · ISO/IEC 27034 · MITRE ATT&CK · CIS Docker Benchmark

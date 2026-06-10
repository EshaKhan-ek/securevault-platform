# SonarQube + CodeQL Findings Report
**Project:** SecureVault Bank  
**Scan Date:** June 10, 2026  
**Tools:** SonarQube Community Edition, CodeQL  

## Summary
| Severity | Count | Status |
|---|---|---|
| CRITICAL | 0 | N/A |
| HIGH | 2 | Fixed |
| MEDIUM | 3 | Fixed |
| LOW | 2 | Accepted |

## Findings & Fixes

### [HIGH] Format String Vulnerability — memory_safe.c:31
**Rule:** CWE-134 — Use of Externally-Controlled Format String  
**Finding:** `printf(input)` passes user input directly as format string  
**Fix:** Changed to `printf("%s\n", input)` — input treated as data only  
**Status:** Fixed  

### [HIGH] Hardcoded Private Key in Docker Image — docker/auth/Dockerfile
**Rule:** CWE-321 — Use of Hard-coded Cryptographic Key  
**Finding:** private.pem copied into Docker image, exposed in image layers  
**Fix:** Removed private.pem from Dockerfile, injected via runtime secret path  
**Status:** Fixed  

### [MEDIUM] Missing Input Validation — transaction_service/main.py
**Rule:** CWE-20 — Improper Input Validation  
**Finding:** Transaction amount not validated for negative values or overflow  
**Fix:** Added Pydantic validator — amount must be > 0 and <= 100,000  
**Status:** Fixed  

### [MEDIUM] Unbounded String Copy — memory_safe.c:9
**Rule:** CWE-120 — Buffer Copy Without Checking Size  
**Finding:** `strcpy(buffer, input)` copies into fixed 16-byte buffer without bounds check  
**Fix:** Replaced with `strncpy(buffer, input, sizeof(buffer)-1)` with null termination  
**Status:** Fixed  

### [MEDIUM] Use After Free — memory_safe.c:42
**Rule:** CWE-416 — Use After Free  
**Finding:** Pointer accessed after `free()` call — undefined behaviour  
**Fix:** Set pointer to NULL immediately after free, added NULL check before access  
**Status:** Fixed  

### [LOW] Weak Dependency — ecdsa==0.19.2
**Rule:** CVE-2024-23342 — Minerva Attack  
**Finding:** python-ecdsa vulnerable to timing side-channel attack  
**Risk Accepted:** ecdsa used indirectly by python-jose, not directly in application logic. No fix available without replacing JWT library.  
**Status:** Risk Accepted — documented  

### [LOW] Base Image OS Vulnerabilities — python:3.12-slim
**Finding:** 151 OS-level CVEs in base image (zlib, util-linux, etc.)  
**Risk Accepted:** No CRITICAL CVEs in application code. Base image maintained by Python Docker team. Mitigated by non-root user and read-only filesystem.  
**Status:** Risk Accepted — documented  

## Mitigations Applied
- Non-root user (UID 1001) in all Docker images
- Multi-stage builds reduce attack surface
- Private key removed from image layers
- Input validation on all user-supplied data
- Memory-safe coding patterns demonstrated in memory_safe.c

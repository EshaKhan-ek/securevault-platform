# Multi-Framework Compliance Mapping

| Control Objective | NIST CSF | OWASP ASVS v5 | ISO 27034 | CSA CCM | MITRE ATT&CK | Implementation in SecureVault |
|---|---|---|---|---|---|---|
| Identity & Access Control | PR.AC-1 | V2 — Authentication | A.9.4 | IAM-01 | T1078 | JWT RS256 asymmetric signing; role-based customer/admin tokens |
| JWT Token Security | PR.AC-3 | V3 — Session Mgmt | A.9.4.2 | IAM-02 | T1134 | RS256-only enforcement; rejects alg:none, HS256 confusion, role tampering |
| Container Security | PR.PT-3 | V10 — Malicious Code | A.12.6.1 | IVS-06 | T1611 | Kyverno blocks privileged pods; Falco CRITICAL on shell spawn, nsenter, shadow read |
| Threat Detection & Monitoring | DE.CM-1 | V1 — Architecture | A.12.6.1 | TVM-01 | T1040 | Falco 5 custom rules (T1059, T1068, T1222, T1496, T1552); Wazuh 5 correlation rules R-01 to R-05 |
| Brute Force Detection | DE.CM-7 | V7 — Error Handling | A.12.4.1 | LOG-01 | T1110 | Wazuh R-01 fires on 5+ failed logins in 2 min from same IP |
| Input Validation & XSS | PR.IP-2 | V5 — Input Validation | A.14.2.5 | AIS-01 | T1190 | Negative amount blocked (400); ABAC enforced (403); XSS found in description field — remediation pending |
| Kafka Message Security | PR.DS-2 | V9 — Communications | A.10.1.1 | IVS-01 | T1565 | Wazuh R-04 detects Kafka auth failures; SASL configured post red team engagement |
| Privilege Escalation Detection | DE.CM-1 | V10 — Malicious Code | A.12.6.1 | TVM-02 | T1068 | Falco rule fires on setuid to UID 0 inside containers |
| Incident Response | RS.RP-1 | V7 — Logging | A.16.1.5 | SEF-04 | T1562 | NIST SP 800-61 framework; blue team runbook; Wazuh + Falco alerts; pod isolation and removal |
| ML Anomaly Correlation | DE.AE-2 | V1 — Architecture | A.12.6.1 | TVM-01 | T1078, T1110 | Wazuh R-03 correlates ML anomaly score with auth failures within 5 min window |

# SecureVault Bank — C4 Architecture Diagrams

## Level 1: System Context
```mermaid
graph TB
    Customer["👤 Bank Customer\n(Web/Mobile User)"]
    Admin["👤 Bank Admin\n(Internal Staff)"]
    SVP["🏦 SecureVault Bank\nPlatform"]
    Redis["⚡ Redis\n(Session Cache)"]
    Kafka["📨 Apache Kafka\n(Event Streaming)"]
    Vault["🔐 HashiCorp Vault\n(Secrets Management)"]

    Customer -->|"HTTPS — Login, Transfer, View Balance"| SVP
    Admin -->|"HTTPS — Manage Users, View All Transactions"| SVP
    SVP -->|"Rate Limiting, Sessions"| Redis
    SVP -->|"Publishes Transaction Events"| Kafka
    SVP -->|"Reads Secrets at Runtime"| Vault
```

## Level 2: Container Diagram
```mermaid
graph TB
    User["👤 User / Admin"]

    subgraph SecureVault Platform
        Auth["🔐 Auth Service\n:8001\nFastAPI + JWT RS256\nbcrypt + Redis rate limit"]
        UserSvc["👥 User Service\n:8002\nFastAPI + RBAC\nAdmin / Customer roles"]
        TxSvc["💸 Transaction Service\n:8003\nFastAPI + ABAC\nInput validation"]
    end

    Redis["⚡ Redis :6379\nRate limiting\nSession store"]
    Kafka["📨 Kafka :9092\nTransaction events\nHMAC signed"]
    Vault["🔐 Vault :8200\nJWT keys\nService secrets"]

    User -->|"POST /auth/login\nPOST /auth/register"| Auth
    User -->|"GET /users/me\nGET /users/all (admin)"| UserSvc
    User -->|"POST /transactions/send\nGET /transactions/history"| TxSvc

    Auth -->|"Rate limit checks"| Redis
    Auth -->|"Reads private key"| Vault
    TxSvc -->|"Publishes events"| Kafka
    UserSvc -->|"Validates JWT"| Auth
    TxSvc -->|"Validates JWT"| Auth
```

## Level 3: Component Diagram — Auth Service
```mermaid
graph TB
    subgraph Auth Service :8001
        API["FastAPI Router\nmain.py"]
        Security["Security Module\nsecurity.py\nJWT RS256, bcrypt"]
        Models["Data Models\nmodels.py\nPydantic validation"]
        DB["In-Memory Store\ndatabase.py\nUser records"]
        VaultClient["Vault Client\nvault_client.py\nSecret injection"]
    end

    Redis["Redis\nRate limiting"]
    Vault["HashiCorp Vault\nRSA private key"]

    API --> Security
    API --> Models
    API --> DB
    Security --> VaultClient
    API -->|"Login attempts"| Redis
    VaultClient -->|"GET secret/auth/jwt-keys"| Vault
```

## Level 4: Code Diagram — JWT Token Flow
```mermaid
sequenceDiagram
    participant C as Client
    participant A as Auth Service
    participant V as Vault
    participant R as Redis

    C->>A: POST /auth/login {username, password}
    A->>R: Check rate limit (IP)
    R-->>A: OK (< 5 attempts)
    A->>A: Verify bcrypt hash
    A->>V: GET private key (RS256)
    V-->>A: RSA private key
    A->>A: Sign JWT (RS256, 30min expiry)
    A-->>C: {access_token, role}
    C->>A: GET /auth/verify (Bearer token)
    A->>A: Verify with public key
    A-->>C: {username, role, valid: true}
```

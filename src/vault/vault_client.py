"""
Vault Secret Integration
Replaces hardcoded env vars with HashiCorp Vault agent paths
In production: secrets are injected at /vault/secrets/ by Vault Agent sidecar
"""
import os

# Vault secret paths (injected by Vault Agent sidecar at runtime)
VAULT_SECRETS_PATH = os.environ.get("VAULT_SECRETS_PATH", "/vault/secrets")

def get_secret(secret_name: str) -> str:
    """
    Read secret from Vault agent-injected file.
    Falls back to environment variable for local dev.
    """
    vault_file = f"{VAULT_SECRETS_PATH}/{secret_name}"
    
    # Try Vault agent path first
    if os.path.exists(vault_file):
        with open(vault_file, "r") as f:
            return f.read().strip()
    
    # Fallback to env var for local development
    env_val = os.environ.get(secret_name.upper())
    if env_val:
        return env_val
    
    raise ValueError(f"Secret '{secret_name}' not found in Vault or environment")


# Example usage in auth service:
# Instead of: JWT_SECRET = "hardcoded_secret"
# Use:        JWT_SECRET = get_secret("jwt-private-key")
#
# Vault path structure:
#   /vault/secrets/jwt-private-key    -> RSA private key
#   /vault/secrets/redis-password     -> Redis auth password
#   /vault/secrets/db-password        -> Database password (future)
#
# Vault policy (in iac/vault-policy.hcl):
#   path "secret/data/securevault/*" {
#     capabilities = ["read"]
#   }

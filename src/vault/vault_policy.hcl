# Vault policy for SecureVault Bank services
# Each service only reads its own secrets (least privilege)

path "secret/data/securevault/auth/*" {
  capabilities = ["read"]
}

path "secret/data/securevault/user/*" {
  capabilities = ["read"]
}

path "secret/data/securevault/transaction/*" {
  capabilities = ["read"]
}

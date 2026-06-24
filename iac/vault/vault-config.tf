terraform {
  required_providers {
    vault = { 
      source  = "hashicorp/vault" 
      version = ">= 3.0" 
    }
  }
}

provider "vault" {
  address = "http://127.0.0.1:8200"
}

# 1. Key-Value Engine for Static Secrets
resource "vault_mount" "kv" {
  path    = "secret"
  type    = "kv"
  options = { version = "2" }
}

# 2. Enable Kubernetes Authentication Backend
resource "vault_auth_backend" "kubernetes" {
  type = "kubernetes"
}

# 3. Enable and Configure Database Engine for Postgres
resource "vault_database_secrets_mount" "postgres" {
  path = "database"

  postgresql {
    name              = "postgres"
    connection_url    = "postgresql://{{username}}:{{password}}@postgres.data-system.svc.cluster.local:5432/authdb?sslmode=disable"
    allowed_roles     = ["auth-service-db-role"]
    username          = "postgres"
    password          = "postgres"
    verify_connection = false  # <--- YEH HAI WOH MAGIC LINE JO ERROR KHATAM KAREGI!
  }
}

# 4. Create Database Secret Role for Auth Service
resource "vault_database_secret_backend_role" "auth_service" {
  backend             = vault_database_secrets_mount.postgres.path
  name                = "auth-service-db-role"
  db_name             = "postgres"
  creation_statements = [
    "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';",
    "GRANT SELECT, INSERT, UPDATE ON auth_users TO \"{{name}}\";"
  ]
  default_ttl         = 3600
  max_ttl             = 86400
}

# 5. Define Vault Access Policy for Applications
resource "vault_policy" "auth_service" {
  name   = "auth-service-policy"
  policy = <<EOT
path "secret/data/auth/*" { capabilities = ["read"] }
path "database/creds/auth-service-db-role" { capabilities = ["read"] }
EOT
}

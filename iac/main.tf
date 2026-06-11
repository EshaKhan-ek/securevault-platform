terraform {
  required_version = ">=1.6.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">=2.0.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "< 3.0.0" 
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

resource "kubernetes_namespace_v1" "namespaces" {
  for_each = toset(["auth-system", "app-system", "data-system", "monitoring", "security"])

  metadata {
    name = each.value
    labels = {
      "pod-security.kubernetes.io/enforce" = "restricted"
      "managed-by"                         = "terraform"
    }
  }
}

# Vault Deployment - With specific version to avoid bug
resource "helm_release" "vault" {
  name       = "vault"
  repository = "https://helm.releases.hashicorp.com"
  chart      = "vault"
  version    = "0.24.0" # Locking version to prevent resolution errors
  namespace  = "security"
  depends_on = [kubernetes_namespace_v1.namespaces]
  wait = false
  set {
    name  = "server.ha.enabled"
    value = "true"
  }

  set {
    name  = "server.ha.replicas"
    value = "3"
  }
}

# Kyverno aur Falco hata diye hain kyunki wo pehle hi cluster mein hain

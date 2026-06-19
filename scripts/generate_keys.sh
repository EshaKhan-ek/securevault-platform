#!/usr/bin/env bash
set -e

KEY_DIR="src/auth_service"
PRIVATE_KEY="$KEY_DIR/private.pem"
PUBLIC_KEY="$KEY_DIR/public.pem"

mkdir -p "$KEY_DIR"

if [ ! -f "$PRIVATE_KEY" ]; then
  echo "Generating RSA private key..."
  openssl genpkey -algorithm RSA -out "$PRIVATE_KEY" -pkeyopt rsa_keygen_bits:2048
fi

if [ ! -f "$PUBLIC_KEY" ]; then
  echo "Generating RSA public key..."
  openssl rsa -pubout -in "$PRIVATE_KEY" -out "$PUBLIC_KEY"
fi

chmod 600 "$PRIVATE_KEY"
chmod 644 "$PUBLIC_KEY"

echo "RSA keys are ready:"
echo "  $PRIVATE_KEY"
echo "  $PUBLIC_KEY"

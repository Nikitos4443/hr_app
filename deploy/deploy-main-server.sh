#!/usr/bin/env bash
# Runs ON the main-server EC2 instance (via SSM) with the release tarball already extracted.
# Usage: deploy-main-server.sh <extracted-release-dir> <aws-region>
set -euo pipefail

RELEASE_DIR="$1"
REGION="$2"
BASE=/opt/hrapp

# Backend sources (keep local state: .env, sqlite db, venv)
rsync -a --delete \
  --exclude '.venv' --exclude '.env' --exclude '*.db' --exclude '__pycache__' \
  "$RELEASE_DIR/app/" "$BASE/app/"

# Frontend build
rsync -a --delete "$RELEASE_DIR/client/" "$BASE/client/"

# Python deps (uv downloads the interpreter pinned in .python-version if needed)
cd "$BASE/app"
UV_PYTHON_INSTALL_DIR="$BASE/python" uv sync --frozen --no-dev --no-editable --package server

chown -R hrapp:hrapp "$BASE/app"
chmod -R a+rX "$BASE/client" "$BASE/python"

# Public address Caddy serves (and gets a certificate for): custom domain or the AWS hostname (IMDSv2)
if [ -n "${SITE_ADDRESS_OVERRIDE:-}" ]; then
  SITE_ADDRESS="$SITE_ADDRESS_OVERRIDE"
else
  IMDS_TOKEN=$(curl -fsS -X PUT http://169.254.169.254/latest/api/token -H 'X-aws-ec2-metadata-token-ttl-seconds: 60')
  SITE_ADDRESS=$(curl -fsS -H "X-aws-ec2-metadata-token: $IMDS_TOKEN" http://169.254.169.254/latest/meta-data/public-hostname)
fi
echo "SITE_ADDRESS=$SITE_ADDRESS" > /etc/caddy/env

# Web server config and systemd units
install -m 644 "$RELEASE_DIR/Caddyfile" /etc/caddy/Caddyfile
install -m 644 "$RELEASE_DIR/caddy.service" "$RELEASE_DIR/hrapp.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable hrapp
SITE_ADDRESS="$SITE_ADDRESS" caddy validate --config /etc/caddy/Caddyfile
systemctl restart hrapp
systemctl enable caddy
systemctl is-active --quiet caddy && systemctl reload caddy || systemctl start caddy

# Fail the deploy if the backend does not come up
for _ in $(seq 1 15); do
  if curl -fs -o /dev/null "http://127.0.0.1:8000/docs"; then
    echo "main server is up"
    exit 0
  fi
  sleep 2
done
journalctl -u hrapp -n 50 --no-pager
exit 1

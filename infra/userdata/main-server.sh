# EC2 user data for MainServerStack (runs once, on first boot, as root).
# CDK prepends: APP_DIR, CADDY_VERSION.
# Only installs software and creates users/dirs. Config (Caddyfile, systemd units) and code
# are installed by deploy/deploy-main-server.sh on every deploy.
set -euxo pipefail

dnf install -y rsync tar gzip

# uv (manages the Python interpreter and backend deps)
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh

# Caddy: static binary
curl -fsSL "https://github.com/caddyserver/caddy/releases/download/v${CADDY_VERSION}/caddy_${CADDY_VERSION}_linux_amd64.tar.gz" \
  | tar -xz -C /usr/local/bin caddy

# Service users and directories
useradd --system --home-dir "$APP_DIR" --shell /sbin/nologin hrapp || true
useradd --system --home-dir /var/lib/caddy --create-home --shell /sbin/nologin caddy || true
mkdir -p "$APP_DIR"/{app,client,python} /etc/caddy

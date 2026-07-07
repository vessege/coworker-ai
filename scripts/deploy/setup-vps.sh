#!/usr/bin/env bash
# CoWorker AI — one-shot VPS deploy (Ubuntu/Debian).
# Run ON the VPS from the repo root:  sudo bash scripts/deploy/setup-vps.sh
# Idempotent: safe to re-run after git pull to redeploy.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
API_DIR="$REPO_DIR/apps/api"
WEB_DIR="$REPO_DIR/apps/web"
PUBLIC_IP="$(curl -s ifconfig.me || hostname -I | awk '{print $1}')"

echo "==> CoWorker AI deploy: repo=$REPO_DIR ip=$PUBLIC_IP"

# ---------- 1. System packages ----------
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv python3-pip nginx curl git

# Node 20 (NodeSource) if missing or too old
if ! command -v node >/dev/null || [ "$(node -v | cut -c2-3)" -lt 18 ]; then
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  apt-get install -y -qq nodejs
fi
echo "==> node $(node -v), python $(python3 --version)"

# ---------- 2. API (FastAPI + venv) ----------
cd "$API_DIR"
python3 -m venv .venv
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q -r requirements.txt

# .env (created once; edit later to add keys, then: systemctl restart coworker-api)
if [ ! -f "$API_DIR/.env" ]; then
  cat > "$API_DIR/.env" <<EOF
APP_ENV=production
DEFAULT_MODEL=claude-sonnet-5
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
CORS_ORIGINS=["http://$PUBLIC_IP"]
EOF
  echo "==> Created $API_DIR/.env — add your ANTHROPIC_API_KEY there."
fi

# Tenants file (production requires real keys; generate one if absent)
mkdir -p "$REPO_DIR/config"
if [ ! -f "$REPO_DIR/config/tenants.json" ]; then
  TKEY="ck_live_$(head -c16 /dev/urandom | md5sum | cut -c1-24)"
  cat > "$REPO_DIR/config/tenants.json" <<EOF
[{"id": "pilot", "name": "Pilot tenant", "api_key": "$TKEY", "plan": "pilot", "credit_limit": 10000}]
EOF
  echo "==> Generated tenant API key: $TKEY  (config/tenants.json)"
fi

# ---------- 3. Web (Next.js build) ----------
cd "$WEB_DIR"
TENANT_KEY="$(python3 -c "import json;print(json.load(open('$REPO_DIR/config/tenants.json'))[0]['api_key'])")"
cat > .env.local <<EOF
NEXT_PUBLIC_API_URL=http://$PUBLIC_IP
NEXT_PUBLIC_API_KEY=$TENANT_KEY
EOF
npm install --no-audit --no-fund
npm run build

# ---------- 4. systemd services ----------
cat > /etc/systemd/system/coworker-api.service <<EOF
[Unit]
Description=CoWorker AI API
After=network.target
[Service]
WorkingDirectory=$API_DIR
ExecStart=$API_DIR/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
EnvironmentFile=$API_DIR/.env
[Install]
WantedBy=multi-user.target
EOF

cat > /etc/systemd/system/coworker-web.service <<EOF
[Unit]
Description=CoWorker AI Web
After=network.target
[Service]
WorkingDirectory=$WEB_DIR
ExecStart=$(command -v npx) next start -p 3000
Restart=always
[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now coworker-api coworker-web
systemctl restart coworker-api coworker-web

# ---------- 5. nginx reverse proxy (port 80) ----------
cat > /etc/nginx/sites-available/coworker <<'EOF'
server {
    listen 80 default_server;
    server_name _;
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
    }
}
EOF
ln -sf /etc/nginx/sites-available/coworker /etc/nginx/sites-enabled/coworker
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

# ---------- 6. Smoke test ----------
sleep 3
echo "==> API health: $(curl -s http://127.0.0.1:8000/api/v1/health || echo FAIL)"
echo "==> Web: HTTP $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3000)"
echo ""
echo "DONE. Open:  http://$PUBLIC_IP"
echo "Tenant API key (for the web + pilots): $TENANT_KEY"
echo "To enable live LLM: edit $API_DIR/.env (ANTHROPIC_API_KEY=...), then: systemctl restart coworker-api"

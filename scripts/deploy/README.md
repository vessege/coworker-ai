# VPS Deploy (Ubuntu/Debian, one command)

## First deploy
SSH into the VPS, then:
```bash
git clone https://github.com/vessege/coworker-ai.git
cd coworker-ai
git checkout claude/coworker-knowledge-base-nv7p9b
sudo bash scripts/deploy/setup-vps.sh
```
(If the repo is private, use a GitHub personal access token in the clone URL.)

The script installs Python/Node/nginx, builds the web app, creates
`coworker-api` and `coworker-web` systemd services, and serves everything on
**port 80** (web at `/`, API at `/api/`). It prints the site URL and the
generated tenant API key at the end.

## Enable live LLM
```bash
sudo nano apps/api/.env        # set ANTHROPIC_API_KEY=sk-ant-...
sudo systemctl restart coworker-api
```

## Update to a new version
```bash
cd coworker-ai && git pull && sudo bash scripts/deploy/setup-vps.sh
```

## Useful commands
```bash
systemctl status coworker-api coworker-web    # status
journalctl -u coworker-api -n 50              # API logs
curl http://127.0.0.1:8000/api/v1/health      # health
```

## Security checklist (after deploy)
- Google Cloud firewall: allow **80/443** inbound; keep 22 restricted to your IP if possible.
- Prefer SSH keys over passwords; change the password after sharing it anywhere.
- `config/tenants.json` holds real API keys — never commit it (already gitignored).
- Add a domain + HTTPS later: `apt install certbot python3-certbot-nginx && certbot --nginx`.

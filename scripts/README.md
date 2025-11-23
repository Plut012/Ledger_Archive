# Scripts

Quick commands to run the Interstellar Archive Terminal.

## Usage

### 🚀 Run Locally
```bash
./scripts/run.sh
```
Starts the server on http://localhost:8000 and opens your browser.
- Auto-starts backend
- Opens browser automatically
- Press Ctrl+C to stop

---

### ☁️ Deploy with Public URL
```bash
./scripts/deploy.sh
# or
./scripts/deploy-local.sh
```
Deploys with a public Cloudflare URL that anyone can access.
- Starts local server
- Creates Cloudflare tunnel
- Gives you a shareable `https://` link
- Press Ctrl+C to stop

**Requires:** `cloudflared` installed ([install instructions](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/))

---

### 🛑 Stop All Processes
```bash
./scripts/stop.sh
```
Stops any running servers or tunnels from this project.
- Stops backend server
- Stops Cloudflare tunnel
- Cleans up orphaned processes
- Safe: won't kill your browser

---

## Quick Reference

| Command | What it does | When to use |
|---------|-------------|-------------|
| `run.sh` | Local development | Working on the project locally |
| `deploy.sh` | Public shareable link | Demoing to others remotely |
| `stop.sh` | Stop everything | Clean up after deploy or run |

---

## Examples

### Local Development
```bash
# Start local server
./scripts/run.sh

# Make some changes...

# Stop server (Ctrl+C or run stop.sh)
./scripts/stop.sh
```

### Share with Others
```bash
# Deploy with public URL
./scripts/deploy.sh

# Copy the URL from output:
#   🌍 YOUR PUBLIC SHAREABLE LINK:
#   https://random-name-abc.trycloudflare.com

# Share that link with anyone!

# When done, press Ctrl+C
```

### Quick Reset
```bash
# Stop everything and start fresh
./scripts/stop.sh
./scripts/run.sh
```

---

## Troubleshooting

### "Port 8000 is already in use"
The scripts will detect this and offer to stop the existing process. If it fails:
```bash
./scripts/stop.sh  # Force stop everything
./scripts/run.sh   # Try again
```

### "cloudflared not found" (deploy only)
Install cloudflared:
```bash
# macOS
brew install cloudflare/cloudflare/cloudflared

# Linux
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
sudo chmod +x /usr/local/bin/cloudflared
```

### Browser doesn't open automatically
Manually visit: http://localhost:8000

---

## What Each Script Does

### run.sh
1. Checks if port 8000 is free (offers to stop if not)
2. Starts `uv run python backend/main.py` in background
3. Waits for server to be ready
4. Opens http://localhost:8000 in your browser
5. Saves PID to `/tmp/archive-server.pid`
6. Waits for Ctrl+C, then cleans up

### deploy.sh (deploy-local.sh)
1. Checks for `cloudflared` and `uv`
2. Checks if port 8000 is free
3. Starts backend server
4. Tests server health
5. Starts Cloudflare tunnel
6. Extracts and displays public URL
7. Tests tunnel connectivity
8. Waits for Ctrl+C, then stops everything

### stop.sh
1. Stops server (from `/tmp/archive-server.pid`)
2. Stops tunnel (from `/tmp/cloudflared.pid`)
3. Kills orphaned Python processes on port 8000 (safely)
4. Kills stray cloudflared processes
5. Cleans up PID files

---

**All scripts are designed to be safe** - they won't kill your browser or other important processes.

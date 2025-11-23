# Deployment Guide

How to deploy the Interstellar Archive Terminal and share it with others.

---

## 🚀 Quick Deploy (Recommended)

**One command to share your app publicly:**

```bash
./scripts/deploy-local.sh
```

This will:
1. ✅ Start the backend server
2. ✅ Create a secure Cloudflare tunnel
3. ✅ Give you a public HTTPS URL
4. ✅ Keep everything running

**Output:**
```
═══════════════════════════════════════════
✓ DEPLOYMENT SUCCESSFUL!
═══════════════════════════════════════════

🌍 Public URL:
   https://your-random-name.trycloudflare.com

📊 Local URL:
   http://localhost:8000
```

**Share the public URL with anyone!** They can access it from anywhere in the world.

---

## 📋 Prerequisites

### Install Cloudflare Tunnel

**macOS:**
```bash
brew install cloudflare/cloudflare/cloudflared
```

**Linux (Debian/Ubuntu):**
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

**Linux (Other):**
```bash
# Download appropriate binary from:
# https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
```

**Verify installation:**
```bash
cloudflared --version
```

---

## 🎮 Usage

### Start Deployment
```bash
./scripts/deploy-local.sh
```

The script will:
- Check dependencies
- Start the server
- Create tunnel
- Display your public URL

**Keep the terminal window open!** The app stays online as long as the script runs.

### Stop Deployment
Press `Ctrl+C` in the terminal, or run:
```bash
./scripts/stop.sh
```

### View Logs
```bash
# Server logs
tail -f /tmp/archive-server.log

# Tunnel logs
tail -f /tmp/cloudflared.log
```

---

## 🌐 Deployment Options

### Option 1: Temporary URL (Current Setup)

**What you get:**
- Random URL like `https://xyz-abc-123.trycloudflare.com`
- Changes each time you deploy
- **Free forever**
- HTTPS automatic
- No account needed

**Use case:** Quick demos, sharing with friends

### Option 2: Fixed Custom Domain

Want a permanent URL like `archive.yourdomain.com`?

**Steps:**
1. Sign up for Cloudflare (free)
2. Add your domain to Cloudflare
3. Create a named tunnel:
   ```bash
   cloudflared tunnel login
   cloudflared tunnel create archive-terminal
   cloudflared tunnel route dns archive-terminal archive.yourdomain.com
   ```
4. Run with config:
   ```bash
   cloudflared tunnel run archive-terminal
   ```

**See:** [Cloudflare Tunnel Docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)

### Option 3: Alternative Services

**ngrok** (simpler but has limits):
```bash
# Install
brew install ngrok

# Run
ngrok http 8000
```

Free tier: Random URLs, limited hours/month
Paid ($8/mo): Fixed domains

**Tailscale Funnel** (private network + public access):
```bash
# Install Tailscale from tailscale.com
tailscale funnel 8000
```

---

## 🔒 Security Notes

### Current Setup (Cloudflare Quick Tunnels)
- ✅ HTTPS automatic
- ✅ No ports opened on your router
- ✅ Cloudflare DDoS protection
- ⚠️ URL is public (anyone with the link can access)
- ⚠️ No authentication built-in

### Production Recommendations

If deploying for real-world use, consider:

1. **Add authentication** - Protect the app with login
2. **Use named tunnel** - More control and monitoring
3. **Rate limiting** - Prevent abuse
4. **Analytics** - Track usage

**For this educational project**, the current setup is perfect for demos and learning!

---

## 📊 Monitoring

### Check if it's running
```bash
# Check server
curl http://localhost:8000

# Check tunnel
curl https://your-url.trycloudflare.com
```

### Common Issues

**Port 8000 already in use:**
```bash
# Kill existing process
./scripts/stop.sh
# Or manually:
kill $(lsof -t -i:8000)
```

**Tunnel won't start:**
```bash
# Check cloudflared installation
cloudflared --version

# Check logs
tail -f /tmp/cloudflared.log
```

**Server won't start:**
```bash
# Check dependencies
uv sync

# Check logs
tail -f /tmp/archive-server.log

# Try manually
uv run python backend/main.py
```

---

## 🎯 Real Deployment (VPS/Cloud)

For 24/7 availability, deploy to a server:

### Quick Deploy to Cloud

**Using Railway** (easiest):
1. Push to GitHub
2. Connect to Railway
3. Deploy

**Using Render** (free tier):
1. Push to GitHub
2. Connect to Render
3. Deploy as web service

**Using DigitalOcean/Linode** (most control):
```bash
# On server:
git clone your-repo
cd chain
uv sync
# Run with systemd or supervisor
```

Want a guide for cloud deployment? Let me know!

---

## 📱 Access from Phone/Tablet

Once deployed with Cloudflare tunnel:
1. Open the public URL on any device
2. Works on mobile browsers
3. Full responsive terminal experience

---

## 💡 Tips

- **Keep laptop awake**: Use caffeine/amphetamine to prevent sleep
- **Stable internet**: WiFi or ethernet recommended
- **Share safely**: Only share URL with people you trust
- **Custom domain**: Makes URL easier to remember and share
- **Restart anytime**: Just run deploy script again

---

## 🆘 Need Help?

Check logs first:
```bash
tail -f /tmp/archive-server.log
tail -f /tmp/cloudflared.log
```

Common commands:
```bash
./scripts/deploy-local.sh   # Start
./scripts/stop.sh            # Stop
uv run pytest               # Test
```

---

**Happy deploying! 🚀**

*"In the vastness of space, truth is the only constant. The ledger remembers all."*

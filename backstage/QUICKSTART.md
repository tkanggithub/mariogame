# Backstage Quick Start - 5 Minutes to Portal

## Step 0: Start Docker (if needed)

**If you see "connect: no such file or directory" error, Docker daemon isn't running:**

### macOS
```bash
# Start Docker from Applications folder, or:
open -a Docker

# Wait for Docker icon to appear in menu bar
```

### Ubuntu/Linux
```bash
# Start Docker daemon
sudo systemctl start docker

# Or with podman (if using podman instead):
systemctl --user start podman.socket
```

### Windows
- Open Docker Desktop application
- Wait for it to fully load

## Step 1: Get GitHub Token (1 minute)

**IMPORTANT: Do this FIRST before starting Backstage**

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name it: `backstage-mario-game`
4. Check these scopes:
   - `repo` (full control)
   - `read:org` (read org members)
   - `read:user` (read user profile)
5. Click **"Generate token"**
6. **Copy the token** (you won't see it again!)

## Step 1.5: Set Token in Terminal (30 seconds)

**In your terminal, before running anything:**

```bash
# Paste your token here:
export GITHUB_TOKEN="ghp_your_token"

# Verify it worked:
echo $GITHUB_TOKEN
# Should show: ghp_...
```

**Keep this terminal open** when starting Backstage, or add to your shell:
```bash
# ~/.bashrc or ~/.zshrc
export GITHUB_TOKEN="ghp_your_token"
```

## Step 2: Start Backstage (2 minutes)

**Make sure Docker is running and GITHUB_TOKEN is set!**

```bash
# Verify token is set
echo $GITHUB_TOKEN
# Should show: ghp_...

# Start Backstage
cd backstage
bash start.sh docker
```

**Wait for this message:**
```
✅ Containers started!
🌐 Access Backstage:
   Frontend: http://localhost:3000
```

If you see errors about Docker/Podman, check the [Troubleshooting](#troubleshooting) section below.

## Step 3: Access Portal (1 minute)

Open http://localhost:3000 in your browser

**You should see:**
- 🏠 Home page with team info
- 📊 Catalog showing "Mario Obstacle Game" component
- 🔍 Search box
- 📚 Documentation section
- 🎯 Create templates button

## Step 4: Explore (1 minute)

### View the Mario Game Component
1. Click **"Catalog"** in left sidebar
2. You'll see **"Mario Obstacle Game"** listed
3. Click on it to see:
   - ✅ Component details
   - ✅ Owner (game-dev-team)
   - ✅ Live game link (http://localhost:3030)
   - ✅ GitHub repository link
   - ✅ Dependencies and relationships

### See Your Team
1. Click **"Home"**
2. Scroll down to see team members
3. See their roles and emails

## What's Now Available

✅ **Centralized Catalog** - All components in one place
✅ **GitHub Integration** - Automatic team and repo sync
✅ **Team Directory** - Find team members and their roles
✅ **Documentation Hub** - TechDocs integration ready
✅ **Search** - Full-text search across all components
✅ **Templates** - Ready for scaffolding new features

## Next: Add More Components

Other repositories can be discovered by adding `catalog-info.yaml`:

```yaml
# In any GitHub repo root
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-feature
  title: My Feature Name
spec:
  type: service
  owner: game-dev-team
  lifecycle: production
  links:
    - url: https://github.com/myorg/myrepo
      title: Repository
```

Then add to Backstage `catalog` config.

## Troubleshooting

### "GITHUB_TOKEN variable is not set"
**Problem:** You didn't set the token before starting

**Solution:**
```bash
# Set the token in current terminal
export GITHUB_TOKEN="ghp_your_token"

# Verify it's set
echo $GITHUB_TOKEN

# Now start Backstage
bash start.sh docker
```

### "unable to get image 'node:20-alpine'" or "no such file or directory"
**Problem:** Docker daemon isn't running

**Solution:**

**macOS:**
```bash
# Start Docker Desktop app
open -a Docker

# Wait 30 seconds for it to fully load, see icon in menu bar
# Then try again
bash start.sh docker
```

**Ubuntu/Linux with systemd:**
```bash
# Start Docker
sudo systemctl start docker

# Verify it's running
sudo docker ps

# Try again
bash start.sh docker
```

**Ubuntu/Linux with podman:**
```bash
# Start podman socket
systemctl --user start podman.socket

# Verify
podman ps

# Try again
bash start.sh docker
```

**Windows:**
- Open Docker Desktop application
- Wait for it to fully start (icon appears in system tray)
- Try again

### Cannot connect to Docker API
**Problem:** Docker socket permission or daemon not running

**Solution:**
```bash
# Check if Docker is running
docker ps

# If not found, install Docker:
# Visit: https://docs.docker.com/get-docker/

# If permission denied, add user to docker group:
sudo usermod -aG docker $USER
# You may need to log out/in after this
```

### Can't see Mario game component?
1. Check `catalog-info.yaml` exists in repo root ✓
2. Check GitHub token has `read:org` scope ✓
3. Reload browser (Cmd+Shift+R) ✓
4. Check backend logs: `docker-compose logs backstage` ✓

### "Connection refused" error?
1. Is Backstage running? `docker ps` should show containers
2. Wait 30 seconds for startup
3. Check ports aren't in use:
   ```bash
   lsof -i :3000  # Frontend
   lsof -i :7007  # Backend
   ```

### Port 3000 already in use?
```bash
# Kill process on port 3000
kill -9 $(lsof -t -i :3000)

# Or use different port
FRONTEND_PORT=3001 bash start.sh docker
```

## Common Tasks

### Stop Backstage
```bash
# Docker
docker-compose down

# Local
Ctrl+C
```

### View Logs
```bash
# Docker
docker-compose logs -f backstage

# Local
(Already visible in terminal)
```

### Restart Services
```bash
docker-compose restart
```

### Reset Database (Docker)
```bash
docker-compose down -v  # -v removes volumes
docker-compose up
```

## Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | Web UI |
| **Backend** | http://localhost:7007 | REST API |
| **Mario Game** | http://localhost:3030 | Game server |
| **Database** | localhost:5432 | PostgreSQL (Docker only) |

## Key Features to Try

### 1. View Component Details
1. Go to Catalog
2. Click "Mario Obstacle Game"
3. See all linked resources

### 2. Search Everything
1. Click Search icon (🔍) at top
2. Type "mario" or "game"
3. Find components, docs, teams

### 3. Manage Team
1. The home page shows team members
2. GitHub org teams auto-sync
3. Add more via `app-config.yaml`

### 4. Documentation
1. Go to "Docs" tab
2. View centralized documentation
3. Add mkdocs.yml to enable for components

## Tips & Tricks

💡 **Performance:**
- First startup takes 2-3 minutes (Docker)
- Subsequent starts are instant
- Reload only takes 5-10 seconds

💡 **Development:**
- Edit `app-config.yaml` for quick changes
- Restart backend only: `docker-compose restart backstage`
- Local mode supports hot reload

💡 **Security:**
- Never commit `.env` file
- Use `.env.example` as template
- Rotate tokens regularly

💡 **Scaling:**
- Add components with `catalog-info.yaml`
- Use GitHub org for team discovery
- PostgreSQL recommended for 100+ components

## Next Steps

1. ✅ Portal is running
2. 🔗 Explore catalog and team
3. 📚 Add documentation (optional)
4. 👥 Invite team members
5. 🚀 Create software templates for features

## Getting Help

- **Official Docs**: https://backstage.io
- **Community**: https://github.com/backstage/backstage
- **Issues**: Check GitHub issues for solutions

---

**🎉 You're all set! Welcome to Backstage!**

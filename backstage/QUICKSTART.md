# Backstage Quick Start - 5 Minutes to Portal

## Step 0: Setup Podman Rootless (1 minute)

**For unprivileged user access without sudo:**

```bash
# Start the podman socket for your user
systemctl --user start podman.socket

# Make it auto-start on login
systemctl --user enable podman.socket

# Verify it's running
systemctl --user status podman.socket
```

If you need to install podman-compose:
```bash
# Install via pip (recommended)
pip install podman-compose

# Or via package manager
apt install podman-compose        # Ubuntu/Debian
brew install podman-compose       # macOS
```

**Cgroup Status:**
The script will automatically detect your cgroup version (v1 or v2). Podman works with both!

### Alternative: Start Docker service (if using Docker instead of Podman)

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

**Make sure Podman socket is running and GITHUB_TOKEN is set!**

```bash
# Verify podman socket is running
systemctl --user status podman.socket
# Should show: active (running)

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
   Frontend: http://localhost:8000
   Backend:  http://localhost:8007
   Game:     http://localhost:8030
```

The script automatically:
- ✅ Detects Podman/Docker
- ✅ Starts podman.socket if needed
- ✅ Shows cgroup version (v1 or v2)
- ✅ Builds and starts containers
- ✅ Uses unprivileged user ports (no sudo needed)

If you see errors about podman socket, check troubleshooting below.

## Step 3: Access Portal (1 minute)

Open http://localhost:8000 in your browser

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
   - ✅ Live game link (http://localhost:8030)
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

### Podman socket not running
**Problem:** "connect: no such file or directory" error

**Solution:**
```bash
# Start podman socket for current user
systemctl --user start podman.socket

# Make it auto-start
systemctl --user enable podman.socket

# Verify it's running
systemctl --user status podman.socket
# Should show: active (running)

# Now try again
bash start.sh docker
```

### Podman socket issues on cgroup v1 systems
**Problem:** Some older systems use cgroup v1 instead of v2

**Solution:**
The script automatically detects your cgroup version and works with both!
You can check your version:

```bash
# Check cgroup version
podman info | grep -i cgroup

# Or use this:
grep cgroup2 /proc/mounts
# If output is empty, you're on cgroup v1 (still works!)
```

Backstage works perfectly with both cgroup v1 and v2.

### "unable to get image" error
**Problem:** Container image download failed

**Solution:**
```bash
# This usually means internet connectivity or DNS issues
# Try pulling manually first

podman pull node:20-alpine
podman pull postgres:16-alpine
podman pull python:3.11-slim

# Then try starting again
bash start.sh docker
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

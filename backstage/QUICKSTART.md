# Backstage Quick Start - 5 Minutes to Portal

## Step 1: Get GitHub Token (1 minute)

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name it: `backstage-mario-game`
4. Check these scopes:
   - `repo` (full control)
   - `read:org` (read org members)
   - `read:user` (read user profile)
5. Click **"Generate token"**
6. **Copy the token** (you won't see it again!)

## Step 2: Start Backstage (2 minutes)

### Using Docker (Recommended)

```bash
cd backstage

# For first time
export GITHUB_TOKEN="ghp_your_token"

# Start everything
bash start.sh docker
```

**Wait for this message:**
```
✅ Containers started!
🌐 Access Backstage:
   Frontend: http://localhost:3000
```

### Using Local Development

```bash
cd backstage

# Create .env file
cp .env.example .env
# Edit .env and add your GITHUB_TOKEN

# Install and start
bash start.sh local
```

**Wait for:**
```
🚀 Frontend started at http://localhost:3000
🚀 Backend started at http://localhost:7007
```

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

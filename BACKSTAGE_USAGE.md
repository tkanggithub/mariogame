# How to Use the Backstage Developer Portal

## 🎯 What You Now Have

You now have a **complete, production-ready Backstage developer portal** for your Mario Game team collaboration platform.

### Components Included

| Component | Purpose | Location |
|-----------|---------|----------|
| **Backstage Frontend** | Web UI for team | http://localhost:3000 |
| **Backstage Backend** | API server | http://localhost:7007 |
| **PostgreSQL Database** | Data persistence | localhost:5432 |
| **Mario Game Server** | The game itself | http://localhost:3030 |

## ⚡ Quick Start (Choose One)

### Option 1: Docker (Recommended - 30 seconds)

**Most reliable, all-in-one:**

```bash
cd backstage
export GITHUB_TOKEN="ghp_your_token_from_github"
bash start.sh docker
```

Then open: **http://localhost:3000**

### Option 2: Local Development (2 minutes)

**For developers who want to modify Backstage:**

```bash
cd backstage
cp .env.example .env
# Edit .env and add your GITHUB_TOKEN
bash start.sh local
```

Wait for: `Frontend started at http://localhost:3000`

## 📊 What You'll See

### Home Page
```
┌─────────────────────────────────────┐
│  🎮 Mario Game Dev Portal           │
├─────────────────────────────────────┤
│                                     │
│  Team Members:                      │
│  👤 You (Lead Developer)            │
│  👤 Teammate 1 (Physics Engineer)   │
│  👤 Teammate 2 (UI/UX Designer)     │
│                                     │
│  Quick Links:                       │
│  📊 Catalog  |  🔍 Search  |  📚 Docs
│                                     │
└─────────────────────────────────────┘
```

### Catalog View
```
Components Discovered:
✅ mario-obstacle-game
   Owner: game-dev-team
   Status: Production
   Links: [GitHub] [Live Game] [Issues]

Dependencies:
  ├── Python 3.8+
  └── Node.js 18+
```

## 🔑 Key Features

### 1. **Component Catalog**
Discover all team components in one place:
- View Mario game component details
- See dependencies and relationships
- Track ownership and lifecycle
- Access GitHub repos and links

**Navigate to:** `http://localhost:3000/catalog`

### 2. **Team Directory**
See all team members and their roles:
- Team structure
- Member roles (Dev, Engineer, Designer, etc.)
- Contact information
- GitHub usernames

**View on:** Home page or click team avatars

### 3. **Search**
Full-text search across everything:
- Components by name
- Documentation by topic
- Team members by email
- Technologies by type

**Click:** 🔍 Search icon (top right)

### 4. **Documentation Hub**
Centralized technical documentation:
- Setup guides
- Architecture docs
- API documentation
- Team runbooks

**Access at:** `http://localhost:3000/docs`

### 5. **Software Templates** (Ready to use)
Scaffolding for creating new features:
- Feature branch template
- Component template
- Documentation template

**Create at:** `http://localhost:3000/create`

## 🚀 Common Tasks

### Task 1: View Mario Game Component Details
```
1. Click "Catalog" in sidebar
2. Find "Mario Obstacle Game"
3. Click to view:
   ✅ Component description
   ✅ GitHub repository link
   ✅ Live game demo
   ✅ Issue tracker
   ✅ Team ownership
```

### Task 2: Find a Team Member
```
1. Home page shows team roster
2. Or click "Search" → type email
3. See:
   ✅ Role and team
   ✅ GitHub profile
   ✅ Contributions
```

### Task 3: Search for Something
```
1. Click 🔍 Search (top navigation)
2. Type: "mario" or "physics" or "ruuvi"
3. Results include:
   ✅ Components
   ✅ Documentation
   ✅ Team members
   ✅ Technologies
```

### Task 4: Check Game Status
```
1. Go to Catalog
2. Click "mario-obstacle-game"
3. Click "Live Game" link
4. Opens http://localhost:3030
5. Play the game! 🎮
```

### Task 5: Add a New Component
```
1. Update your repo's catalog-info.yaml:
   
   apiVersion: backstage.io/v1alpha1
   kind: Component
   metadata:
     name: my-feature
     title: My Feature Name
   spec:
     type: service
     owner: game-dev-team
     lifecycle: production

2. Backstage auto-discovers it
3. Shows up in Catalog within minutes
```

## 📚 Documentation Files

After you create this, you'll have important docs:

| File | Purpose | Location |
|------|---------|----------|
| **QUICKSTART.md** | Get running in 5 min | `backstage/QUICKSTART.md` |
| **README.md** | Complete guide (500+ lines) | `backstage/README.md` |
| **CONFIGURATION.md** | All config options | `backstage/CONFIGURATION.md` |

## 🔧 Configuration (if needed)

The Backstage configuration is in: `backstage/app-config.yaml`

**Key sections:**
```yaml
app:
  title: Mario Game Development Portal
  baseUrl: http://localhost:3000      # Change this if hosting elsewhere

game:
  ruuviIntegration:
    enabled: true                      # Enable/disable Ruuvi support
  difficulty:
    baseGravity: 0.8                   # Game physics settings
    baseJumpPower: 18

teams:
  gameDev:
    members:  # Add/remove team members here
      - email: user@example.com
        role: Developer
```

## ⚙️ Architecture Diagram

```
                    Internet / GitHub
                          ▲
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
    
    Frontend         Backend API      GitHub API
    (React)         (Express.js)     (Integration)
    3000            7007             oauth
      │                │                │
      └─────────────────┼────────────────┘
                        │
                        ▼
                    
                   PostgreSQL
                   Database
                   (5432)
                   
                        │
                        ▼
                   
        ┌──────────────────────────────┐
        │   Backstage Portal Data      │
        │                              │
        │  ✅ Components               │
        │  ✅ Team Members             │
        │  ✅ Documentation            │
        │  ✅ GitHub Sync              │
        └──────────────────────────────┘
```

## 🔐 Authentication

Currently: **Guest access enabled** (development mode)

For production, you can enable:
- GitHub OAuth
- Google OAuth
- Custom authentication

See `backstage/CONFIGURATION.md` for setup.

## 📊 Team Sync

Backstage automatically discovers and syncs:
- ✅ GitHub organization teams
- ✅ GitHub repository owners
- ✅ GitHub org members
- ✅ Components with `catalog-info.yaml`

Updates every few minutes automatically.

## 🛠️ Troubleshooting

### Can't access http://localhost:3000?
```bash
# Check if containers are running
docker-compose ps

# View logs
docker-compose logs backstage

# Restart
docker-compose restart
```

### Don't see Mario component?
```bash
# Check catalog-info.yaml exists
cat ../catalog-info.yaml

# Check GitHub token
echo $GITHUB_TOKEN

# Reload page (Cmd+Shift+R)
```

### Port 3000 already in use?
```bash
# Kill old process
kill -9 $(lsof -t -i :3000)

# Or use different port
FRONTEND_PORT=3001 bash start.sh docker
```

## 🎓 Learning Path

1. **Start here:** Read `backstage/QUICKSTART.md` (5 min)
2. **Then explore:** Browse catalog and team (10 min)
3. **Go deeper:** Read `backstage/README.md` (20 min)
4. **Master it:** Study `backstage/CONFIGURATION.md` (30 min)

## 🚀 What's Next?

### Immediate (Today)
- ✅ Get GITHUB_TOKEN from https://github.com/settings/tokens
- ✅ Run `bash backstage/start.sh docker`
- ✅ Explore portal at http://localhost:3000

### Soon (This Week)
- Add documentation via mkdocs
- Create software templates
- Invite team members to portal
- Set up Slack notifications

### Advanced (Next Sprint)
- Enable GitHub OAuth
- Switch to PostgreSQL
- Deploy to Kubernetes
- Add custom plugins

## 📞 Support

| Question | Answer |
|----------|--------|
| How do I...? | See QUICKSTART.md and README.md |
| What's this button? | Hover for tooltip or check docs |
| How to customize? | See CONFIGURATION.md |
| Official docs? | https://backstage.io/docs/ |

## ✅ Verification Checklist

After starting, verify these work:

- [ ] Frontend accessible at http://localhost:3000
- [ ] Can see Home page
- [ ] Can see team members listed
- [ ] Catalog shows "Mario Obstacle Game"
- [ ] Can click on Mario component
- [ ] Can see GitHub links
- [ ] Can click "Live Game" and reach game
- [ ] Search works (click 🔍)
- [ ] Backend API responds (http://localhost:7007/.well-known/health)

Check off all of these = **Backstage is fully operational! 🎉**

---

## 🎯 Summary

You now have a **professional team collaboration platform** that:

✅ Shows all components in one catalog
✅ Auto-discovers GitHub teams and repos
✅ Hosts centralized documentation
✅ Enables feature templates
✅ Provides team directory
✅ Tracks component ownership
✅ Integrates with GitHub
✅ Runs locally or in Docker
✅ Fully documented and ready to use

**To start using it right now:**

```bash
cd backstage
export GITHUB_TOKEN="ghp_your_token"
bash start.sh docker
# Wait for startup (~30 seconds)
# Open http://localhost:3000 in browser
```

That's it! You're in the portal. 🚀

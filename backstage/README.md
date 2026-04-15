# Backstage Developer Portal - Complete Setup Guide

## Overview

This is a **Backstage Developer Portal** for the Mario Game development team. It provides:

- 📊 **Centralized Catalog** - Discover and manage all team components
- 🔗 **GitHub Integration** - Automatic component discovery and sync
- 🎯 **Software Templates** - Scaffolding for new features and repositories
- 📚 **TechDocs Integration** - Centralized documentation hosting
- 👥 **Team Management** - Organize team members and ownership
- 🎮 **Game-Specific Features** - Track Mario game development metrics

## Quick Start (2 minutes)

### Option 1: Docker (Recommended) ⭐

**Fastest way to get started - everything in containers**

```bash
cd backstage
bash start.sh docker
```

Then open:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:7007
- **Game**: http://localhost:3030

### Option 2: Local Development

**For hands-on development and debugging**

```bash
cd backstage

# Install dependencies (one time)
yarn install

# Create .env file
cat > .env << 'EOF'
GITHUB_TOKEN=ghp_your_personal_access_token
NODE_ENV=development
LOG_LEVEL=debug
EOF

# Start in concurrent mode (frontend + backend)
yarn dev
```

Then open http://localhost:3000

## Requirements

### For Docker
- Docker (v20.10+)
- Docker Compose (v2.0+)

**Install:**
```bash
# macOS (using Homebrew)
brew install docker

# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### For Local Development
- Node.js v18.x or higher
- Yarn v3.x or higher

**Install:**
```bash
# macOS
brew install node yarn

# Ubuntu/Debian
sudo apt-get install nodejs yarn
# or via nvm: https://github.com/nvm-sh/nvm
```

## Authentication & Setup

### Get GitHub Token

To enable GitHub integration:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` - Full control of repositories
   - `read:org` - Read org members and teams
   - `read:user` - User profile data
4. Copy the token
5. Add to `.env` or `docker-compose.yml`:

```bash
GITHUB_TOKEN=ghp_your_token_here
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Backstage Developer Portal                      │
│         (Team Coordination Platform)                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐         ┌──────────────────┐    │
│  │    Frontend      │         │     Backend      │    │
│  │  (React)         │────────│  (Node.js/Expr.) │    │
│  │  Port: 3000      │         │  Port: 7007      │    │
│  └──────────────────┘         └──────────────────┘    │
│         │                               │               │
│         └───────────────┬───────────────┘               │
│                         │                               │
│            ┌────────────┴────────────┐                 │
│            │                         │                  │
│      ┌──────────────┐         ┌───────────────┐       │
│      │  PostgreSQL  │         │  GitHub API   │       │
│      │  (Database)  │         │  Integration  │       │
│      └──────────────┘         └───────────────┘       │
│                                                         │
└─────────────────────────────────────────────────────────┘
            │                    │
            │                    │
            ▼                    ▼
┌──────────────────────────┐  ┌───────────────────┐
│   Mario Game Dev Catalog │  │   GitHub Repos    │
│   catalog-info.yaml      │  │   & Teams         │
└──────────────────────────┘  └───────────────────┘
```

## File Structure

```
backstage/
├── start.sh                    # Startup script (docker/local)
├── docker-compose.yml          # Docker orchestration
├── package.json                # Root workspace
├── app-config.yaml             # Main Backstage config
├── packages/
│   ├── backend/
│   │   ├── package.json        # Backend dependencies
│   │   └── src/
│   │       └── index.ts        # Backend entry point
│   └── frontend/
│       ├── package.json        # Frontend dependencies
│       └── src/
│           └── App.tsx         # React app component
└── docs/
    └── team-catalog/          # Additional entity files
```

## Configuration

### Main Configuration: `app-config.yaml`

The main configuration file includes:

```yaml
app:
  title: Mario Game Development Portal
  baseUrl: http://localhost:3000

backend:
  baseUrl: http://localhost:7007

integrations:
  github:
    - host: github.com
      token: ${GITHUB_TOKEN}

catalog:
  locations:
    - type: file
      target: ./catalog-info.yaml

game:
  name: Mario Obstacle Game
  ruuviIntegration:
    enabled: true
```

**Key Sections:**
- `app` - Frontend configuration
- `backend` - Backend server settings
- `integrations` - External service connections
- `catalog` - Component discovery settings
- `game` - Mario-specific settings

## Features & Usage

### 1. **Component Catalog**

View all team components (discoverable from `catalog-info.yaml`):

1. Go to http://localhost:3000/catalog
2. Browse components:
   - **mario-obstacle-game** - Main game component
   - **Python Runtime** - Python dependencies
   - **Node.js Runtime** - JavaScript environment

**Add your own components:**
Create a `catalog-info.yaml` in any repository:
```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: your-component
  title: Your Component Title
spec:
  type: service
  owner: game-dev-team
  lifecycle: production
```

### 2. **Search**

Find components, docs, and team members:

1. Click Search in top navbar
2. Type component name or developer email
3. Filter by type, owner, or lifecycle

### 3. **Documentation (TechDocs)**

Centralized documentation hosting:

1. Go to http://localhost:3000/docs
2. Browse team documentation
3. Add docs via `mkdocs.yml` in repositories

**Add documentation:**
Put `mkdocs.yml` in your repo root:
```yaml
site_name: Your Component Docs
docs_dir: docs
plugins:
  - techdocs-core
```

### 4. **Software Templates**

Scaffolding for new features:

1. Go to http://localhost:3000/create
2. Select a template
3. Fill in form
4. Generate repository or feature branch

### 5. **Team Management**

View team members and their roles:

1. Go to http://localhost:3000 (Home page)
2. See team roster from `app-config.yaml`
3. GitHub integration auto-syncs org members

## Deployment Scenarios

### Scenario 1: Local Development

```bash
cd backstage
yarn dev  # Start frontend + backend concurrently
```

**Use when:**
- Developing Backstage plugins
- Testing catalog changes
- Local experimentation

### Scenario 2: Docker Deployment

```bash
cd backstage
docker-compose up
```

**Use when:**
- Team deployment
- Production-like environment
- Consistent across machines

### Scenario 3: Kubernetes (Advanced)

Deploy with Helm (see `kubernetes/` for values):
```bash
helm repo add backstage https://backstage.io
helm install backstage backstage/backstage
```

**Use when:**
- Enterprise scale
- Multi-region deployment
- Advanced monitoring needs

## Troubleshooting

### Common Issues

#### "Port 3000 already in use"
```bash
# Find process using port 3000
lsof -i :3000

# Kill it
kill -9 <PID>

# Or use different port
BACKEND_PORT=7008 yarn dev
```

#### "GITHUB_TOKEN not recognized"
```bash
# For Docker
# Edit docker-compose.yml and set GITHUB_TOKEN

# For local
export GITHUB_TOKEN="ghp_your_token"
yarn dev
```

#### "Cannot find module '@backstage/...'"
```bash
# Clear and reinstall
yarn clean
yarn install
yarn build
```

#### "Database connection failed"
```bash
# If using local PostgreSQL
brew services start postgresql

# For Docker
docker-compose up postgres -d
```

### Debug Mode

Enable verbose logging:

```bash
# For Docker
docker-compose logs -f backstage

# For local
LOG_LEVEL=debug yarn dev
```

## Integration Points

### With Mario Game

The Backstage portal tracks:
- 🎮 Game version and deployment status
- 👥 Team members and assignments
- 📊 Development metrics
- 🐛 GitHub issues and PRs
- 📚 Documentation and guides

### With GitHub

Automatic integration:
- Syncs org teams and members
- Discovers repositories with `catalog-info.yaml`
- Shows branch activity
- Links to PRs and issues

### With CI/CD

Optional setup:
- Trigger deployments from Backstage
- Report build status
- Link to deployment logs

## Plugin Ecosystem

Installed plugins:

| Plugin | Purpose | Docs |
|--------|---------|------|
| **Catalog** | Component discovery | [Link](https://backstage.io/docs/features/software-catalog/) |
| **Search** | Full-text search | [Link](https://backstage.io/docs/features/search/) |
| **TechDocs** | Documentation hosting | [Link](https://backstage.io/docs/features/techdocs/) |
| **Scaffolder** | Template scaffolding | [Link](https://backstage.io/docs/features/scaffolder/) |
| **Auth** | Authentication | [Link](https://backstage.io/docs/auth/) |
| **GitHub** | GitHub integration | [Link](https://backstage.io/docs/integrations/github/) |

## Best Practices

### 1. Keep Catalog Updated

```bash
# Catalog should always have latest entities
# Commit catalog-info.yaml to all repos
```

### 2. Document Everything

```yaml
# Every component should have description and links
metadata:
  description: Clear one-liner about component
  links:
    - url: https://github.com/...
      title: Repository
```

### 3. Ownership

```yaml
# Always assign owner (person or team)
spec:
  owner: game-dev-team  # Must exist in GitHub org
```

### 4. Lifecycle

```yaml
# Mark component status
spec:
  lifecycle: production|experimental|deprecated
```

## Support & Resources

- **Official Docs**: https://backstage.io/docs/
- **Community**: https://github.com/backstage/backstage/discussions
- **Plugins**: https://backstage.io/plugins/
- **GitHub Issues**: Report bugs at https://github.com/backstage/backstage/issues

## Environment Variables

```bash
# Required
GITHUB_TOKEN=ghp_...

# Optional
NODE_ENV=development|production
LOG_LEVEL=debug|info|warn|error
BACKEND_PORT=7007
FRONTEND_PORT=3000
```

## Performance Tips

1. **Use PostgreSQL** for production (not SQLite)
2. **Enable caching** for large catalogs
3. **Use CDN** for frontend static assets
4. **Monitor** backend resource usage
5. **Regular backups** of database

## Next Steps

1. ✅ Start Backstage (Docker or local)
2. ✅ Access http://localhost:3000
3. ✅ View Mario game component in catalog
4. ✅ Explore team members and documentation
5. ✅ Create software template for next feature
6. ✅ Invite team members to portal

---

**Backstage is ready for your team! 🚀**

For detailed questions, see official docs at https://backstage.io

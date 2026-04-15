# Backstage Configuration Guide

## Overview

Backstage configuration is primarily managed through `app-config.yaml`. This guide explains all available options for the Mario Game development portal.

## Main Configuration File Structure

```yaml
app:                    # Frontend app settings
backend:               # Backend server settings
integrations:          # External service connections
auth:                  # Authentication setup
catalog:               # Component discovery
scaffolder:            # Template engine
techdocs:              # Documentation system
kubernetes:            # K8s integration
plugins:               # Plugin configuration
game:                  # Mario game custom settings
teams:                 # Team configuration
```

## Detailed Configuration

### 1. App Configuration

```yaml
app:
  title: Mario Game Development Portal        # Browser tab and header title
  baseUrl: http://localhost:3000             # Full URL where frontend is accessible
  googleAnalyticsTrackingId: UA-XXXXXXXX-X  # Optional: Google Analytics
  support:
    url: https://github.com/tkanggithub/mariogame/issues
    items:                   # Support links in menu
      - text: Issues
        icon: github
        links:
          - url: https://github.com/issues
            title: GitHub Issues
```

### 2. Backend Configuration

```yaml
backend:
  baseUrl: http://localhost:7007           # Backend API URL
  listen:
    port: 7007                             # Backend server port
  database:
    client: better-sqlite3                 # Or: postgresql
    connection:
      filename: ./backstage.sqlite         # SQLite file path
  csp:
    connect-src:                           # CSP directives
      - "'self'"
      - 'http:'
      - 'https:'
  cors:
    origin: http://localhost:3000          # Allow frontend
    methods: [GET, HEAD, PATCH, POST, PUT, DELETE]
    credentials: true
  auth:
    externalAccess:
      - type: static
        static:
          token: ${BACKSTAGE_AUTH_TOKEN}
          subject: automation
```

### 3. GitHub Integration

```yaml
integrations:
  github:
    - host: github.com
      token: ${GITHUB_TOKEN}               # Required
      apiBaseUrl: https://api.github.com   # Use for GitHub Enterprise
      rawBaseUrl: https://raw.githubusercontent.com
```

**Required scopes for GITHUB_TOKEN:**
- `repo` - Access repositories
- `read:org` - Read org members and teams
- `read:user` - Read user profile

### 4. Authentication

```yaml
auth:
  environment: development                 # production for live
  providers:
    guest: {}                              # Guest access (dev only)
    github:                                # GitHub OAuth (optional)
      development:
        clientId: ${AUTH_GITHUB_CLIENT_ID}
        clientSecret: ${AUTH_GITHUB_CLIENT_SECRET}
    google:                                # Google OAuth (optional)
      development:
        clientId: ${AUTH_GOOGLE_CLIENT_ID}
        clientSecret: ${AUTH_GOOGLE_CLIENT_SECRET}
```

### 5. Catalog Configuration

```yaml
catalog:
  import:
    entityFilename: catalog-info.yaml     # File name to search
  rules:
    - allow:
      - Component   # Allow Components
      - API        # Allow APIs
      - Resource   # Allow Resources
      - Group      # Allow Teams
      - User       # Allow Users
      - Template   # Allow Templates
  locations:                              # Where to discover entities
    - type: file
      target: ./catalog-info.yaml         # Root catalog
      rules:
        - allow: [Component, API, Resource, Group, User, Template]
    - type: file
      target: ./docs/team-catalog/**/*.yaml
      rules:
        - allow: [Group, User, Component]
    - type: github
      target: https://github.com/tkanggithub/*/blob/master/catalog-info.yaml
      rules:
        - allow: [Component, API, Resource, Group, User, Template]
```

### 6. Scaffolder Configuration

```yaml
scaffolder:
  tasks:
    taskLogUpdateIntervallMs: 350         # Update frequency
    taskTimeout: 3600000                  # 1 hour timeout
    backstageBaseUrl: http://localhost:3000
```

### 7. TechDocs Configuration

```yaml
techdocs:
  builder: 'local'                        # or 'external'
  generator:
    runIn: 'docker'                       # Run in Docker container
    fetchTimeout: 600000                  # 10 minutes
  publisher:
    type: 'local'                         # Publish location
    local:
      publishDirectory: './site'
```

### 8. Kubernetes Integration (Optional)

```yaml
kubernetes:
  serviceLocatorMethod:
    type: 'multiTenant'  # or 'singleTenant'
  clusterLocatorMethods:
    - type: 'config'
      config:
        clusters:
          - name: local
            url: https://localhost:6443
            authProvider: serviceAccount
            serviceAccountToken: ${K8S_TOKEN}
```

### 9. Plugins Configuration

```yaml
plugins: []  # Plugins loaded are in packages/frontend/src/plugins.ts
             # and packages/backend/src/plugins/index.ts
```

### 10. Game-Specific Configuration

```yaml
game:
  name: Mario Obstacle Game
  version: 1.0.0
  port: 3030                              # Game server port
  description: Interactive platformer game
  ruuviIntegration:
    enabled: true                         # Enable Ruuvi sensors
    sensorInterval: 100                   # Poll interval (ms)
    motionThreshold: 5                    # Motion sensitivity
    jumpThreshold: 15                     # Jump trigger sensitivity
  difficulty:
    baseGravity: 0.8                      # Physics constant
    baseJumpPower: 18                     # Jump power
    spawnRate: 70                         # Obstacle spawn rate (frames)
    minDifficulty: 0.5                    # Minimum multiplier
    maxDifficulty: 2.0                    # Maximum multiplier
  features:
    obstacles: true
    powerups: true
    scoring: true
    leaderboard: false                    # Optional
    multiplayer: false                    # Future feature
```

### 11. Team Configuration

```yaml
teams:
  gameDev:                                # Team ID
    name: "Game Dev Team"                 # Display name
    description: "Mario game development team"
    members:
      - email: tkanggithub@example.com
        name: Team Lead
        role: Lead Developer
        github: tkanggithub
      - email: teammate1@example.com
        name: Developer 1
        role: Physics Engineer
        github: teammate1
      - email: teammate2@example.com
        name: Designer
        role: UI/UX Designer
        github: teammate2
```

## Environment Variables

Create a `.env` file or export variables:

```bash
# Required
GITHUB_TOKEN=ghp_...

# Optional
NODE_ENV=development|production
LOG_LEVEL=debug|info|warn|error
DATABASE_URL=postgresql://user:pass@localhost/backstage
BACKSTAGE_AUTH_TOKEN=token_for_scripts
```

## Configuration by Environment

### Development (Local)

```bash
# .env
NODE_ENV=development
LOG_LEVEL=debug
GITHUB_TOKEN=ghp_your_dev_token
```

**Features:**
- Guest authentication
- Hot reload
- Verbose logging
- SQLite database

### Production (Docker/K8s)

```bash
export NODE_ENV=production
export LOG_LEVEL=warn
export GITHUB_TOKEN=ghp_production_token
export DATABASE_URL=postgresql://...
export BACKSTAGE_AUTH_TOKEN=...
```

**Features:**
- GitHub OAuth
- PostgreSQL database
- Error tracking
- Performance monitoring

## Testing Configuration

```yaml
# app-config.test.yaml
app:
  title: Test Portal
  baseUrl: http://localhost:3001

backend:
  database:
    client: better-sqlite3
    connection:
      filename: ':memory:'  # In-memory for tests
```

Run tests with:
```bash
yarn test --config app-config.test.yaml
```

## Adding Custom Configuration

Add custom sections to `app-config.yaml`:

```yaml
# Custom game metrics
gameMetrics:
  trackingEnabled: true
  metricsInterval: 60000  # 1 minute
  includeFields:
    - playerScore
    - gameTime
    - obstaclesCollected
    - ruuviSensorActivity

# Custom integrations
slack:
  webhookUrl: ${SLACK_WEBHOOK_URL}
  channel: '#game-dev'
  notifyOn:
    - deployment
    - majorIssue
    - pullRequest
```

Access in code:
```typescript
import { useApi, configApiRef } from '@backstage/core-plugin-api';

const config = useApi(configApiRef);
const gameMetrics = config.getConfig('gameMetrics');
```

## Configuration Validation

Validate your configuration:
```bash
# Validate schema
yarn config:validate

# Check for required fields
yarn config:check-required
```

## Common Customizations

### Change Frontend Port
Edit `app-config.yaml`:
```yaml
app:
  baseUrl: http://localhost:3001  # Change port
```

### Enable PostgreSQL
```yaml
backend:
  database:
    client: postgresql
    connection:
      host: localhost
      port: 5432
      user: backstage
      password: backstage
      database: backstage
```

### Add Custom Catalog Locations
```yaml
catalog:
  locations:
    - type: github
      target: https://github.com/myorg/*/blob/master/catalog-info.yaml
```

### Enable GitHub OAuth
```yaml
auth:
  providers:
    github:
      production:
        clientId: ${AUTH_GITHUB_CLIENT_ID}
        clientSecret: ${AUTH_GITHUB_CLIENT_SECRET}
```

## Security Best Practices

1. **Never commit secrets** - Use environment variables
2. **Rotate tokens** - Update GITHUB_TOKEN regularly
3. **Use HTTPS** - In production, always use https://
4. **Limit permissions** - Give tokens only required scopes
5. **Audit access** - Monitor who accesses the portal
6. **Use PostgreSQL** - SQLite only for development

## Performance Tuning

```yaml
# For large catalogs
catalog:
  cache:
    ttl: 900000  # 15 minutes, increase for stability

# Increase worker threads
backend:
  database:
    poolMin: 10
    poolMax: 20

# CDN for static assets
app:
  staticPath: https://cdn.example.com/backstage/static
```

## Logging Configuration

```yaml
backend:
  logger:
    level: debug
    format: json  # or 'text'
    colorize: true
    transports:
      - type: console
      - type: file
        filename: ./logs/backstage.log
```

## Monitoring & Observability

```yaml
backend:
  observability:
    metrics:
      enabled: true
      otel:
        enabled: false
    tracing:
      enabled: true
      samplingRate: 0.1
```

---

**For advanced configuration, see:** https://backstage.io/docs/conf/

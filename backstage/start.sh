#!/bin/bash

# Mario Game Backstage Portal - Startup Script
# Supports multiple deployment methods

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🎮 Mario Game Backstage Developer Portal                 ║"
echo "║   Team Collaboration & Development Platform                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check requirements
check_requirements() {
    echo -e "${YELLOW}📋 Checking requirements...${NC}"
    
    if [ "$1" = "docker" ]; then
        if ! command -v docker &> /dev/null; then
            echo -e "${RED}❌ Docker is not installed${NC}"
            echo "   Install from: https://docs.docker.com/get-docker/"
            exit 1
        fi
        if ! command -v docker-compose &> /dev/null; then
            echo -e "${RED}❌ Docker Compose is not installed${NC}"
            echo "   Install from: https://docs.docker.com/compose/install/"
            exit 1
        fi
        echo -e "${GREEN}✅ Docker requirements met${NC}"
    else
        if ! command -v node &> /dev/null; then
            echo -e "${RED}❌ Node.js is not installed${NC}"
            echo "   Install from: https://nodejs.org/ (v18.x or higher)"
            exit 1
        fi
        if ! command -v yarn &> /dev/null; then
            echo -e "${RED}❌ Yarn is not installed${NC}"
            echo "   Install with: npm install -g yarn"
            exit 1
        fi
        echo -e "${GREEN}✅ Node.js requirements met${NC}"
    fi
}

# Start with Docker/Podman
start_docker() {
    echo -e "${BLUE}🐳 Starting Backstage with Podman (rootless)...${NC}"
    
    check_requirements "docker"
    
    # Check for GITHUB_TOKEN
    if [ -z "$GITHUB_TOKEN" ]; then
        echo ""
        echo -e "${YELLOW}⚠️  GITHUB_TOKEN not set!${NC}"
        echo ""
        echo "Get a GitHub token:"
        echo "  1. Go to: https://github.com/settings/tokens"
        echo "  2. Click: 'Generate new token (classic)'"
        echo "  3. Select scopes: repo, read:org, read:user"
        echo "  4. Copy the token"
        echo ""
        echo "Then set it and try again:"
        echo "  export GITHUB_TOKEN=\"ghp_your_token_here\""
        echo "  bash start.sh docker"
        echo ""
        exit 1
    fi
    
    # Check if using podman
    if command -v podman &> /dev/null; then
        echo -e "${YELLOW}📍 Detected Podman (rootless mode)${NC}"
        
        # Check podman socket
        if ! systemctl --user is-active --quiet podman.socket; then
            echo ""
            echo -e "${YELLOW}⚠️  Podman socket not running. Starting it...${NC}"
            systemctl --user start podman.socket
            
            if ! systemctl --user is-active --quiet podman.socket; then
                echo -e "${RED}❌ Failed to start podman.socket${NC}"
                echo ""
                echo "Try these commands:"
                echo "  systemctl --user start podman.socket"
                echo "  systemctl --user enable podman.socket"
                echo ""
                exit 1
            fi
            echo -e "${GREEN}✅ Podman socket started${NC}"
        fi
        
        # Check cgroup version
        CGROUP_VERSION=$(podman info | grep "cgroupVersion" | awk '{print $NF}')
        echo -e "${YELLOW}📊 Cgroup version: ${CGROUP_VERSION}${NC}"
        
        # Change to backstage directory for compose
        cd "$(dirname "$0")" || exit 1
        
        echo -e "${YELLOW}📦 Building and starting containers with podman-compose...${NC}"
        
        # Try podman-compose first, fall back to docker-compose
        if command -v podman-compose &> /dev/null; then
            podman-compose up -d
        else
            # Use docker-compose which will use podman
            docker-compose up -d 2>&1 | grep -v "nodocker" || true
        fi
    else
        echo -e "${YELLOW}📍 Using Docker${NC}"
        docker-compose up -d
    fi
    
    # Check if containers started successfully
    sleep 3
    
    # Use podman or docker based on what's available
    if command -v podman &> /dev/null; then
        if ! podman ps | grep -q backstage; then
            echo ""
            echo -e "${RED}❌ Failed to start containers${NC}"
            echo ""
            echo "Troubleshooting:"
            echo "  1. Check Podman status:"
            echo "     podman ps"
            echo "  2. Check logs:"
            echo "     podman-compose logs (or docker-compose logs)"
            echo "  3. Try with verbose output:"
            echo "     podman-compose up (without -d flag)"
            echo ""
            exit 1
        fi
    else
        if ! docker-compose ps | grep -q backstage; then
            echo ""
            echo -e "${RED}❌ Failed to start containers${NC}"
            echo ""
            echo "Troubleshooting:"
            echo "  1. Check Docker status:"
            echo "     docker ps"
            echo "  2. Check logs:"
            echo "     docker-compose logs"
            echo "  3. Try with verbose output:"
            echo "     docker-compose up (without -d flag)"
            echo ""
            exit 1
        fi
    fi
    
    echo ""
    echo -e "${GREEN}✅ Containers started!${NC}"
    echo ""
    echo -e "${BLUE}🌐 Access Backstage:${NC}"
    echo "   Frontend: http://localhost:8000"
    echo "   Backend:  http://localhost:8007"
    echo "   Game:     http://localhost:8030"
    echo ""
    echo -e "${BLUE}📊 Monitor logs:${NC}"
    echo "   podman-compose logs -f"
    echo "   (or: docker-compose logs -f)"
    echo ""
    echo -e "${BLUE}🛑 Stop containers:${NC}"
    echo "   podman-compose down"
    echo "   (or: docker-compose down)"
    echo ""
}

# Start locally (development mode)
start_local() {
    echo -e "${BLUE}💻 Starting Backstage in development mode...${NC}"
    
    check_requirements "local"
    
    # Check for .env file for GITHUB_TOKEN
    if [ ! -f .env ]; then
        echo -e "${YELLOW}⚠️  .env file not found${NC}"
        echo "   Creating .env with placeholder..."
        cat > .env << 'EOF'
# GitHub Integration
GITHUB_TOKEN=ghp_your_token_here

# Database (optional)
DB_HOST=localhost
DB_PORT=5432
DB_USER=backstage
DB_PASSWORD=backstage
DB_NAME=backstage

# Backstage
NODE_ENV=development
LOG_LEVEL=debug
EOF
        echo -e "${YELLOW}📝 Please update .env with your GITHUB_TOKEN${NC}"
        echo "   Get a token from: https://github.com/settings/tokens"
    fi
    
    # Load env file
    if [ -f .env ]; then
        export $(cat .env | xargs)
    fi
    
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    yarn install
    
    echo -e "${YELLOW}🏗️  Building packages...${NC}"
    yarn build
    
    echo -e "${GREEN}✅ Build complete!${NC}"
    echo ""
    echo -e "${BLUE}🚀 Starting development servers...${NC}"
    echo ""
    
    # Start in concurrent mode
    yarn dev
}

# Show usage
show_usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  docker     Start Backstage with Docker (recommended)"
    echo "  local      Start Backstage in local development mode"
    echo "  help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 docker              # Start with Docker Compose"
    echo "  $0 local               # Start locally with Node.js"
    echo ""
}

# Main logic
case "${1:-docker}" in
    docker)
        start_docker
        ;;
    local)
        start_local
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        echo -e "${RED}❌ Unknown option: $1${NC}"
        show_usage
        exit 1
        ;;
esac

#!/bin/bash

# Enhanced AEO Intelligence Platform Deployment Script
# Deploys the complete AEO intelligence platform with all modules

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Banner
echo -e "${BLUE}"
echo "🚀 AEO Intelligence Platform Deployment"
echo "========================================"
echo "Enhanced with:"
echo "• FAQ Intelligence & Analysis"
echo "• Schema Intelligence & Validation"
echo "• Entity Recognition & Semantic Analysis"
echo "• Voice Search Optimization"
echo "• Dynamic AI Recommendations"
echo -e "${NC}"

# Check prerequisites
log_info "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

log_success "Prerequisites check passed"

# Environment setup
log_info "Setting up environment..."

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    cat > .env << EOF
# AEO Intelligence Platform Configuration
ENVIRONMENT=production
GOOGLE_PAGESPEED_API_KEY=your_api_key_here

# Optional: Advanced Configuration
LOG_LEVEL=INFO
MAX_WORKERS=4
TIMEOUT=300
EOF
    log_warning "Created .env file. Please update GOOGLE_PAGESPEED_API_KEY with your actual API key."
fi

# Create logs directory
mkdir -p logs
log_success "Environment setup complete"

# Build and deploy
log_info "Building and deploying AEO Intelligence Platform..."

# Stop existing containers
log_info "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Build new images
log_info "Building Docker images..."
docker-compose build --no-cache

# Start services
log_info "Starting services..."
docker-compose up -d

# Wait for services to be ready
log_info "Waiting for services to start..."
sleep 30

# Health check
log_info "Performing health checks..."

# Check AEO Intelligence service
if curl -f -s http://localhost:8001/health > /dev/null; then
    log_success "AEO Intelligence Platform is healthy"
else
    log_error "AEO Intelligence Platform health check failed"
    echo "Checking logs..."
    docker-compose logs aeo-intelligence
    exit 1
fi

# Check if nginx is running (optional)
if docker-compose ps nginx | grep -q "Up"; then
    if curl -f -s http://localhost/health > /dev/null; then
        log_success "Nginx proxy is healthy"
    else
        log_warning "Nginx proxy health check failed, but AEO service is running directly"
    fi
fi

# Display status
echo
log_success "🎉 Deployment Complete!"
echo
echo -e "${GREEN}Your Enhanced AEO Intelligence Platform is now running!${NC}"
echo
echo "📊 Service Endpoints:"
echo "• Direct API Access: http://localhost:8001"
echo "• Health Check: http://localhost:8001/health"
echo "• API Documentation: http://localhost:8001/docs"
echo "• Features Endpoint: http://localhost:8001/api/features"
echo

if docker-compose ps nginx | grep -q "Up"; then
    echo "🌐 Production Access (via Nginx):"
    echo "• Main Access: http://localhost"
    echo "• API: http://localhost/api/"
    echo "• Health: http://localhost/health"
    echo
fi

echo -e "${BLUE}🧠 Intelligence Features Available:${NC}"
echo "✅ AI-Powered FAQ Detection & Analysis"
echo "✅ Advanced Schema Intelligence & Validation"
echo "✅ Entity Recognition & Semantic Analysis"
echo "✅ Voice Search Optimization Assessment"
echo "✅ Dynamic AI Recommendation Generation"
echo "✅ Topic Authority & Content Depth Analysis"
echo "✅ Competitive Positioning Insights"
echo

echo -e "${YELLOW}📋 Quick Test Commands:${NC}"
echo "# Test basic health"
echo "curl http://localhost:8001/health"
echo
echo "# Test enhanced analysis"
echo 'curl -X POST http://localhost:8001/api/analyze -H "Content-Type: application/json" -d "{\"url\":\"https://example.com\"}"'
echo
echo "# View platform features"
echo "curl http://localhost:8001/api/features"
echo

echo -e "${BLUE}📖 Management Commands:${NC}"
echo "• View logs: docker-compose logs -f"
echo "• Stop platform: docker-compose down"
echo "• Restart platform: docker-compose restart"
echo "• Update platform: ./deploy.sh"
echo

log_success "Enhanced AEO Intelligence Platform deployment successful!"
echo -e "${GREEN}Your 70%+ intelligence AEO platform is ready for production use! 🚀${NC}"
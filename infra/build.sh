#!/bin/bash

set -e

echo "📦 Building production images..."

# Build backend
echo "🔨 Building backend..."
docker build -t aap-backend:latest ./backend
docker tag aap-backend:latest aap-backend:$(date +%Y%m%d_%H%M%S)

# Build frontend
echo "🎨 Building frontend..."
docker build -t aap-frontend:latest ./frontend
docker tag aap-frontend:latest aap-frontend:$(date +%Y%m%d_%H%M%S)

# Build all services
echo "🐳 Building full stack..."
docker-compose -f docker-compose.prod.yml build

echo "✅ Build complete!"
echo ""
echo "Images ready for deployment:"
docker images | grep aap

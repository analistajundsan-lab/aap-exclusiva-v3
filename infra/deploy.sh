#!/bin/bash

set -e

echo "🚀 Deploying AAP Exclusiva to Kubernetes..."

NAMESPACE="production"
ENVIRONMENT=${1:-staging}

# Create namespace
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Apply configurations
echo "📋 Applying configurations..."
kubectl apply -f infra/k8s/config.yaml

# Apply database
echo "🗄️ Deploying PostgreSQL..."
kubectl apply -f infra/k8s/postgres.yaml
kubectl wait --for=condition=ready pod -l app=postgres -n $NAMESPACE --timeout=300s

# Apply backend
echo "🔧 Deploying backend..."
kubectl apply -f infra/k8s/backend.yaml

# Apply frontend
echo "🎨 Deploying frontend..."
kubectl apply -f infra/k8s/frontend.yaml

# Apply scaling
echo "📈 Configuring autoscaling..."
kubectl apply -f infra/k8s/hpa.yaml

# Apply network policies
echo "🔒 Applying network policies..."
kubectl apply -f infra/k8s/network-policy.yaml

# Apply backup jobs
echo "💾 Configuring backups..."
kubectl apply -f infra/k8s/backup.yaml

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Monitoring:"
kubectl get svc -n $NAMESPACE
kubectl get pods -n $NAMESPACE
echo ""
echo "🌐 Access your application:"
echo "   Backend:  http://$(kubectl get svc aap-backend -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"
echo "   Frontend: http://$(kubectl get svc aap-frontend -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"

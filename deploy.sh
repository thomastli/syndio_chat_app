#!/bin/bash

# Start Minikube
minikube start

# Enable the ingress addon for external access
minikube addons enable ingress

eval $(minikube docker-env)

# Build the Docker image in Minikube's environment
docker build -t chat-app:latest .

# Create secret for OpenAI API key
# Replace YOUR_API_KEY with your actual OpenAI API key
kubectl create secret generic chat-app-secrets \
  --from-literal=openai-api-key="YOUR_API_KEY"

# Apply Kubernetes manifests
kubectl apply -f k8s/configmap.ymal
kubectl apply -f k8s/app_deployment.yaml
kubectl apply -f k8s/app_service.yaml
kubectl apply -f k8s/mongodb_deployment.yaml
kubectl apply -f k8s/mongodb_service.yaml
kubectl apply -f k8s/hpa.yaml

# Display pod status
echo "Pod Status:"
kubectl get pods

# Display service status
echo "Service Status:"
kubectl get services

# Display HPA status
echo "HPA Status:"
kubectl get hpa

# Get the URL to access the application
minikube service chat-app-service --url
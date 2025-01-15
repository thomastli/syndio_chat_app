#!/bin/bash

# Start Minikube
minikube start

# Enable the ingress addon for external access
minikube addons enable ingress

eval $(minikube docker-env)

# Build the Docker image in Minikube's environment
docker build -t chat-app:latest .

# Create secrets from environment variable
kubectl create secret generic chat-app-secrets --from-env-file=.env

# Apply Kubernetes manifests
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/app-service.yaml
kubectl apply -f k8s/mongodb-deployment.yaml
kubectl apply -f k8s/mongodb-service.yaml
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

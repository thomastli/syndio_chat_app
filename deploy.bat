@echo off
SETLOCAL EnableDelayedExpansion

:: Start Minikube
echo Starting Minikube...
minikube start

:: Enable the ingress addon for external access
echo Enabling ingress addon...
minikube addons enable ingress

:: Set Docker environment variables for Minikube
echo Setting Docker environment...
FOR /F "tokens=*" %%i IN ('minikube docker-env') DO @%%i

:: Build the Docker image in Minikube's environment
echo Building Docker image...
docker build -t chat-app:latest .

:: Create secret for OpenAI API key
:: Replace YOUR_API_KEY with your actual OpenAI API key
echo Creating Kubernetes secret...
kubectl create secret generic chat-app-secrets --from-literal=openai-api-key="YOUR_API_KEY"

:: Apply Kubernetes manifests
echo Applying Kubernetes manifests...
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/app_deployment.yaml
kubectl apply -f k8s/app_service.yaml
kubectl apply -f k8s/mongodb_deployment.yaml
kubectl apply -f k8s/mongodb_service.yaml
kubectl apply -f k8s/hpa.yaml

:: Display pod status
echo:
echo Pod Status:
kubectl get pods

:: Display service status
echo:
echo Service Status:
kubectl get services

:: Display HPA status
echo:
echo HPA Status:
kubectl get hpa

:: Get the URL to access the application
echo Getting service URL...
minikube service chat-app-service --url

ENDLOCAL
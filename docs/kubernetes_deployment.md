# Kubernetes Deployment

The following defines the Kubernetes manifests and a sample deployment script for a `MiniKube` instance.

## Manifests
The `k8s` directory contains the following manifests:
```
.
├── k8s
│   ├── app_deployment.yaml
│   ├── app_service.yaml
│   ├── configmap.yaml
│   ├── hpa.yaml
│   ├── mongodb_deployment.yaml
│   └── mongodb_service.yaml 
├── 
```

### ConfigMap
The `configmap.yaml` manifest stores runtime configuration variables for the Syndio chat application:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: chat-app-config
data:
  MAX_MESSAGES: "100"
  DEBUG: "False"
```

This configuration sets two application parameters:
- **Maximum number of messages allowed:** `100`
- **Debug mode:** `Disabled`

### App Deployment
The `app_deployment.yaml` manifest defines how the application should be deployed and managed within the cluster:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-app
spec:
  replicas: 1 # Reduced for Minikube environment
  selector:
    matchLabels:
      app: chat-app
  template:
    metadata:
      labels:
        app: chat-app
    spec:
      containers:
      - name: chat-app
        image: chat-app:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 5000
        env:
          - name: MONGO_URI
            value: "mongodb://mongodb:27017/chat_app"
        resources:
          requests:
            memory: "64Mi"   # Reduced for Minikube
            cpu: "100m"
          limits:
            memory: "128Mi"  # Reduced for Minikube
            cpu: "200m"
```

Specifications:
- Maintains `1` replica of the application
- Uses locally built image (`chat-app:latest`)
- Exposes port `5000`
- Labels pods with `app: chat-app` for service discovery

### App Service
The `app_service.yaml` Service manifest defines how the application is exposed to the network:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: chat-app-service
spec:
  type: NodePort
  selector:
    app: chat-app
  ports:
  - port: 5000
    targetPort: 5000
```

Configuration:
- Type: `NodePort` for Minikube compatibility
- Selects pods labeled with `app: chat-app`
- Maps `service port: 5000` to `container port: 5000`


### Horizontal Pod Autoscaler (HPA)
The `hpa.yaml` manifest configures automatic scaling based on resource utilization:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: chat-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: chat-app
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

Autoscaling configuration:
- Scales between `1` and `5` replicas
- Triggers scaling when CPU utilization exceeds `70%`
- Targets the `chat-app` deployment

## MongoDB Deployment
The `mongodb_deployment.yaml` manifest configures a MongoDB instance:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongodb
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
      - name: mongodb
        image: mongo:8
        ports:
        - containerPort: 27017
```

Specifications:
- Uses MongoDB version 8
- Runs a single replica of MongoDB (replicas: 1)
- Labels the pod with `app: mongodb` for service discovery
- Exposes port `27017` (MongoDB's default port)
- Doesn't specify any resource limits or persistent storage

## MongoDB Service 
The `mongodb_service.yaml` manifest defines how the MongoDB deployment:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb
spec:
  selector:
    app: mongodb
  ports:
  - port: 27017
    targetPort: 27017
  type: ClusterIP
```

Specifications: 
- Creates a Service named `mongo`
- Maps port `27017` to the same port on all the pods
- Uses selector `app: mongodb` to match the pods created by the deployment
- Creates a `ClusterIP` type service

Notes:
- The Service and Deployment are linked via the `app: mongo` label
- Being a `ClusterIP` service, MongoDB will only be accessible within the cluster
- There's no persistent storage configured, so data will be lost if the pod restarts
- No security configurations are specified (like authentication or network policies)

## Deployment Script

The deployment script (`sample_deploy.sh`/`sample_deploy.bat`) automates the entire deployment process:

1. Environment Setup:
   - Starts `Minikube` cluster
   - Enables `ingress` addon
   - Configures `docker` to use Minikube's Docker daemon
2. Application Build:
   - Builds the Docker image within Minikube's environment
3. Secrets Management:
   - Creates a Kubernetes secret for the OpenAI API key
4. Resource Deployment:
   - Applies all Kubernetes manifests in sequence:
     - ConfigMap
     - App Deployment
     - App Service
     - MongoDB Deployment
     - MongoDB Service
     - HPA
5. Status Verification:
   - Displays status of:
     - Pods
     - Services
     - Horizontal Pod Autoscaler
   - Retrieves application URL

## Notes
- This deployment is optimized for local development in Minikube
- Resource limits are intentionally low to accommodate Minikube's constraints
- The application relies on OpenAI's API, requiring a valid API key
- Local image building is used instead of pulling from a registry
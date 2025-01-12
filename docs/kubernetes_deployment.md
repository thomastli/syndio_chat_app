# Kubernetes Deployment

The following defines the Kubernetes manifests and a sample deployment script for a `MiniKube` instance.

## Manifests
The `k8s` directory contains the following manifests:
```
.
├── k8s
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── hpa.yaml
│   └── service.yaml
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

### Deployment
The `deployment.yaml` manifest defines how the application should be deployed and managed within the cluster:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-app
spec:
  replicas: 2
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
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

Specifications:
- Maintains `2` replicas of the application
- Uses locally built image (`chat-app:latest`)
- Exposes port `5000`
- Labels pods with `app: chat-app` for service discovery

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

### Service
The `service.yaml` Service manifest defines how the application is exposed to the network:

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

Service configuration:
- Type: `NodePort` for Minikube compatibility
- Selects pods labeled with `app: chat-app`
- Maps `service port: 5000` to `container port: 5000`

## Deployment Script

`deploy.sh` automates the entire deployment process:

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
     - Deployment
     - Service
     - HPA
5. Status Verification:
   - Retrieves application URL
   - Displays status of:
     - Pods
     - Services
     - Horizontal Pod Autoscaler

## Notes
- This deployment is optimized for local development in Minikube
- Resource limits are intentionally low to accommodate Minikube's constraints
- The application relies on OpenAI's API, requiring a valid API key
- Local image building is used instead of pulling from a registry
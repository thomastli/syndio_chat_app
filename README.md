# syndio_chat_app

[![codecov](https://codecov.io/gh/thomastli/syndio_chat_app/graph/badge.svg?token=BbIsm1rnoz)](https://codecov.io/gh/thomastli/syndio_chat_app) [![CodeFactor](https://www.codefactor.io/repository/github/thomastli/syndio_chat_app/badge)](https://www.codefactor.io/repository/github/thomastli/syndio_chat_app)

Simple Flask-based, real-time chat app that uses an AI model to return responses to the user.

## Usage

Create an `.env` file to set the following environment variables:

```bash
APP_HOST=127.0.0.1 # Optional, uses default value in constants.py otherwise
APP_PORT=5000 # Optional, uses default value in constants.py otherwise
MONGO_URI=mongodb://mongodb:27017/chat_app # Required 
OPENAI_API_KEY=your-openai-api-key # Required
```

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

Build and start the application via `docker compose`:

```bash
docker compose build
docker compose up -d
```

## API Contract

See [API Contract](docs/api_contract.md)

## Kubernetes Deployment

See [Kubernetes Deployment Plan](docs/kubernetes_deployment.md)

## Checklist

### Main Requirements

- [X] Python Flask application with the following endpoints:
    - [X] Serves the frontend (`GET /`)
    - [X] Sends chat messages (`POST /chat/message`)
    - [X] Retrieves chat history (`GET /chat/history`)
- [X] Implement generative AI/LLM integration:
    - [X] Create a dummy function that simulates AI assistant responses
    - [X] Describe how you would replace dummy responses with a real LLM model in production
- [X] Add basic logging (for user messages, error, etc.)
    - [X] Describe how you would implement tools like Splunk or Datadog in comments or placeholder functions
- [X] Implement a docker build and Kubernetes deployment:
    - [X] Include Dockerfile to build/run your app
    - [X] Describe a Kubernetes deployment plan for the app
- [X] Include basic unit and integration tests
- [X] Add GitHUb Actions workflow for CI/CD (linting, testing, and building applications)
- [X] Write an API contract for the chat app including the following:
    - [X] API Endpoints
    - [X] HTTP Methods used by each endpoint
    - [X] Request body examples (in JSON)
    - [X] HTTP Response Codes
    - [X] Response body examples (in JSON)

### Optional

- [X] Integrate either a local SQL or NoSQL database for chat history
    - [X] Implement a local MongoDB database using `flask-pymongo`
    - [X] Create a Docker Compose `yaml` configuration to define multiple containers for the Flask app and MongoDB
      instance
    - [X] Update GitHub Actions build stage to use `docker compose` instead of `docker build`
    - [X] Update Kubernetes deployment plan to include deployment and services manifests for the MongoDB instance
- [ ] Extend the provided frontend or create a React/Vue component for the REST API.

## Future Improvements

The following include some possible future improvements that were either outside the scope of the original spec or not
feasible for the deliverable timeframe:

### AI Integration / Performance

- Implement the [Circuit Breaker pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)
  for the AI response requests to help prevent cascading failures and more efficiently manage API calls to AI services.
- Add wrappers for other pretrained AI models (i.e. `Claude 3.5`, `Gemini`, etc.).
- Evaluate training a custom model via `PyTorch` or `TensorFlow` for AI responses.

### Database

- Since the original requirements specified an in-memory messages store, the MongoDB implementation does not persist its
  data when `docker compose`/`minikube` goes down:
    - We can add a [persistent volume data store](https://docs.docker.com/reference/compose-file/volumes/) in our
      `compose.yaml` if we wanted chat history to persist.
    - Similarly, we can add a [persistent volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
      manifest for our Kubernetes deployment.
- Implement [authentication](https://www.mongodb.com/docs/manual/core/authentication/) for the MongoDB instance (i.e.
  `Kerberos`, `OAuth2`, etc.)
- Implement [Role-Based Access Control](https://www.mongodb.com/docs/manual/reference/built-in-roles/) in MongoDB.

### Deployment

- Deploy the application on a cloud-hosted Kubernetes cluster service (i.e. `Google Kubernetes Engine (GKE)`,
  `Amazon Elastic Kubernetes Service (EKS`, or `Azure Kubernetes Service (AKS)`) instead of locally.
- Use an external secrets manager (i.e. `Google Secret Manager`, `AWS Secrets Manager`, `Azure Key Vault`).

### Flask

- Enforce HTTPS via [flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman)
- Consider implement authorization and authentication:
    - Role-based access control via [Flask-RBAC](https://flask-rbac.readthedocs.io/en/latest/)
    - Authentication via
      either [Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/?ref=escape.tech) (basic) or
      using [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/?ref=escape.tech) (more advanced)
- Implement rate limiting with [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/?ref=escape.tech)

### Input Validation / Sanitization

- Considering defining a more robust
  `Mozilla Bleach` [cleaner](https://bleach.readthedocs.io/en/latest/clean.html#using-bleach-sanitizer-cleaner) instance
  to sanitize user messages.

### Monitoring
- Deploy a [Splunk Operator](https://splunk.github.io/splunk-operator/) instance as part of the Kubernetes deployment.
- Replace basic logging with commented Splunk logs in the Flask application.

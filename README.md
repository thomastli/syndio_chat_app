# syndio_assignment

[![codecov](https://codecov.io/gh/thomastli/syndio_assignment/graph/badge.svg?token=BbIsm1rnoz)](https://codecov.io/gh/thomastli/syndio_assignment)

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

Run the Flask application:
```bash
flask --app flask-chat-app run
```

Or using Docker:
```bash
docker build -t chat-app .
docker run -p 5000:5000 chat-app
```

## API Contract
See [API Contract](docs/api_contract.md)

## Kubernetes Deployment
See [Kubernetes Deployment Plan](docs/kubernetes_deployment.md)

## Checklist
### Main Requirements
- [X] Python Flask application with the following endpoints:
  - [X] Serving the frontend (`GET /`)
  - [X] Sending chat messages (`POST /chat/message`)
  - [X] Retrieving chat history (`GET /chat/history`)
- [X] Implement generative AI/LLM integration: 
  - [X] Create a dummy function that simulates AI assistant responses
  - [X] Describe how you would replace dummy responses with a real LLM model in production
- [X] Add basic logging (for user messages, error, etc.)
  - [X] Describe how you would implement tools like Splunk or Datadog in comments or placeholder functions
- [X] Implement a docker build and Kubernetes deployment:
  - [X] Include Dockerfile to build/run your app
  - [X] Description of how to deploy the app to a Kubernetes cluster
- [X] Include basic unit and integration tests
- [X] Add GitHUb Actions workflow for CI/CD (linting, testing, and building applications)
- [X] Write an API contract for the chat app including the following:
  - [X] API Endpoints
  - [X] HTTP Methods used by each endpoint
  - [X] Sample request bodies (in JSON)
  - [X] HTTP Response Codes 
  - [X] Sample response bodies (in JSON)

### Optional
- [ ] Integrate either a local SQL or NoSQL database for chat history
- [ ] Extend the provided frontend or create a React/Vue component for the REST API.

# syndio_assignment

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
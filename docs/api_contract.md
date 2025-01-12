# Syndio Chat API Contract

## Endpoints

### 1. Home Page
**Endpoint:** `/`  
**HTTP Method:** `GET`  
**Description:** Serves the chat interface HTML page

**Response Codes:**
- `200`: Success - Returns the HTML page
- `500`: Internal Server Error

**Error Response Body:**
```json
{
    "error": "Internal server error"
}
```

### 2. Send Message
**Endpoint:** `/chat/message`  
**HTTP Method:** `POST`  
**Description:** Handles incoming chat messages and returns AI responses

#### Response Codes
- `200`: Success
- `400`: Bad Request (Invalid format or empty message)
- `500`: Internal Server Error

#### Request Body
```json
{
    "message": "Hello, how are you today?"
}
```

#### Success Response Body (Example)
```json
{
    "status": "success"
}
```

#### Bad Request Response Body (Examples)
##### Empty Message Request Body
```json
{
    "error": "Message cannot be empty"
}
```

#### Server Error
```json
{
    "error": "Internal server error"
}
```

#### Internal Server Error Response Body (Example)
```json
{
    "error": "Invalid request format"
}
```

### 3. Get Chat History
**Endpoint:** `/chat/history`  
**HTTP Method:** `GET`  
**Description:** Retrieves the chat conversation history

#### Response Codes
- `200`: Success
- `500`: Internal Server Error

#### Success Response Body (Example)
```json
[
    {
        "user": "User",
        "message": "Hello, how are you today?",
        "timestamp": "2025-01-12T14:30:00.123456"
    },
    {
        "user": "AI",
        "message": "Hi there! I'm a simulated AI assistant.",
        "timestamp": "2025-01-12T14:30:01.234567"
    },
    {
        "user": "User",
        "message": "What's the weather like?",
        "timestamp": "2025-01-12T14:30:15.345678"
    },
    {
        "user": "AI",
        "message": "I understand what you're saying. Please tell me more!",
        "timestamp": "2025-01-12T14:30:16.456789"
    }
]
```

#### Error Response Body
```json
{
    "error": "Error retrieving chat history"
}
```

## Notes
1. The application maintains a configurable message limit (default: 100 messages)
2. All timestamps are in ISO format with microsecond precision
3. Empty messages are not accepted
4. The API uses JSON for all request and response bodies
5. All error responses follow the same structure with an "error" field containing the error message
6. The AI responses are currently limited to a predefined set of dummy responses in development, but in production would use the GPT-4o Mini model
7. The User field in messages will always be either "User" or "AI"

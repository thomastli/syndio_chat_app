# Syndio Chat API Contract

## Endpoints

### 1. Retrieve Home Page
**Endpoint:** `/`  
**HTTP Method:** `GET`  
**Description:** Serves the chat interface HTML page

**Response Codes:**
- `200`: Success - Returns the HTML page
- `500`: Internal Server Error

#### Error Response Body Example
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

#### Request Body Example
```json
{
    "message": "Hello, how are you today?"
}
```

#### Success Response Body Example
```json
{
    "status": "success"
}
```

#### Bad Request Response Body Examples
##### Empty Message Request Body
```json
{
    "error": "Message cannot be empty"
}
```
##### Invalid Request Format Response Body Example
```json
{
    "error": "Invalid request format"
}
```

##### Internal Server Error Response Body Example
```json
{
    "error": "Internal server error"
}
```

### 3. Get Chat History
**Endpoint:** `/chat/history`  
**HTTP Method:** `GET`  
**Description:** Retrieves the chat history

#### Response Codes
- `200`: Success
- `500`: Internal Server Error

#### Success Response Body Example
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

#### Error Response Body Example
```json
{
    "error": "Error retrieving chat history"
}
```
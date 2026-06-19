# How APIs Work

## The Request-Response Cycle

Every API interaction follows a request-response cycle. Here is what happens step by step when you call an API:

1. **Client makes a request**: The client (browser, mobile app, Python script) constructs an HTTP request containing a method (GET, POST, etc.), a URL (the endpoint), headers (metadata like content type, authentication tokens), and optionally a body (data for POST/PUT requests).
2. **DNS resolution**: If the URL contains a domain name (e.g., `api.example.com`), the client's DNS resolver translates it to an IP address.
3. **TCP connection**: The client establishes a TCP connection with the server at the resolved IP address. In HTTPS, a TLS handshake follows to establish an encrypted connection.
4. **Server receives the request**: The web server (Nginx, Apache, or the ASGI server directly) receives the HTTP request and forwards it to the application (FastAPI).
5. **Request processing**: FastAPI parses the request, validates the input data using Pydantic models, extracts path/query parameters, and routes the request to the appropriate handler function.
6. **Business logic**: The handler function executes the business logic — querying a database, running an ML model inference, or processing data.
7. **Response construction**: The handler returns data (typically a dictionary or Pydantic model), which FastAPI serializes to JSON and packages into an HTTP response with the appropriate status code and headers.
8. **Client receives the response**: The client receives the JSON response and processes it — displaying data to the user, storing results, or triggering further actions.

```text
  Client         DNS          Uvicorn         FastAPI       ML Model / DB
    |             |               |               |               |
    +--resolve--->|               |               |               |
    |<----IP------+               |               |               |
    |             |               |               |               |
    +--------TCP + TLS handshake->|               |               |
    |<-------connection ready-----+               |               |
    |             |               |               |               |
    +--------POST /predict {"features":[...]}---->|               |
    |             |               +---ASGI scope->|               |
    |             |               |               +---validate--->|
    |             |               |               |<--result------+
    |             |               |               +---inference-->|
    |             |               |               |<--output------+
    |             |               +<--JSON 200----+               |
    |<-------HTTP Response--------+               |               |
```

## Anatomy of an API Request

```
POST /predict HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...

{
  "image_url": "https://example.com/cat.jpg",
  "model": "resnet50"
}
```

## Anatomy of an API Response

```
HTTP/1.1 200 OK
Content-Type: application/json
X-Response-Time: 45ms

{
  "prediction": "Persian cat",
  "confidence": 0.92,
  "model_version": "resnet50-v1"
}
```

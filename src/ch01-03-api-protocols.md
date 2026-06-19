# API Protocols

## HTTP/HTTPS

HTTP (Hypertext Transfer Protocol) is the foundational protocol for web-based APIs. It defines how messages are formatted and transmitted between clients and servers. HTTPS adds a layer of TLS/SSL encryption on top of HTTP, ensuring that all communication between the client and server is encrypted and cannot be intercepted by third parties. In production, every API should use HTTPS to protect sensitive data in transit. FastAPI applications are typically served behind a reverse proxy (like Nginx) that handles TLS termination and forwards requests to the FastAPI application over HTTP.

## HTTP Methods

RESTful APIs use standard HTTP methods to indicate the type of operation being performed:

| Method | Purpose | Example |
|--------|---------|---------|
| **GET** | Retrieve data | `GET /items/` — Get all items |
| **POST** | Create new data | `POST /items/` — Create a new item |
| **PUT** | Update entire resource | `PUT /items/1` — Replace item 1 |
| **DELETE** | Remove data | `DELETE /items/1` — Delete item 1 |
| **PATCH** | Partial update | `PATCH /items/1` — Update item 1 partially |

## JSON (JavaScript Object Notation)

JSON has become the de facto standard data format for REST APIs. It is a lightweight, human-readable format that represents data as key-value pairs and arrays. The key advantage of JSON is that it is **language-agnostic** — the same JSON data can be parsed by Python, JavaScript, Java, PHP, Go, or any other programming language. This makes JSON the perfect format for APIs that need to serve clients written in different languages. When you build a FastAPI endpoint that returns a dictionary or a Pydantic model, FastAPI automatically serializes it to JSON behind the scenes.

```json
{
  "prediction": "cat",
  "confidence": 0.95,
  "model_version": "1.0"
}
```

## Status Codes

HTTP status codes communicate the result of an API request. Understanding these codes is essential for both building and consuming APIs:

- **2xx Success**: `200 OK` (successful GET/PUT), `201 Created` (successful POST), `204 No Content` (successful DELETE)
- **3xx Redirection**: `301 Moved Permanently`, `304 Not Modified`
- **4xx Client Errors**: `400 Bad Request` (malformed input), `401 Unauthorized` (missing/invalid auth), `403 Forbidden` (insufficient permissions), `404 Not Found`, `422 Unprocessable Entity` (validation failure)
- **5xx Server Errors**: `500 Internal Server Error`, `503 Service Unavailable`

FastAPI automatically returns appropriate status codes in many cases, and you can also set them explicitly for each endpoint.

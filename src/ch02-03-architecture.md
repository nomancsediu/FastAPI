# Architecture of FastAPI

## ASGI (Asynchronous Server Gateway Interface)

FastAPI is built on the ASGI specification, which is the asynchronous counterpart to WSGI (Web Server Gateway Interface). ASGI allows Python web applications to handle asynchronous operations natively, supporting WebSockets, HTTP/2, and long-polling in addition to standard HTTP requests. FastAPI uses Uvicorn (or Hypercorn) as the ASGI server, which manages the event loop and handles the low-level details of receiving HTTP requests and sending responses.

## The Request Processing Pipeline

When a request arrives at a FastAPI application, it goes through several stages:

```text
  +------------------+     +------------------+     +------------------+
  |  Incoming HTTP   +---->+  Uvicorn (ASGI)  +---->+ Starlette Router |
  |  Request         |     |  Server          |     |                  |
  +------------------+     +------------------+     +--------+---------+
                                                              |
                                                              v
                                                    +--------+---------+
                                                    |  FastAPI         |
                                                    |  Validation      |
                                                    |  (Pydantic)      |
                                                    +--------+---------+
                                                              |
                                                              v
                                                    +--------+---------+
                                                    |  Dependencies    |
                                                    |  Resolution      |
                                                    |  (Depends)       |
                                                    +--------+---------+
                                                              |
                                                              v
                                                    +--------+---------+
                                                    |  Endpoint        |
                                                    |  Handler         |
                                                    +--------+---------+
                                                              |
                                                              v
                                                    +--------+---------+
                                                    |  Response        |
                                                    |  Serialization   |
                                                    +--------+---------+
                                                              |
                                                              v
                                                    +--------+---------+
                                                    |  HTTP Response   |
                                                    |  to Client       |
                                                    +------------------+
```

1. **ASGI Server** (Uvicorn) receives the raw HTTP request and converts it into a Python ASGI scope.
2. **Starlette** (the underlying framework) routes the request to the appropriate endpoint based on the URL path and HTTP method.
3. **FastAPI** processes path parameters, query parameters, request headers, and request body, validating them against the defined type hints and Pydantic models.
4. **Dependencies** are resolved — any `Depends()` parameters in the endpoint function are executed.
5. **Endpoint function** is called with the validated and processed parameters.
6. **Response** is constructed — the return value is serialized (if needed) and wrapped in an HTTP response with the appropriate status code and headers.

## Pydantic Integration

Pydantic is the data validation library that powers FastAPI's request/response handling. When you define a Pydantic model (a class inheriting from `BaseModel`), Pydantic automatically validates data against the model's field types and constraints. If validation fails, it raises a `ValidationError` with detailed information about which fields failed and why. FastAPI catches these errors and converts them into user-friendly HTTP 422 responses. Pydantic also handles serialization (converting Python objects to JSON) and deserialization (parsing JSON into Python objects) seamlessly.

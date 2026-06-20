# Key Features of FastAPI

## Automatic Documentation (Swagger UI & ReDoc)

One of FastAPI's most powerful features is its automatic generation of interactive API documentation. When you define endpoints with type hints and Pydantic models, FastAPI automatically generates OpenAPI specification and provides two documentation UIs: Swagger UI (at `/docs`) and ReDoc (at `/redoc`). These are not static documentation pages — they are fully interactive. You can explore all endpoints, see the expected request/response schemas, and even send test requests directly from the documentation interface. For ML APIs, this means that your data science team can test model predictions without writing a single line of client code.

## Type Hints and Automatic Validation

FastAPI leverages Python's type hints to provide automatic request validation. When you define a function parameter with a type hint (like `age: int` or `name: str`), FastAPI automatically validates incoming request data against these types. If validation fails, FastAPI returns a clear, descriptive error message with the HTTP status code 422 (Unprocessable Entity). For ML APIs, this is extremely valuable — you can define exactly what format the model expects (image dimensions, tensor shapes, feature types) and let FastAPI handle all the validation automatically.

## Asynchronous Support

FastAPI has first-class support for Python's `async` and `await` keywords, allowing you to define asynchronous endpoint handlers. This is particularly important for ML APIs because model inference often involves I/O operations (reading files, making database queries, calling external services) that can benefit from non-blocking execution. With async support, a single FastAPI server can handle many concurrent requests efficiently, even when some requests are waiting for slow operations to complete.

## Dependency Injection

FastAPI's dependency injection system allows you to define reusable components (like database connections, authentication checks, configuration values) and inject them into your endpoint functions. This promotes code reuse, makes testing easier (you can easily substitute mock dependencies), and keeps your endpoint functions clean and focused on their core logic. We will explore dependency injection in depth in Chapter 3.

## High Performance

FastAPI is one of the fastest Python web frameworks available, with performance comparable to NodeJS and Go frameworks. This is achieved through Starlette's ASGI implementation, which handles HTTP requests asynchronously, and Pydantic's Rust-based core, which performs validation and serialization extremely quickly. Benchmarks consistently show FastAPI outperforming Flask and Django for API workloads.

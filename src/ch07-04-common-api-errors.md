# Common API Errors

## 422 Unprocessable Entity

This is the most common error in FastAPI APIs. It occurs when the request data fails Pydantic validation. Common causes include missing required fields, incorrect data types (sending a string where a number is expected), values outside the allowed range, and incorrect array lengths. FastAPI automatically returns detailed error messages that identify which fields failed and why, making it easy for clients to fix their requests.

## 500 Internal Server Error

This indicates an unhandled exception in your code. Common causes in ML APIs include model not loaded (forgotten to load at startup), NumPy shape mismatch (input does not match expected dimensions), file not found (model file path incorrect), and database connection failure. Always implement proper error handling and logging to diagnose 500 errors quickly.

## 401 Unauthorized / 403 Forbidden

These errors occur when authentication or authorization fails. 401 means the client has not provided valid credentials (missing or invalid token/API key). 403 means the client is authenticated but does not have permission to access the requested resource. Common causes include expired JWT tokens, incorrect API keys, and insufficient user permissions.

## 429 Too Many Requests

This occurs when the client exceeds the rate limit. Implement rate limiting to protect your API from abuse and ensure fair resource allocation. Return a `Retry-After` header to tell the client when they can retry.

```text
  +--------------------+--------------------+--------------------+--------------------+
  |  422 Unprocessable |  500 Internal      |  401 / 403         |  429 Too Many      |
  |  Entity            |  Server Error      |  Auth Failure      |  Requests          |
  +--------------------+--------------------+--------------------+--------------------+
  | Pydantic           | Model not loaded   | 401: missing /     | Rate limit         |
  | validation failed  | Shape mismatch     | invalid token      | exceeded           |
  | Missing fields     | File not found     | 403: authenticated | Too many requests  |
  | Wrong data types   | DB failure         | but no permission  | from same client   |
  | Out-of-range values| Unhandled except.  | Expired JWT        |                    |
  +--------------------+--------------------+--------------------+--------------------+
  | Fix: check request | Fix: logs +        | Fix: refresh token | Fix: back off and  |
  | body against schema| error handlers     | or use correct key | retry after delay  |
  +--------------------+--------------------+--------------------+--------------------+
```

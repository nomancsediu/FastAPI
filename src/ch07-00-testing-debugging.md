# Testing and Debugging

This chapter covers how to write tests for our `mlapi/` project — including the
model logic, the API endpoints, and the authentication we added in Chapter 6.

## What We'll Test

| What We Test | Tools |
|-------------|-------|
| Model prediction logic (direct function calls) | `pytest` |
| API endpoints (with `TestClient`) | `pytest`, `httpx` |
| Auth flow (API key, JWT register/login) | `pytest`, `TestClient` |
| Error handling (bad input, wrong auth) | `pytest` |

## Testing Philosophy

```
        ┌──────────────┐
        │   E2E Tests  │  Few — test the full system
        ├──────────────┤
        │  Integration │  Some — test endpoints end-to-end
        │    Tests     │
        ├──────────────┤
        │  Unit Tests  │  Many — test individual functions
        └──────────────┘
```

- **Unit tests**: Fast, isolated, test one function
- **Integration tests**: Use `TestClient` to test endpoints end-to-end
- **Auth tests**: Test with and without valid API keys / JWT tokens

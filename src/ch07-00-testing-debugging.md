# Testing and Debugging

This chapter covers how to write tests for both of our projects — `fastapi-crud/` and `ml-serving-api/` — and how to debug issues when they arise.

## What We'll Test

| Project | What We Test | Tools |
|---------|-------------|-------|
| **fastapi-crud/** | API endpoints, validation, auth, CRUD operations | `pytest`, `TestClient` |
| **ml-serving-api/** | Model prediction, batch processing, model mocking | `pytest`, `unittest.mock` |

## Testing Philosophy

```
        ┌──────────────┐
        │   E2E Tests  │  Few — test the full system
        ├──────────────┤
        │  Integration │  Some — test components together
        │    Tests     │
        ├──────────────┤
        │  Unit Tests  │  Many — test individual functions
        └──────────────┘
```

- **Unit tests**: Fast, isolated, test one function
- **Integration tests**: Use `TestClient` to test endpoints end-to-end
- **Mocked ML tests**: Replace real model with fake for deterministic results

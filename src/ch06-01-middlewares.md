# Middlewares

## What is Middleware?

Middleware is a function that runs before (and sometimes after) every HTTP request is processed by your endpoint handlers. Think of middleware as a series of filters or checkpoints through which every request must pass. Middleware can modify the request before it reaches the handler, modify the response before it is sent back to the client, perform logging and monitoring, enforce security policies, handle CORS (Cross-Origin Resource Sharing), and manage request-specific state.

## The Middleware Pipeline

```text
  +-------------+
  |   Request   |
  +------+------+
         |
         v
  +------+------+       +--------+
  | Middleware 1+------>+  CORS  |
  +------+------+       +--------+
         |
         v
  +------+------+       +--------+
  | Middleware 2+------>+ Timing |
  +------+------+       +--------+
         |
         v
  +------+------+       +------------+
  | Middleware 3+------>+ Rate Limit |
  +------+------+       +------------+
         |
         v
  +------+----------+
  | Endpoint Handler|
  +------+----------+
         |
         v
  +------+------+       +--------------+
  | Middleware 3+------>+ Post-process |
  +------+------+       +--------------+
         |
         v
  +------+------+       +--------------+
  | Middleware 2+------>+ Post-process |
  +------+------+       +--------------+
         |
         v
  +------+------+       +--------------+
  | Middleware 1+------>+ Post-process |
  +------+------+       +--------------+
         |
         v
  +------+------+
  |   Response  |
  +-------------+
```

When a request arrives, it passes through each middleware in the order they are registered. Each middleware can decide to pass the request to the next middleware (or the endpoint handler), return a response immediately (blocking the request), or modify the request/response as it passes through. After the endpoint handler produces a response, the response passes back through the middleware chain in reverse order.

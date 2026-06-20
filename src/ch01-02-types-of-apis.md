# Types of APIs

## REST APIs (Representational State Transfer)

REST is the most widely used API architectural style today. It uses standard HTTP methods (GET, POST, PUT, DELETE) to perform CRUD (Create, Read, Update, Delete) operations on resources, which are identified by URLs. REST APIs are stateless, meaning each request from the client contains all the information needed to process it — the server does not store session state between requests. REST typically uses JSON for request and response bodies, making it lightweight and easy to work with across different programming languages. Most public APIs you interact with (Google Maps, Twitter, GitHub) are REST APIs.

## SOAP APIs (Simple Object Access Protocol)

SOAP is a more rigid and formal protocol that uses XML exclusively for message formatting. Unlike REST, SOAP has strict standards and built-in error handling, making it suitable for enterprise applications where reliability and security are paramount. SOAP APIs support WS-Security for encryption and ACID-compliant transactions. While REST has become the dominant choice for new projects, SOAP is still widely used in banking, healthcare, and telecommunication systems where compliance with strict standards is required.

## GraphQL

GraphQL is a query language for APIs developed by Facebook. Unlike REST, where each endpoint returns a fixed data structure, GraphQL allows the client to specify exactly what data it needs in a single query. This eliminates the problems of over-fetching (getting more data than needed) and under-fetching (needing multiple requests to get all required data) that are common with REST. GraphQL uses a single endpoint and a type system to define the available data, giving clients fine-grained control over their queries.

## gRPC (Google Remote Procedure Call)

gRPC is a high-performance RPC framework developed by Google that uses Protocol Buffers (protobuf) as its interface definition language and data serialization format. Unlike REST/JSON, protobuf is a binary format that is significantly more compact and faster to serialize and deserialize. gRPC supports bidirectional streaming, making it ideal for real-time applications. It is heavily used in microservices architectures where inter-service communication performance is critical, particularly in polyglot environments where services may be written in different programming languages.

## WebSocket APIs

WebSocket APIs provide full-duplex communication channels over a single TCP connection. Unlike traditional HTTP requests where the client initiates each interaction, WebSocket allows both the client and the server to send messages to each other at any time. This makes WebSocket ideal for real-time applications like chat applications, live sports scores, stock market tickers, and collaborative editing tools. FastAPI has first-class support for WebSockets.

```text
  +---------------+---------------+---------------+---------------+---------------+
  |     REST      |     SOAP      |   GraphQL     |     gRPC      |   WebSocket   |
  +---------------+---------------+---------------+---------------+---------------+
  | HTTP + JSON   | XML + strict  | Single        | Protobuf      | Full-duplex   |
  | Stateless     | WS-Security   | endpoint      | Binary format | Persistent    |
  | CRUD ops      | ACID txns     | Client-driven | Bidirectional | connection    |
  +---------------+---------------+---------------+---------------+---------------+
  | Web & Mobile  | Banking       | Complex data  | Microservices | Chat / Live   |
  | Most popular  | Healthcare    | requirements  | High perf.    | Streaming     |
  +---------------+---------------+---------------+---------------+---------------+
```

# API Authentication & Authorization

## Authentication vs Authorization

**Authentication** is the process of verifying who the user is (identity verification). **Authorization** is the process of verifying what the user is allowed to do (permission verification). While often used together, they serve different purposes. A user might be authenticated (we know who they are) but not authorized to access a particular resource (they do not have the required permissions).

## API Keys

API keys are the simplest form of API authentication. The client includes a secret key in every request (typically in the `X-API-Key` header), and the server validates the key before processing the request. While simple to implement, API keys have limitations — they do not expire by default, they cannot carry user-specific information, and if leaked, anyone can use them until they are manually rotated.

## JWT (JSON Web Tokens)

JWT is a stateless authentication mechanism that is widely used in modern APIs. A JWT is a self-contained token that contains three parts: a header (specifying the algorithm), a payload (containing user data and claims), and a signature (ensuring the token has not been tampered with). The server signs the token with a secret key, and the client includes it in the `Authorization` header as a `Bearer` token on every request. Since the token is self-contained, the server does not need to store session data, making JWT inherently scalable. We will implement a complete JWT authentication system in Chapter 6.

```text
  Client              Server /login        User DB      Protected Endpoint
    |                       |                 |                |
    +---POST /login-------->|                 |                |
    |   username+password   +---verify------->|                |
    |                       |<--user found----+                |
    |                       +---create JWT (sign w/ SECRET)--->|
    |<--{access_token,------+                 |                |
    |    token_type}        |                 |                |
    |                                                          |
    +---GET /predict (Authorization: Bearer JWT)-------------->|
    |                                         +--verify sig--->|
    |                                         +--extract user->|
    |<--200 OK + data--------------------------------------------------+
```

## OAuth 2.0

OAuth 2.0 is an authorization framework that allows third-party applications to access a user's resources without sharing their credentials. It is the protocol behind "Sign in with Google/GitHub" buttons. OAuth 2.0 defines several grant types (Authorization Code, Client Credentials, etc.) for different use cases. For ML APIs, OAuth 2.0 is commonly used when the API needs to integrate with enterprise identity providers or when you need fine-grained permission management.

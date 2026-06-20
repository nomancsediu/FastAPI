# API Components

## Endpoints

An endpoint is a specific URL where an API receives requests. Each endpoint corresponds to a specific function or resource. For example, in a machine learning API, you might have endpoints like `/predict` for making predictions, `/train` for triggering model training, `/health` for checking system status, and `/models` for listing available models. Well-designed endpoints use nouns (resources) rather than verbs (actions) in the URL, with the HTTP method conveying the action. For example, `POST /predictions` is preferred over `POST /predict`, and `GET /models` is preferred over `GET /getModels`.

## Request Methods

As covered in the protocols section, HTTP methods (GET, POST, PUT, DELETE, PATCH) define the type of operation. RESTful API design maps these methods to CRUD operations: GET for Read, POST for Create, PUT/PATCH for Update, and DELETE for Delete.

## Headers

HTTP headers carry additional metadata about the request or response. Common request headers include `Content-Type` (specifying the format of the request body), `Authorization` (carrying authentication credentials), `Accept` (specifying the desired response format), and `User-Agent` (identifying the client). Common response headers include `Content-Type`, `X-Response-Time` (for performance monitoring), `Cache-Control` (for caching directives), and `RateLimit-Remaining` (for API rate limiting information).

## Request Body and Response Body

The request body carries data sent by the client (used with POST, PUT, PATCH methods), and the response body carries data returned by the server. Both are typically in JSON format. In FastAPI, you define the structure of these bodies using Pydantic models, which provide automatic validation, serialization, and documentation generation. For example, a prediction request body might require an `image_url` string and an optional `model` string, while the response body might include a `prediction` string and a `confidence` float.

## Authentication

APIs need authentication to control who can access them and what they can do. Common authentication methods include API keys (simple but less secure), JWT (JSON Web Tokens, stateless and scalable), OAuth 2.0 (delegated authorization, used by Google, GitHub, etc.), and HTTP Basic Auth (username/password, simple but not recommended for production). We will implement JWT authentication in Chapter 6.

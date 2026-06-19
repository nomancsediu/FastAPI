# Project Diagrams

---

## 1. Book Structure

```text
  FastAPI for Machine Learning
  |
  +-- Ch01: Introduction to APIs
  |     +-- What is an API
  |     +-- Types of APIs
  |     +-- API Protocols
  |     +-- How APIs Work
  |     +-- API Components
  |     +-- API Lifecycle
  |     +-- Auth & Authorization
  |
  +-- Ch02: Introduction to FastAPI
  |     +-- About FastAPI
  |     +-- Key Features
  |     +-- Architecture
  |     +-- Installing
  |     +-- First App
  |     +-- Comparative Analysis
  |
  +-- Ch03: Building APIs
  |     +-- Creating APIs
  |     +-- CRUD Operations
  |     +-- Validations & Errors
  |     +-- Async Programming
  |
  +-- Ch04: Database Integration
  |     +-- Database Basics
  |     +-- SQLAlchemy
  |     +-- CRUD Project Structure
  |
  +-- Ch05: ML Integration
  |     +-- Model Serialization
  |     +-- Pickle & Joblib
  |     +-- Keras Serialization
  |     +-- Pickle vs Joblib
  |     +-- Input/Output Schemas
  |     +-- Serving ML Models
  |     +-- Batch Predictions
  |
  +-- Ch06: Advanced FastAPI
  |     +-- Middlewares
  |     +-- Built-in Middlewares
  |     +-- Custom Middlewares
  |     +-- Dependency Injection
  |     +-- JWT Authentication
  |     +-- API Key Management
  |     +-- Best Practices
  |
  +-- Ch07: Testing & Debugging
        +-- Importance of Testing
        +-- Types of Tests
        +-- ML Model Mocking
        +-- Common API Errors
        +-- Debugging Techniques
```

---

## 2. Monolithic vs API Architecture

```text
   Monolithic Architecture          API Architecture
  +--------------------------+    +--------------------------------+
  |                          |    |                                |
  |  +----------+            |    |  +----------+                 |
  |  | Web Front+--> BL copy |    |  | Web Front+--+              |
  |  +----------+            |    |  +----------+  |              |
  |  +----------+            |    |  +----------+  |  +---------+ |
  |  |Mobile App+--> BL copy |    |  |Mobile App+--+--> API     | |
  |  +----------+            |    |  +----------+  |  | Layer   | |
  |  +----------+            |    |  +----------+  |  +----+----+ |
  |  | iOS App  +--> BL copy |    |  | iOS App  +--+       |      |
  |  +----------+            |    |  +----------+          v      |
  |       |   |   |          |    |                   +--------+  |
  |       v   v   v          |    |                   | Backend|  |
  |  +----------------+      |    |                   +----+---+  |
  |  | DB  DB  DB     |      |    |                        |      |
  |  | (duplicated x3)|      |    |                        v      |
  |  +----------------+      |    |                   +--------+  |
  |                          |    |                   | DB     |  |
  +--------------------------+    |                   |(single)|  |
                                  |                   +--------+  |
                                  +--------------------------------+
```

---

## 3. ML API — Clients to Model

```text
  +-------------+
  |   Web App   +--+
  +-------------+  |
  +-------------+  |    +------------------+    +-----------------+
  | Mobile App  +--+--->+  FastAPI ML API  +--->+ ML Model        |
  +-------------+  |    +--------+---------+    | Inference       |
  +-------------+  |             |              +--------+--------+
  |   Script    +--+             v                       |
  +-------------+       +--------+--------+              |
                         |   Database      |             |
                         +--------+--------+             |
                                  |                      |
                                  +----------+-----------+
                                             |
                                             v
                                  +----------+----------+
                                  |    JSON Response    |
                                  +---------------------+
```

---

## 4. API Types Comparison

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

---

## 5. HTTP Request-Response Cycle

```text
  Client         DNS          Uvicorn         FastAPI       ML Model / DB
    |             |               |               |               |
    +--resolve--->|               |               |               |
    |<----IP------+               |               |               |
    |             |               |               |               |
    +--------TCP + TLS handshake->|               |               |
    |<-------connection ready-----+               |               |
    |             |               |               |               |
    +--------POST /predict {"features":[...]}---->|               |
    |             |               +---ASGI scope->|               |
    |             |               |               +---validate--->|
    |             |               |               |<--result------+
    |             |               |               +---inference-->|
    |             |               |               |<--output------+
    |             |               +<--JSON 200----+               |
    |<-------HTTP Response--------+               |               |
```

---

## 6. FastAPI Request Processing Pipeline

```text
  +------------------+     +------------------+     +------------------+
  |  Incoming HTTP   +---->+  Uvicorn (ASGI)  +---->+ Starlette Router |
  |  Request         |     |  Server          |     +--------+---------+
  +------------------+     +------------------+              |
                                                             v
                                                   +--------+---------+
                                                   |  FastAPI         |
                                                   |  Pydantic        |
                                                   |  Validation      |
                                                   +--------+---------+
                                                             |
                                                             v
                                                   +--------+---------+
                                                   |  Dependencies    |
                                                   |  Resolution      |
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

---

## 7. API Lifecycle

```text
  +----------+    +----------+    +----------+    +----------+
  |  Design  +---->  Develop +---->  Testing +---->  Deploy  |
  | OpenAPI  |    | FastAPI  |    | Unit/Int |    | Docker + |
  |  Spec    |    |  Code    |    |   E2E    |    |  Cloud   |
  +----------+    +----------+    +----------+    +----+-----+
       ^                                               |
       |                                               v
  +----+------+    +----------+               +--------+--+
  | Versioning|<---+ Changes? +<--------------+ Monitoring|
  | /v1  /v2  |    |          |               | Logs +    |
  +-----------+    +----------+               | Alerts    |
                                              +----------++
```

---

## 8. JWT Authentication Flow

```text
  Client            Server /login         User DB       Protected Endpoint
    |                     |                  |                  |
    +---POST /login------->                  |                  |
    |   user + password   |                  |                  |
    |                     +---verify creds-->|                  |
    |                     |<--user found-----+                  |
    |                     +---create JWT (sign w/ SECRET_KEY)   |
    |<--{access_token,----+                  |                  |
    |    token_type}      |                  |                  |
    |                                                           |
    +---GET /predict (Authorization: Bearer <token>)---------->|
    |                                        +--verify sig----->|
    |                                        +--extract user--->|
    |<--200 OK + data---------------------------------------------------+
```

---

## 9. Middleware Pipeline

```text
  +-----------+
  |  Request  |
  +-----+-----+
        |
        v
  +-----+-----+    +-----------+
  |Middleware1+---->   CORS    |
  +-----+-----+    +-----------+
        |
        v
  +-----+-----+    +-----------+
  |Middleware2+---->  Timing   |
  +-----+-----+    +-----------+
        |
        v
  +-----+-----+    +-----------+
  |Middleware3+----> Rate Limit|
  +-----+-----+    +-----------+
        |
        v
  +-----+---------+
  |Endpoint Handler|
  +-----+---------+
        |
        v
  +-----+-----+    +--------------+
  |Middleware3+---->Post-process  |
  +-----+-----+    +--------------+
        |
        v
  +-----+-----+    +--------------+
  |Middleware2+---->Post-process  |
  +-----+-----+    +--------------+
        |
        v
  +-----+-----+    +--------------+
  |Middleware1+---->Post-process  |
  +-----+-----+    +--------------+
        |
        v
  +-----+-----+
  |  Response |
  +-----------+
```

---

## 10. Dependency Injection

```text
  +--------------------+
  |  Endpoint Function |
  +--+----------+--+---+
     |          |  |
     v          v  v
  +--+----------+--+---+
  |       Depends()    |
  +--+----------+--+---+
     |          |  |
     v          v  v
  +-------+ +--------+ +-----------+
  | get_db| |get_user| |get_settings|
  +---+---+ +---+----+ +-----+------+
      |         |            |
      v         v            v
  +--------+ +-------+ +-----------+
  |Database| |  JWT  | |  .env     |
  |        | | Store | |  Config   |
  +--------+ +-------+ +-----------+
```

---

## 11. CRUD — HTTP Methods to Database

```text
  +---------------------+          +------------+
  |  POST   /items/     +--Create->+            |
  +---------------------+          |            |
  +---------------------+          |            |
  |  GET    /items/     +--Read---->  Database  |
  +---------------------+          |            |
  +---------------------+          |            |
  |  GET    /items/{id} +--Read---->            |
  +---------------------+          |            |
  +---------------------+          |            |
  |  PUT    /items/{id} +-Update-->+            |
  +---------------------+          |            |
  +---------------------+          |            |
  |  DELETE /items/{id} +-Delete-->+            |
  +---------------------+          +------------+
```

---

## 12. Database Project Structure

```text
  +----------------------------------------------+
  |                  main.py                     |
  |          FastAPI App + Routes                |
  +----------+--------------+-------------------+
             |              |              |
             v              v              v
  +----------+--+  +--------+---+  +------+----------+
  | schemas.py  |  |  crud.py   |  |  database.py    |
  | Pydantic    |  |  DB Ops    |  |  get_db()       |
  | Models      |  |            |  |  dependency     |
  +-------------+  +-----+------+  +------+----------+
                         |                |
                         v                |
                   +-----+------+         |
                   | models.py  +<--------+
                   | SQLAlchemy |
                   +-----+------+
                         |
                         v
                   +-----+-----------+
                   |  Engine+Session |
                   +-----+-----------+
                         |
                         v
                   +-----+-----------+
                   | SQLite/Postgres |
                   +-----------------+
```

---

## 13. ML Model Serialization Lifecycle

```text
  +-----------+    +-----------+    +------------------+    +-----------+    +----------+
  | Train     +--->+ Serialize +--->+ model.pkl /      +--->+ Load at   +--->+ Serve    |
  | Model     |    | Save to   |    | .joblib / .keras |    | API Start |    | FastAPI  |
  +-----------+    | Disk      |    +------------------+    +-----------+    +----+-----+
                   +-----------+                                                  |
                                                                                  v
                                                                           +------+------+
                                                                           | Client Gets |
                                                                           | Predictions |
                                                                           +-------------+
```

---

## 14. ML Model Serving Pipeline

```text
  +----------+
  |  Client  |
  +----+-----+
       | HTTP POST + JSON
       v
  +----+----------------+
  |  FastAPI Endpoint   |
  +----+----------------+
       |
       v
  +----+----------------+
  |  Pydantic           |
  |  Input Validation   |
  +----+--------+-------+
       |        |
     Valid    Invalid
       |        |
       v        v
  +---------+  +------------------+
  | Input   |  | 422 Validation   |
  | Preproc |  | Error            |
  +----+----+  +------------------+
       |
       v
  +----+----------------+
  |  ML Model Inference |
  +----+----------------+
       |
       v
  +----+----------------+
  |  Output             |
  |  Postprocessing     |
  +----+----------------+
       |
       v
  +----+----------------+
  |  Pydantic Response  |
  +----+----------------+
       | JSON Response
       v
  +----+-----+
  |  Client  |
  +----------+
```

---

## 15. Batch Prediction Flow

```text
  +--------+
  |  Client|
  +----+---+
       |
       v
  +----+------------------------------+
  |  POST /predict/batch              |
  |  or  POST /predict/csv            |
  +----+------------------------------+
       |
       v
  +----+------------------------------+
  |  Loop over samples /              |
  |  Vectorized batch call            |
  +----+------------------------------+
       |
       v
  +----+----------+
  |  ML Model     |
  +----+----------+
       |
       v
  +----+-----------------------------------+
  |  BatchOutput                           |
  |  predictions, total_samples,           |
  |  total_time_ms, avg_time_per_sample_ms |
  +----+-----------------------------------+
       |
       v
  +----+---+
  | Client |
  +--------+
```

---

## 16. API Key Validation Flow

```text
  Client                   FastAPI                  Key Store
    |                         |                         |
    +---GET /predict--------->|                         |
    |   X-API-Key: sk-xxx     |                         |
    |                         +---lookup key----------->|
    |                         |<--valid / invalid-------+
    |                         |
    |                    +----+-----+
    |                    |         |
    |                  Valid     Invalid
    |                    |         |
    |                    v         v
    |<--200 OK + result--+  +------+----------+
    |                       | 401 Unauthorized|
    |<--401-----------------+ Invalid API key |
                             +-----------------+
```

---

## 17. Testing Strategy

```text
  +------------------------------------------------------------+
  |                    Testing Strategy                        |
  +--------------------+-------------------+------------------+
  |    Unit Tests      | Integration Tests |   ML Mocking     |
  +--------------------+-------------------+------------------+
  | pytest             | TestClient        | unittest.mock    |
  | Schemas            | Full endpoints    | patch predictor  |
  | Preprocessing      | API + DB + Model  | Deterministic    |
  | Field validation   | Status codes      | Fast, no model   |
  | Error on bad input | Response shape    | needed           |
  +--------------------+-------------------+------------------+
```

---

## 18. Full System Architecture

```text
  +------------------+
  |     Clients      |
  | Web / Mobile /   |
  | External Service |
  +--------+---------+
           |
           v
  +--------+---------+
  | Middleware Layer |
  | CORS, Logging,   |
  | Rate Limiting    |
  +--------+---------+
           |
           v
  +--------+---------+
  |   Auth Layer     |
  |  JWT / API Key   |
  +--------+---------+
           |
           v
  +--------+---------+
  |  Router          |
  |  Endpoints       |
  +--------+---------+
           |
     +-----+-----+
     |           |
     v           v
  +--+--------+ ++----------+
  | Dependency| | Pydantic  |
  | Injection | | Validation|
  | DB Session| | Req / Resp|
  +-----------+ +--+--------+
                   |
             +-----+------+
             |            |
             v            v
  +----------+--+  +------+-------+
  | ML Model    |  | Data Layer   |
  | Preprocess  |  | PostgreSQL   |
  | Inference   |  | Redis Cache  |
  | Postprocess |  | Model Files  |
  +-------------+  +--------------+
```

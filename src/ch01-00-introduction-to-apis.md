# Introduction to APIs

This chapter covers the fundamental concepts of APIs. We explore what APIs are, why they exist, the different types and protocols, and how they form the backbone of modern software architecture. Understanding APIs is essential before diving into FastAPI, as FastAPI is a framework for building APIs — and you need to understand what you are building before building it.

```text
  +-----------------------------------------------------------+
  |                          APIs                             |
  +---------------+---------------+-------------+------------+
  |     What      |      Why      |    Types    | Protocols  |
  +---------------+---------------+-------------+------------+
  | Software      | Decouple FE/  | REST        | HTTP/HTTPS |
  | communication | BE            | SOAP        | JSON       |
  | Rules &       | 3rd-party     | GraphQL     | Status     |
  | protocols     | access        | gRPC        | Codes      |
  | Language-     | Multi-        | WebSocket   |            |
  | agnostic      | platform      |             |            |
  |               | ML serving    |             |            |
  +---------------+---------------+-------------+------------+
  |              Components                                   |
  +-----------------------------------------------------------+
  |   Endpoints  |  Methods  |  Headers  |  Body  |  Auth    |
  +-----------------------------------------------------------+
```

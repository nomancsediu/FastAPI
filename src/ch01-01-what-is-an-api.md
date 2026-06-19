# What is an API?

## Definition

An API (Application Programming Interface) is a mechanism that lets software components communicate with each other using defined rules and protocols. Think of it as a messenger that takes a request from one application, delivers it to another application, and then returns the response back. Just as a waiter in a restaurant takes your order (request) to the kitchen (server), brings the food back (response), and never cooks the food themselves — an API acts as the intermediary between the client and the server.

## The Problem APIs Solve: Monolithic Architecture

Before APIs became mainstream, most applications were built using a **monolithic architecture**. In a monolithic system, the front end (user interface) and the back end (business logic, database access) are tightly coupled into a single application. While this approach works for small projects, it creates several critical problems as applications grow:

- **Tight coupling**: Changes in one part of the system can break the entire application. If you modify the front end, you might accidentally break the database layer, and vice versa. This makes maintenance and updates extremely risky and time-consuming.
- **No third-party access**: In a monolithic system, there is no clean way for external applications to access your data or services. For example, if IRCTC (Indian Railway's ticketing system) were monolithic, travel apps like MakeMyTrip could not access train schedule data without direct database access, which is a massive security risk.
- **Code duplication**: When companies want to support multiple platforms (website, Android app, iOS app), they often end up duplicating the back-end logic for each platform, leading to wasted effort and inconsistent behavior across platforms.

## API as the Middle Layer

The fundamental shift that APIs introduce is **decoupling**. Instead of the front end directly accessing the back end and database, an API sits as a middle layer:

```
[Front End]  -->  [API Layer]  -->  [Back End / Database]
```

The front end (whether it is a website, a mobile app, or a desktop application) sends HTTP requests to the API. The API processes the request, interacts with the back end or database as needed, and returns the response in a structured format (typically JSON). This decoupling provides several critical advantages that have made APIs the standard way to build modern software.

```text
   Monolithic Architecture        |    API Architecture
                                   |
  +------------+  +------------+  |  +------------+
  | Web Front  +->+ BE Logic   |  |  | Web Front  +--+
  +------------+  +------------+  |  +------------+  |
  +------------+  +------------+  |  +------------+  |    +-----------+
  | Mobile App +->+ BE copy    |  |  | Mobile App +--+--->+  API      |
  +------------+  +------------+  |  +------------+  |    |  Layer    |
  +------------+  +------------+  |  +------------+  |    +-----------+
  | iOS App    +->+ BE copy    |  |  | iOS App    +--+          |
  +------------+  +-----+------+  |  +------------+             v
                        |         |                       +-----------+
                        v         |                       |  Backend  |
                  +-----+------+  |                       +-----------+
                  | DB  DB  DB |  |                             |
                  | (x3 dupl.) |  |                             v
                  +------------+  |                       +-----------+
                                  |                       | DB single |
                                  |                       +-----------+
```

## Multi-Platform Support

The smartphone revolution created a demand for applications across web, Android, and iOS platforms simultaneously. Without APIs, development teams would need to build separate monolithic back ends for each platform, resulting in duplicated logic, inconsistent behavior, and multiplied maintenance costs. With API architecture, you build **one back end and one database**, then create multiple front ends that all communicate through the same API. Companies like Google, Uber, and Zomato all rely on this architecture to serve millions of users across dozens of platforms from a single API back end.

## APIs in the Machine Learning Domain

In the ML world, APIs serve a crucial role: they act as the bridge between a trained machine learning model and the applications that need to use it. When you train a model in a Jupyter notebook, it lives only on your machine. To make that model useful to a product team building a web app or mobile app, you need to serve it through an API. This way, any application can send input data (like an image or text) to the API, and receive the model's prediction (like a classification label or generated text) as a response. This is the core problem that this entire book addresses: how to take a trained ML model and expose it as a production-ready API using FastAPI.

```text
  +-------------+
  |   Web App   +--+
  +-------------+  |
  +-------------+  |    +------------------+    +------------------+
  | Mobile App  +--+--->+  FastAPI ML API  +--->+  ML Model        |
  +-------------+  |    +--------+---------+    |  Inference       |
  +-------------+  |             |              +--------+---------+
  |   Script    +--+             v                       |
  +-------------+       +--------+--------+              |
                         |   Database     |              |
                         +--------+-------+              |
                                  |                      |
                                  +----------+-----------+
                                             |
                                             v
                                  +----------+-----------+
                                  |    JSON Response     |
                                  +----------------------+
```

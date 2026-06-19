# Database Basics

## Why Databases in ML APIs?

Databases serve several important purposes in ML APIs. They store prediction results for auditing and analysis, maintain model version information and metadata, manage user data for authentication, log API usage for billing and monitoring, and cache frequently requested predictions to reduce model load. Choosing the right database depends on your use case: PostgreSQL or MySQL for structured data, MongoDB for document-based storage, Redis for caching, and specialized vector databases (like Pinecone or Milvus) for embedding-based search.

## SQL vs NoSQL

**SQL databases** (PostgreSQL, MySQL, SQLite) use structured tables with defined schemas. They provide strong consistency guarantees (ACID transactions), support complex queries with JOINs, and are ideal for applications where data relationships are well-defined. **NoSQL databases** (MongoDB, Cassandra, Redis) offer flexible schemas, horizontal scalability, and are optimized for specific access patterns. For most ML APIs, a SQL database like PostgreSQL is the right choice for storing structured metadata (users, predictions, model versions), while a NoSQL database or file storage system might be used for storing raw inputs and outputs.

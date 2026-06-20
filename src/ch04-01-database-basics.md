# Database Basics

## Why Databases in ML APIs?

Databases serve several critical purposes in production ML APIs:

| Use Case | What We Store | Why |
|----------|--------------|-----|
| **Audit trail** | Input features, predictions, confidence, timestamp | Debug incorrect predictions, retrain with real data |
| **Model versioning** | Model version used for each prediction | Reproduce results, A/B test between versions |
| **User feedback** | User corrections to predictions | Improve model quality over time |
| **Authentication** | API keys, user credentials | Secure the API |

## Our Migration Path

| Stage | Storage | Persistence | Chapter |
|-------|---------|-------------|---------|
| Start | In-memory list | Lost on restart | Ch 3 |
| **Now** | **SQLite via SQLAlchemy** | **Persisted to file** | **Ch 4** |
| Production | PostgreSQL | Full ACID | Your choice |

## SQL vs NoSQL for ML APIs

| Aspect | SQL (SQLite → PostgreSQL) | NoSQL (MongoDB) |
|--------|---------------------------|-----------------|
| **Schema** | Fixed columns, strong typing | Flexible documents |
| **Consistency** | ACID guaranteed | Eventual consistency |
| **Best for** | Prediction logs, user data, metadata | Raw feature storage, large blobs |
| **Migration** | Start with SQLite, switch to PostgreSQL with 1 line change | Harder to migrate |

We use **SQLite** here because it requires zero setup (no server, no installation). The SQLAlchemy code works identically with PostgreSQL — change one line in `database.py` when you deploy.

## What is SQLAlchemy?

SQLAlchemy is Python's most popular **Object-Relational Mapper (ORM)**. It lets you write Python classes instead of raw SQL:

```python
# Raw SQL — error-prone, hard to maintain
cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
row = cursor.fetchone()

# SQLAlchemy ORM — clean, type-safe
item = db.query(Item).filter(Item.id == item_id).first()
```

The ORM translates Python method calls into SQL behind the scenes. You can switch from SQLite to PostgreSQL by changing the connection URL without touching any of your query code.

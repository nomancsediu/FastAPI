# Best Practices — Quick Summary

## Keep Secrets Out of Code

```bash
# .env (add to .gitignore!)
API_KEY=your-secret-key
SECRET_KEY=another-secret
```

```python
# config.py
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")
```

## Use Status Codes Correctly

| Situation | Status Code |
|-----------|-------------|
| Created successfully | `201` |
| Deleted successfully | `204` |
| Validation error | `422` |
| Not found | `404` |
| Unauthorized | `401` |

## Log Important Events

```python
import logging
logging.basicConfig(level=logging.INFO)

@app.post("/items/")
def create_item(item: Item, db: Session = Depends(get_db)):
    logging.info(f"Creating item: {item.name}")
    ...
```

## Small Tips

- Run with `--reload` in development, NOT in production
- Use `pip freeze > requirements.txt` to save exact versions
- Test your API with Swagger UI (`/docs`) and curl
- One file = one responsibility (database.py, models.py, auth.py, etc.)

## Your Final Project

```
fastapi-crud/
├── main.py           # FastAPI app + all routes
├── database.py       # Database connection
├── models.py         # Table definitions
├── auth.py           # Authentication logic
├── config.py         # Environment variables
├── .env              # Secrets (git-ignored)
├── requirements.txt
├── items.db          # SQLite database
```

Now let's learn how to test everything.

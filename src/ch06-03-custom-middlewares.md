# Environment Variables

Never write secrets (API keys, passwords) directly in your code. Use a `.env` file instead.

## Step 1: Create .env

```bash
echo "API_KEY=my-super-secret-key
SECRET_KEY=jwt-secret-change-in-production
DATABASE_URL=sqlite:///./items.db" > .env
```

## Step 2: Read with python-dotenv

```bash
pip install python-dotenv
```

```python
# config.py
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

## Step 3: Use in Code

```python
# main.py
from config import API_KEY, DATABASE_URL

# Use DATABASE_URL when creating database engine
# Use API_KEY in your auth system
```

## Security Tips

- Add `.env` to `.gitignore` (never commit secrets!)
- Use different keys for development and production
- Rotate keys periodically

Your project should now look like:

```
fastapi-crud/
├── main.py
├── database.py
├── models.py
├── auth.py
├── config.py          # NEW
├── .env               # NEW (git-ignored)
├── requirements.txt
├── items.db
```

# Debugging Tips

## 1. Read the Error Message

When something breaks, the server terminal shows a **traceback**. Read the last line first — it tells you exactly what went wrong.

## 2. Use Swagger UI

`http://localhost:8000/docs` shows you exactly what each endpoint expects. If you get a 422 error, compare your request with the Swagger UI example.

## 3. Use curl for Testing

```bash
# Test health
curl http://localhost:8000/health

# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'

# Test with auth
curl http://localhost:8000/items/ \
  -H "Authorization: Bearer <token>"
```

## 4. Add Logging

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("myapp")

@app.post("/predict")
def predict(data: InputData):
    logger.info(f"Got request: {data.features}")
    result = predictor.predict(data.features)
    logger.info(f"Result: {result}")
    return result
```

## 5. The 5-Minute Debug Workflow

```
1. What status code?
   ├── 4xx → Check what you're sending (Swagger UI helps)
   └── 5xx → Check server terminal for traceback

2. Can you reproduce with curl?
   ├── Yes → Compare with working example
   └── No → It's a frontend issue, not API

3. Is the model loaded?
   ├── Call GET /health to check
   └── If not → Check model file path
```

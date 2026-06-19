# Debugging Techniques

## Logging

Structured logging is the most important debugging tool for production APIs. Set up logging with different levels (DEBUG, INFO, WARNING, ERROR) and include contextual information in every log entry:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@app.post("/predict/")
def predict(input_data: IrisInput):
    logger.info(f"Prediction request: features={input_data.features}")
    try:
        result = predict.predictor.predict(input_data.features)
        logger.info(f"Prediction result: {result['prediction']} (confidence: {result['confidence']})")
        return result
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction failed")
```

## Global Exception Handler

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url}: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please try again later."}
    )
```

## Testing with cURL

cURL is an invaluable tool for debugging API endpoints from the command line:

```bash
# Basic GET request
curl http://localhost:8000/health

# POST with JSON body
curl -X POST http://localhost:8000/predict   -H "Content-Type: application/json"   -d '{"features": [5.1, 3.5, 1.4, 0.2]}'

# With authentication
curl -X POST http://localhost:8000/predict   -H "Content-Type: application/json"   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9..."   -d '{"features": [5.1, 3.5, 1.4, 0.2]}'

# Upload a file
curl -X POST http://localhost:8000/predict-image   -F "file=@image.jpg"   -F "model_name=resnet50"
```

## Debugging Workflow

When debugging an ML API issue, follow this systematic approach: first, check the logs for error messages and stack traces. Second, reproduce the issue with a minimal cURL command to isolate it from the front end. Third, verify the input data format matches what the model expects. Fourth, test the model prediction locally (outside the API) to confirm the model itself works. Fifth, check the API endpoint code for incorrect data transformation or response formatting. This systematic approach helps you quickly identify whether the issue is in the client, the API layer, the data pipeline, or the model itself.

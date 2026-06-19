# Handling Batch Predictions

## Why Batch Predictions?

Individual prediction requests work well for real-time applications where you predict one sample at a time. However, many ML use cases require processing multiple samples at once — bulk scoring of leads, batch image classification, processing uploaded CSV files, or nightly re-scoring of all records. Batch prediction endpoints optimize for throughput by processing multiple samples in a single request, reducing the overhead of multiple HTTP round trips.

## Implementation

```python
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
import predict

app = FastAPI()

class BatchInput(BaseModel):
    samples: List[List[float]]

class BatchOutput(BaseModel):
    predictions: List[dict]
    total_samples: int
    total_time_ms: float
    avg_time_per_sample_ms: float

@app.post("/predict/batch", response_model=BatchOutput)
def predict_batch(input_data: BatchInput):
    import time
    start_time = time.time()
    results = []
    for sample in input_data.samples:
        result = predict.predictor.predict(sample)
        results.append(result)
    total_time = (time.time() - start_time) * 1000

    return BatchOutput(
        predictions=results,
        total_samples=len(input_data.samples),
        total_time_ms=round(total_time, 2),
        avg_time_per_sample_ms=round(total_time / len(input_data.samples), 2)
    )

@app.post("/predict/csv")
async def predict_csv(file: UploadFile = File(...)):
    import pandas as pd
    import io

    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    features = df.values.tolist()
    results = [predict.predictor.predict(sample) for sample in features]

    return {
        "filename": file.filename,
        "total_rows": len(df),
        "predictions": results
    }
```

## Optimizing Batch Performance

For large batches, you can leverage NumPy's vectorized operations and the model's native batch prediction capability. Instead of predicting one sample at a time, convert all samples to a 2D NumPy array and pass it to the model in a single call. Most scikit-learn models and all deep learning frameworks support batch prediction natively, and it is significantly faster than looping over individual samples.

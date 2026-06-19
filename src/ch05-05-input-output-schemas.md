# Input and Output Schemas

## Designing Input Schemas

The input schema defines what data the API expects from the client. For ML APIs, this is particularly important because models require specific input formats. A well-designed input schema validates the data before it reaches the model, preventing crashes and providing clear error messages:

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum

class ModelName(str, Enum):
    logistic_regression = "logistic_regression"
    random_forest = "random_forest"
    svm = "svm"

class PredictionInput(BaseModel):
    features: List[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Exactly 4 iris features: sepal_length, sepal_width, petal_length, petal_width"
    )
    model_name: ModelName = Field(
        default=ModelName.logistic_regression,
        description="The ML model to use for prediction"
    )

    @validator("features")
    def validate_features(cls, v):
        for val in v:
            if val < 0 or val > 15:
                raise ValueError("Feature values should be between 0 and 15")
        return v

class PredictionOutput(BaseModel):
    prediction: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    model_used: str
    prediction_time_ms: float
```

## Designing Output Schemas

The output schema defines what the API returns to the client. For ML APIs, the response typically includes the prediction result, confidence score, model version, and metadata like inference time. Separating input and output schemas (rather than using a single schema for both) allows you to return different fields than what was sent in, include computed fields (like inference time), and hide internal implementation details from the client.

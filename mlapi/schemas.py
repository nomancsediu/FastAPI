from pydantic import BaseModel, Field
from typing import List


class IrisInput(BaseModel):
    features: List[float] = Field(
        ...,
        min_length=4,
        max_length=4,
    )


class IrisOutput(BaseModel):
    species: str
    confidence: float = Field(ge=0.0, le=1.0)


class BatchInput(BaseModel):
    samples: List[List[float]] = Field(..., min_length=1)


class BatchOutput(BaseModel):
    predictions: List[IrisOutput]
    count: int

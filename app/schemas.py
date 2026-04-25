
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class PredictionResponse(BaseModel):
    query: str
    prediction: int
    label: str
    confidence: float
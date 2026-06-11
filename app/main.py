from fastapi import FastAPI
from app.model.predict import predict
from app.Schema.preprocess_schema import (
    LoanPredictionRequest,
    LoanPredictionResponse,
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict", response_model=LoanPredictionResponse)
def predict_loan(req: LoanPredictionRequest):
    return predict(req)

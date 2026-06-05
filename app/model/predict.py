from joblib import load
from app.Schema.preprocess_schema import LoanPredictionRequest, LoanPredictionResponse, preprocess_prediction_request
from app.config.env_config import EnvConfig

env_config = EnvConfig()

model = load(env_config.MODEL_PATH)

def predict(payload: LoanPredictionRequest) -> LoanPredictionResponse:
 
    df = preprocess_prediction_request(payload)

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return LoanPredictionResponse(int(prediction), round(float(probability), 4),)
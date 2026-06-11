import joblib
from app.Schema.preprocess_schema import LoanPredictionRequest, LoanPredictionResponse
from app.config.env_config import EnvConfig
import pandas as pd

env_config = EnvConfig()

def predict(request: LoanPredictionRequest) -> LoanPredictionResponse:
    model = joblib.load(env_config.MODEL_PATH)
    preprocessor = joblib.load(env_config.PREPROCESSOR_PATH)

    request_data = request.model_dump(mode="json")

    df = pd.DataFrame([request_data])
    
    X_processed = preprocessor.transform(df)
    
    prediction = model.predict(X_processed)
    probability = model.predict_proba(X_processed)

    return LoanPredictionResponse(
        prediction=int(prediction[0]),
        approval_probability=float(probability[0][1])
    )
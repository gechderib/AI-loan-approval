import joblib
from app.Schema.preprocess_schema import LoanPredictionRequest, LoanPredictionResponse
from app.config.env_config import EnvConfig
import pandas as pd

env_config = EnvConfig()

def convert_request_values(data: dict) -> dict:
    mappings = {
        "loan_limit": {"cf": 1, "ncf": 0},
        "approv_in_adv": {"nopre": 0, "pre": 1},
        "Credit_Worthiness": {"l1": 1, "l2": 0},
        "open_credit": {"nopc": 0, "opc": 1},
        "business_or_commercial": {"nob/c": 0, "b/c": 1},
        "Neg_ammortization": {"not_neg": 0, "neg_amm": 1},
        "interest_only": {"not_int": 0, "int_only": 1},
        "lump_sum_payment": {"not_lpsm": 0, "lpsm": 1},
        "construction_type": {"sb": 0, "mh": 1},
        "Secured_by": {"home": 0, "land": 1},
        "co_applicant_credit_type": {"CIB": 0, "EXP": 1},
        "submission_of_application": {"to_inst": 1, "not_inst": 0},
        "Security_Type": {"direct": 0, "Indriect": 1},

        # 🔥 ADD THIS (your current error)
        "age": {
            "<25": 0,
            "25-34": 1,
            "35-44": 2,
            "45-54": 3,
            "55-64": 4,
            "65-74": 5,
            ">74": 6
        }
    }

    converted = {}

    for key, value in data.items():
        if key in mappings:
            converted[key] = mappings[key].get(value, value)
        else:
            converted[key] = value

    return converted

def predict(request_data: LoanPredictionRequest) -> LoanPredictionResponse:
    pipeline = joblib.load(env_config.MODEL_PATH)

    raw_data = request_data.model_dump(mode="json")

    # 🔥 convert categorical strings → numbers
    converted_data = convert_request_values(raw_data)

    input_df = pd.DataFrame([converted_data])

    prediction = pipeline.predict(input_df)
    probability = pipeline.predict_proba(input_df)

    return LoanPredictionResponse(
        prediction=int(prediction[0]),
        approval_probability=float(probability[0][1])
    )
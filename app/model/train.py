import os
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import joblib
from app.config.env_config import EnvConfig

env_config = EnvConfig()

def load_processed_data(processed_file_path):
    try:
        df = pd.read_csv(processed_file_path)
  
        X_train = df.drop(columns=["Status"])
        y_train = df["Status"]
        return X_train, y_train
    except Exception as e:
        print(f"An error occurred while loading processed data: {e}")
        return None, None

def ensure_model_directory_exists(model_file_path):
    directory = os.path.dirname(model_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def evaluate_model(model, X_test, y_test):
    try:
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print("Confusion Matrix:")
        print(cm)
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")
    except Exception as e:
        print(f"An error occurred during model evaluation: {e}") 
    

def train_loan_approval_model(processed_train_file_path, processed_test_file_path, model_file_path):
    try:
        X_train, y_train = load_processed_data(processed_train_file_path)
        X_test, y_test = load_processed_data(processed_test_file_path)
        if X_train is None or y_train is None:
            print("Failed to load training data. Aborting model training.")
            return
                
        one_hot_encoding_columns = [
            "loan_type",
            "loan_purpose",
            "occupancy_type",
            "Region",
            "Gender",
            
            #### To handle all categorical columns using  one hot encoding
            "Security_Type", "submission_of_application", "co_applicant_credit_type", "Secured_by", "construction_type", "lump_sum_payment", "interest_only", "Neg_ammortization", "business_or_commercial", "open_credit", "Credit_Worthiness", "approv_in_adv", "loan_limit", "age"
        ]

        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "categorical",
                    OneHotEncoder(
                        handle_unknown="ignore"
                    ),
                    one_hot_encoding_columns,
                )
            ],
            remainder="passthrough"
        )
        
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            (
                "model",
                LGBMClassifier(
                    n_estimators=500,
                    learning_rate=0.05,
                    random_state=42
                )
            )
        ])


        pipeline.fit(X_train, y_train)
        print(X_train.columns)

        ensure_model_directory_exists(model_file_path)
        print("Model evaluation using LGBMClassifier...")
        evaluate_model(pipeline, X_test, y_test)
        
        joblib.dump(pipeline, model_file_path)
        print(f"Model trained and saved to: {model_file_path}")
    except Exception as e:
        print(f"An error occurred during model training: {e}")
    
# TN   FP
# FN   TP 
 
if __name__ == "__main__":
    processed_train_file_path = env_config.PROCESSED_DATA_TRAIN_PATH
    processed_test_file_path = env_config.PROCESSED_DATA_TEST_PATH
    model_file_path = env_config.MODEL_PATH
    train_loan_approval_model(processed_train_file_path, processed_test_file_path, model_file_path)

# Confusion Matrix:
# [[22152   342]
#  [ 2704  4536]]
# Accuracy: 0.8976
# Precision: 0.9299
# Recall: 0.6265
# F1 Score: 0.7486

import os
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from joblib import dump
from app.config.env_config import EnvConfig

env_config = EnvConfig()

def load_processed_data(processed_file_path):
    try:
        df = pd.read_csv(processed_file_path)

        # print(f'{processed_file_path}{df.groupby("Status")["Interest_rate_spread"].describe()}')
        # print(pd.crosstab(df["credit_type_EQUI"],df["Status"]))
        
        # for col in [
        #     "rate_of_interest",
        #     "Upfront_charges",
        #     "approv_in_adv",
        #     "Credit_Worthiness"
        # ]:
        #     print("\n", col)
        #     print(df.groupby("Status")[col].describe())
                
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
        
        leakage_columns = [
            "Interest_rate_spread",
            "credit_type_EQUI",
            "rate_of_interest",
            "Upfront_charges",
        ]
        
        X_train = X_train.drop(columns=leakage_columns)
        X_test = X_test.drop(columns=leakage_columns)

        dump(X_train.columns.tolist(), env_config.FEATURE_COLUMNS_PATH)
                
        # pipeline = make_pipeline(
        #     StandardScaler(), 
        #     LogisticRegression(max_iter=10000, random_state=42, n_jobs=-1)   
        # )
        
        # pipeline = RandomForestClassifier(
        #     n_estimators=300
        # )

        # pipeline = XGBClassifier(
        #     n_estimators=500,
        #     learning_rate=0.05
        # )
        
        pipeline = LGBMClassifier(
            # n_estimators=500,
            # learning_rate=0.05
            
            n_estimators=1000,
            learning_rate=0.03,
            random_state=42
        )
        


        pipeline.fit(X_train, y_train)
        print(X_train.columns)
        # for feature, importance in sorted(
        #     zip(X_train.columns, pipeline.feature_importances_),
        #     key=lambda x: x[1],
        #     reverse=True
        # ):
        #     print(feature, importance)
                
        ensure_model_directory_exists(model_file_path)
        print("Model evaluation using LGBMClassifier...")
        evaluate_model(pipeline, X_test, y_test)
        
        dump(pipeline, model_file_path)
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

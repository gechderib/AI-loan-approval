import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from joblib import dump
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
        
        model = LogisticRegression(max_iter=1000, random_state=42)
        model.fit(X_train, y_train)
        
        ensure_model_directory_exists(model_file_path)
        
        evaluate_model(model, X_test, y_test)
        
        dump(model, model_file_path)
        print(f"Model trained and saved to: {model_file_path}")
    except Exception as e:
        print(f"An error occurred during model training: {e}")
 
 
if __name__ == "__main__":
    processed_train_file_path = env_config.PROCESSED_DATA_TRAIN_PATH
    processed_test_file_path = env_config.PROCESSED_DATA_TEST_PATH
    model_file_path = env_config.MODEL_PATH
    train_loan_approval_model(processed_train_file_path, processed_test_file_path, model_file_path)
import joblib
import os
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score,roc_auc_score, classification_report
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import RandomizedSearchCV

from app.config.env_config import EnvConfig
from app.services.preprocess import preprocess_data

env_config = EnvConfig()

def ensure_model_directory_exists(model_file_path):
    directory = os.path.dirname(model_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)





def evaluate_model(model, y_pred, y_test, probs):
    
    try:
        preprocessor = joblib.load(env_config.PREPROCESSOR_PATH)
        
        cm = confusion_matrix(y_test, y_pred)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, probs)

        importance = pd.DataFrame({
            "feature": preprocessor.get_feature_names_out(),
            "importance": model.feature_importances_
        })

        importance.sort_values(
            "importance",
            ascending=False
        ).head(20)
        print("importance")
        print(importance)
        
        print("Confusion Matrix:")
        print(cm)
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")
        print(f"AUC: {auc:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
    except Exception as e:
        print(f"An error occurred during model evaluation: {e}") 
    

def train_loan_approval_model(raw_file_path, model_file_path):
    try:
        X_train, X_test, y_train, y_test = preprocess_data(raw_file_path)
        if X_train is None or y_train is None:
            print("Failed to load training data. Aborting model training.")
            return

        models = {
            # "Logistic Regression": LogisticRegression(max_iter=1000),
            # "Decision Tree": DecisionTreeClassifier(random_state=42),
            # "Random Forest": RandomForestClassifier(
            #     n_estimators=200,
            #     random_state=42
            # ),
            # "Gradient Boosting": GradientBoostingClassifier(
            #     random_state=42
            # ),
            # "AdaBoost": AdaBoostClassifier(
            #     random_state=42
            # ),
            # "KNN": KNeighborsClassifier(
            #     n_neighbors=5
            # ),
            # "SVM": SVC(
            #     kernel="rbf",
            #     probability=True,
            #     random_state=42
            # ),
            # "XGBClassifier": XGBClassifier(
            #     n_estimators=300
            # ),

            "LGBMClassifier": LGBMClassifier(
                random_state=42,
                class_weight="balanced",
                n_jobs=-1,
                verbose=-1,
                learning_rate=0.05,
                n_estimators=400,
                num_leaves=31,
                max_depth=7,
                subsample=0.8,
                colsample_bytree=0.8,
                reg_alpha=0.1,
                reg_lambda=0.1
            )   
        }


        for model_name, model in models.items():        
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            
            probs = model.predict_proba(X_test)[:, 1]

            ensure_model_directory_exists(model_file_path)
            print(f"Model evaluation using {model_name}")
            evaluate_model(model, y_pred, y_test, probs)
            
            joblib.dump(model, model_file_path)
            print(f"Model trained and saved to: {model_file_path}")
    except Exception as e:
        print(f"An error occurred during model training: {e}")
    
# TN   FP
# FN   TP 
 
if __name__ == "__main__":
    
    raw_file_path = env_config.RAW_DATA_PATH
    model_file_path = env_config.MODEL_PATH
    
    train_loan_approval_model(raw_file_path, model_file_path)


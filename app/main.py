# from fastapi import FastAPI
# from app.model.predict import predict
# from app.Schema.preprocess_schema import (
#     LoanPredictionRequest,
#     LoanPredictionResponse,
# )

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.post("/predict", response_model=LoanPredictionResponse)
# def predict_loan(req: LoanPredictionRequest):
#     return predict(req)

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

def preprocess_data(raw_file_path, preprocessor_path):

    nominal_features = [
        "gender",
        "city",
        "owns_house",
    ]
    
    numeric_features = [
        "age",
        "income",
        "credit_score",
        "years_employed",
        "loan_amount"
    ]
    
    ordinal_features = [
        "education"
    ]
    
    drop_featurs = [
        "customer_id",
    ]

    education_order = [
        "High School",
        "Bachelor",
        "Master",
        "PhD"
    ]
    
    nominal_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])
    
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    
    ordinal_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OrdinalEncoder(categories=[education_order]))
    ])

    preprocessor = ColumnTransformer([
        ("nom", nominal_pipeline, nominal_features),
        ("num", numeric_pipeline, numeric_features),
        ("ord", ordinal_pipeline, ordinal_features),
    ])
    
    df = pd.read_csv(raw_file_path)

    # Remove unnecessary columns
    df = df.drop(columns=drop_featurs)

    X = df.drop(columns=["loan_status"])
    y = df["loan_status"]

    # Split BEFORE preprocessing
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # Fit only on training data
    X_train_processed = preprocessor.fit_transform(X_train)

    # Transform test data using train statistics
    X_test_processed = preprocessor.transform(X_test)

    # Convert to DataFrames for easier inspection
    feature_names = preprocessor.get_feature_names_out()

    X_train_processed_df = pd.DataFrame(
        X_train_processed,
        columns=feature_names,
    )

    X_test_processed_df = pd.DataFrame(
        X_test_processed,
        columns=feature_names,
    )

    # Save preprocessor
    joblib.dump(preprocessor, preprocessor_path)

    print("\nProcessed Training Data")
    print(X_train_processed_df.head())

    print("\nProcessed Testing Data")
    print(X_test_processed_df.head())

    print("\nFeature Names")
    print(feature_names)

    return (
        X_train_processed_df,
        X_test_processed_df,
        y_train,
        y_test,
    )    

def train_model(
    X_train,
    X_test,
    y_train,
    y_test,
):
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            random_state=42
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            random_state=42
        ),
        "AdaBoost": AdaBoostClassifier(
            random_state=42
        ),
        "KNN": KNeighborsClassifier(
            n_neighbors=5
        ),
        "SVM": SVC(
            kernel="rbf",
            probability=True,
            random_state=42
        ),
    }

    results = []

    for model_name, model in models.items():

        print(f"\n{'='*60}")
        print(f"Training: {model_name}")
        print(f"{'='*60}")

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(
            y_test,
            y_pred,
            pos_label="Approved"
        )
        recall = recall_score(
            y_test,
            y_pred,
            pos_label="Approved"
        )
        f1 = f1_score(
            y_test,
            y_pred,
            pos_label="Approved"
        )

        cm = confusion_matrix(y_test, y_pred)

        print("Confusion Matrix")
        print(cm)

        print(f"Accuracy : {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall   : {recall:.4f}")
        print(f"F1 Score : {f1:.4f}")

        results.append({
            "Model": model_name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1": f1,
        })

    results_df = pd.DataFrame(results)

    print("\n")
    print("=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)

    print(
        results_df.sort_values(
            by="F1",
            ascending=False
        )
    )

    best_model = results_df.sort_values(
        by="F1",
        ascending=False
    ).iloc[0]

    print("\nBest Model")
    print(best_model)

    return results_df


if __name__ == "__main__":
    
    raw_file_path = "./raw.csv"
    
    X_train_processed_file_path = "./X_train_processed.pkl"
    X_test_processed_file_path = "./X_test_processed.csv"

    y_train_processed_file_path = "./y_train_processed.csv"
    y_test_processed_file_path = "./y_test_processed.csv"

    xt, xt, yt, yt = preprocess_data(raw_file_path, X_train_processed_file_path)
    
    train_model(xt, xt, yt, yt)
    
    
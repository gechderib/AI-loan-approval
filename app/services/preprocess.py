import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

from app.config.env_config import EnvConfig

env_config = EnvConfig()


def preprocess_data(raw_data_path):
    
    # low importance features
    low_importance_features = [
        "Secured_by",
        "Security_Type",
        "construction_type",
        "open_credit"
    ]
        
    # features tha need to be dropped cause the are not important and some of them leak the answere
    drop_features = ["ID", "year", "total_units", "Interest_rate_spread", "Upfront_charges", "rate_of_interest", "credit_type"] + low_importance_features
    
    # nominal features used to to have their own column for each type like gender_femal, gender_male ...
    nominal_features = ["loan_type", "loan_purpose", "occupancy_type", "Region", "Gender", "loan_limit", "approv_in_adv", 
                        "Credit_Worthiness", "business_or_commercial", "Neg_ammortization", "interest_only", 
                        "lump_sum_payment", "co_applicant_credit_type", "submission_of_application"]
    
    # numeric features 
    numeric_features = ["loan_amount", "term", "property_value", "income", "Credit_Score", "LTV", "dtir1"]
    
    # Ordinar features
    ordinar_features = ["age"]
    age_order = ["<25", "25-34", "35-44", "45-54", "55-64", "65-74", ">74"]
    
    print(f"The number of columen used to train: {len(nominal_features) + len(numeric_features) + len(ordinar_features)}")
    # pipelines
    nominal_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])
    
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("encoder", StandardScaler())
    ])
    
    order_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OrdinalEncoder(categories=[age_order]))

    ])
    
    # columntransformer
    
    preprocessor = ColumnTransformer([
        ("nom", nominal_pipeline, nominal_features),
        ("num", numeric_pipeline, numeric_features),
        ('ord', order_pipeline, ordinar_features)
    ])
    
    df = pd.read_csv(raw_data_path)
    df = df.drop(columns=drop_features)
    df.rename(columns={"co-applicant_credit_type": "co_applicant_credit_type"}, inplace=True)
    
    X = df.drop(columns=["Status"])
    y = df["Status"]
    
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
    
    # Save preprocessor
    feature_names = preprocessor.get_feature_names_out()

    # Convert to DataFrame
    X_train_processed_df = pd.DataFrame(
        X_train_processed,
        columns=feature_names
    )

    X_test_processed_df = pd.DataFrame(
        X_test_processed,
        columns=feature_names
    )

    joblib.dump(preprocessor, env_config.PREPROCESSOR_PATH)

    # just to save and see the processed data in csv fomat for testing purpose 
    save_preprocessed_for_testing(X_train_processed_df, X_test_processed_df)
    
    return (X_train_processed_df, X_test_processed_df, y_train, y_test)

    


def save_preprocessed_for_testing(X_train_processed_df, X_test_processed_df):
    
    # Save
    X_train_processed_df.to_csv(
        env_config.PROCESSED_DATA_TRAIN_PATH,
        index=False
    )

    X_test_processed_df.to_csv(
        env_config.PROCESSED_DATA_TEST_PATH,
        index=False
    )
        
    
if __name__ == "__main__":
    preprocess_data(env_config.RAW_DATA_PATH)
    

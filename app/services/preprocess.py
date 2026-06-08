import pandas as pd

from app.config.env_config import EnvConfig

env_config = EnvConfig()

def apply_mappings(df: pd.DataFrame, mappings: dict) -> pd.DataFrame:

    df = df.copy()

    # for col, mapping in mappings.items():
    #     if col in df.columns:
    #         df[col] = df[col].fillna(df[col].mode()[0]).map(mapping)

    for col, mapping in mappings.items():
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mode()[0])


    return df

def get_mappings():
    return {
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
    }


def preprocess_data(raw_file_path, processed_file_path):
    try:
        df = pd.read_csv(raw_file_path)

        # fill numeric missing values
        num_cols = ["property_value", "income", "LTV", "dtir1"]

        for col in num_cols:
            df[col].fillna(df[col].median(), inplace=True)

        df["term"].fillna(df["term"].mode()[0], inplace=True)

        # drop useless columns
        df.drop(columns=["ID", "year", "total_units", "Interest_rate_spread", "Upfront_charges", "rate_of_interest", "credit_type"], inplace=True)

        # rename fix
        df.rename(columns={"co-applicant_credit_type": "co_applicant_credit_type"}, inplace=True)

        # apply mappings (🔥 ONE LINE POWER)
        df = apply_mappings(df, get_mappings())

        # categorical handling
        one_hot_encoding_columns = [
            "loan_type", "loan_purpose", "occupancy_type", "Region", "Gender"
        ]

        for col in one_hot_encoding_columns:
            df[col].fillna(df[col].mode()[0], inplace=True)

        # ordinal encoding (age)
        age_order = ["<25", "25-34", "35-44", "45-54", "55-64", "65-74", ">74"]
        df["age"] = df["age"].fillna(df["age"].mode()[0])
        # df["age"] = pd.Categorical(df["age"], categories=age_order, ordered=True).codes

        df.to_csv(processed_file_path, index=False)
        print(f"Saved: {processed_file_path}")

    except Exception as e:
        print(f"Preprocessing error: {e}")
        
        
if __name__ == "__main__":
    file_path_test = env_config.RAW_DATA_TEST_PATH
    file_path_train = env_config.RAW_DATA_TRAIN_PATH

    preprocess_data(file_path_test, env_config.PROCESSED_DATA_TEST_PATH)
    preprocess_data(file_path_train, env_config.PROCESSED_DATA_TRAIN_PATH)
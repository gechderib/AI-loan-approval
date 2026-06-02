import pandas as pd




from app.config.env_config import EnvConfig

env_config = EnvConfig()


def preprocess_data(raw_file_path, processed_file_path):
 try:
  print(f"Preprocessing data from: {raw_file_path}")
  df = pd.read_csv(raw_file_path)
  print("Data loaded successfully.")
  print("Performing basic preprocessing steps...")

  # 1. Handle missing values
  df["rate_of_interest"].fillna(df["rate_of_interest"].median(), inplace=True)
  df["Interest_rate_spread"].fillna(df["Interest_rate_spread"].median(), inplace=True)
  df["Upfront_charges"].fillna(df["Upfront_charges"].median(), inplace=True)
  df["property_value"].fillna(df["property_value"].median(), inplace=True)
  df["income"].fillna(df["income"].median(), inplace=True)
  df["LTV"].fillna(df["LTV"].median(), inplace=True)
  df["dtir1"].fillna(df["dtir1"].median(), inplace=True)
  df["term"].fillna(df["term"].mode()[0], inplace=True)
  
  # 2. Drop unnecessary columns
  df.drop(columns=["ID", "year","total_units"], inplace=True)
  
  loan_limit_map = {
      "cf": 1,
      "ncf": 0,
  }
  approv_in_adv_map = {
      "nopre": 0,
      "pre": 1,
  }
  Credit_Worthiness_map = {
      "l1": 1,
      "l2": 0,
  }
  open_credit_map = {
      "nopc": 0, 
      "opc": 1,
  }
  business_or_commercial_map = {
      "nob/c": 0,
      "b/c": 1,
  }
  Neg_ammortization_map = {
      "not_neg": 0,
      "neg_amm": 1,
  }
  interest_only_map = {
      "not_int": 0,
      "int_only": 1,
  }
  lump_sum_payment_map = {
      "not_lpsm": 0,
      "lpsm": 1,
  }
  construction_type_map = {
      "sb": 0,
      "mh": 1,
  }
  
  
  secured_by_map = {
      "home": 0,
      "land": 1,
  }
    
  co_applicant_credit_type_map = {
      "CIB": 0,
      "EXP": 1,
  }
  
  submission_of_application_map = {
      "to_inst": 1,
      "not_inst": 0,
  }
  
  Security_Type_map = {
      "direct": 0,
      "Indriect": 1,
  }
  
  # 3. Handle categorical variables (example: fill missing values with mode)

  df["loan_limit"] = df["loan_limit"].fillna(df["loan_limit"].mode()[0]).map(loan_limit_map)
  df["approv_in_adv"] = df["approv_in_adv"].fillna(df["approv_in_adv"].mode()[0]).map(approv_in_adv_map)
  df["Credit_Worthiness"] = df["Credit_Worthiness"].fillna(df["Credit_Worthiness"].mode()[0]).map(Credit_Worthiness_map)
  df["open_credit"] = df["open_credit"].fillna(df["open_credit"].mode()[0]).map(open_credit_map)
  df["business_or_commercial"] = df["business_or_commercial"].fillna(df["business_or_commercial"].mode()[0]).map(business_or_commercial_map)
  df["Neg_ammortization"] = df["Neg_ammortization"].fillna(df["Neg_ammortization"].mode()[0]).map(Neg_ammortization_map)
  df["interest_only"] = df["interest_only"].fillna(df["interest_only"].mode()[0]).map(interest_only_map)
  df["lump_sum_payment"] = df["lump_sum_payment"].fillna(df["lump_sum_payment"].mode()[0]).map(lump_sum_payment_map)
  df["construction_type"] = df["construction_type"].fillna(df["construction_type"].mode()[0]).map(construction_type_map)
  df["Secured_by"] = df["Secured_by"].fillna(df["Secured_by"].mode()[0]).map(secured_by_map)
  df["co-applicant_credit_type"] = df["co-applicant_credit_type"].fillna(df["co-applicant_credit_type"].mode()[0]).map(co_applicant_credit_type_map)
  df["submission_of_application"] = df["submission_of_application"].fillna(df["submission_of_application"].mode()[0]).map(submission_of_application_map)
  df["Security_Type"] = df["Security_Type"].fillna(df["Security_Type"].mode()[0]).map(Security_Type_map)
  
  # use one hot encoding for the below columns and fill missing values with mode before one hot encoding  
  one_hot_encoding_columns = ["loan_type", "loan_purpose", "occupancy_type", "credit_type", "Region","Gender"]
  for col in one_hot_encoding_columns:
      df[col].fillna(df[col].mode()[0], inplace=True)
  df = pd.get_dummies(df, columns=one_hot_encoding_columns, dummy_na=False, dtype=int)
  
  # use ordinal encoding for the below column and fill missing values with mode before ordinal encoding
  ordinal_categorical_columns = ["age"]
  age_order = ["<25", "25-34", "35-44", "45-54", "55-64", "65-74", ">74"]
  for col in ordinal_categorical_columns:
      df[col].fillna(df[col].mode()[0], inplace=True)
      df[col] = pd.Categorical(df[col], categories=age_order, ordered=True).codes
          
  # Save the preprocessed data to a new CSV file
  df.to_csv(processed_file_path, index=False)
  print(f"Preprocessed data saved to: {processed_file_path}")
  
  
  
 except Exception as e:
  print(f"An error occurred during preprocessing: {e}")
  
if __name__ == "__main__":
    file_path_test = env_config.RAW_DATA_TEST_PATH
    file_path_train = env_config.RAW_DATA_TRAIN_PATH
    
    preprocess_data(file_path_test, env_config.PROCESSED_DATA_TEST_PATH)
    preprocess_data(file_path_train, env_config.PROCESSED_DATA_TRAIN_PATH)
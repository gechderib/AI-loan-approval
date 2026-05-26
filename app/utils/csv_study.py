import pandas as pd
import json
from app.config.env_config import EnvConfig

env_config = EnvConfig()


def get_csv_column_names(file_path) -> list:
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Get the column names from the DataFrame
        column_names = df.columns.tolist()
        return column_names
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
       
       
       
def read_csv_and_get_unique_values(file_path, column_names) -> str:
    try:
        # Read CSV
        df = pd.read_csv(file_path)

        # Validate columns
        for column_name in column_names:
            if column_name not in df.columns:
                raise ValueError(
                    f"Column '{column_name}' does not exist in the CSV file."
                )

        # Build dictionary
        unique_values = {}

        for column_name in column_names:
            values = []

            for value in df[column_name].unique().tolist():
                # Convert NaN to None (valid JSON null)
                if pd.isna(value):
                    values.append(None)
                else:
                    values.append(value)

            unique_values[column_name] = values

        # Return valid JSON
        return json.dumps(unique_values, indent=4)

    except Exception as e:
        print(f"An error occurred: {e}")
        return json.dumps({})



if __name__ == "__main__":
    file_path = env_config.RAW_DATA_PATH
    column_names = get_csv_column_names(file_path)
    # print(column_names)
    column_names = [
     "year",
     "loan_limit",
     "Gender",
     "approv_in_adv",
     "loan_type",
     "loan_purpose",
     "Credit_Worthiness",
     "open_credit",
     "business_or_commercial",
     "Neg_ammortization",
     "interest_only",
     "lump_sum_payment",
     "construction_type",
     "occupancy_type",
     "Secured_by",
     "total_units",
     "credit_type",
     "co-applicant_credit_type",
     "submission_of_application",
     "Region",
     "Security_Type",
     "age",
    ]
    unique_values = read_csv_and_get_unique_values(file_path, column_names)
    print(unique_values)
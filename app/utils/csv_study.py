import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

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


#  each column data dirstibution percntage like Gender male 40%, female 45%, joint 10% and null value 5%
def read_csv_and_get_column_distribution(file_path, column_names) -> str:
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
        distribution = {}

        for column_name in column_names:
            value_counts = df[column_name].value_counts(dropna=False)
            total_count = len(df)

            distribution[column_name] = {
                str(value): f"{(count / total_count) * 100:.2f}%"
                for value, count in value_counts.items()
            }

        # Return valid JSON
        return json.dumps(distribution, indent=4)

    except Exception as e:
        print(f"An error occurred: {e}")
        return json.dumps({})

# drawing using matplotlib and seaborn for each column distribution

def draw_column_distribution(file_path, column_names):

    try:
        # Read CSV
        df = pd.read_csv(file_path)

        # Validate columns
        for column_name in column_names:
            if column_name not in df.columns:
                raise ValueError(
                    f"Column '{column_name}' does not exist in the CSV file."
                )

        # Draw distribution for each column
        for column_name in column_names:
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, x=column_name)
            plt.title(f"Distribution of {column_name}")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    file_path = env_config.RAW_DATA_PATH
    column_names = get_csv_column_names(file_path)
    # print(column_names)
    column_names = [
    #  "year",
    #  "loan_limit",
    #  "Gender",
    #  "approv_in_adv",
    #  "loan_type",
    #  "loan_purpose",
    #  "Credit_Worthiness",
    #  "open_credit",
    #  "business_or_commercial",
    #  "Neg_ammortization",
    #  "interest_only",
    #  "lump_sum_payment",
    #  "construction_type",
    #  "occupancy_type",
    #  "Secured_by",
    #  "total_units",
    #  "credit_type",
    #  "co-applicant_credit_type",
    #  "submission_of_application",
     "Region",
     "Security_Type",
     "age",
    ]
    unique_values = read_csv_and_get_unique_values(file_path, column_names)
    print(unique_values)
    
    distribution = read_csv_and_get_column_distribution(file_path, column_names)
    print(distribution)
    
    draw_column_distribution(file_path, column_names)
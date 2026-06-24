import pandas as pd
import json
import matplotlib
# for ubuntu and debian users use 'TkAgg' backend, for windows and macOS users use 'Agg' backend the default no need to impor tk
matplotlib.use('TkAgg')
import tkinter as tk
# the above two
from pathlib import Path
from datetime import datetime


import matplotlib.pyplot as plt


import seaborn as sns

from app.config.env_config import EnvConfig

env_config = EnvConfig()


def get_csv_column_names(file_path) -> list:
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        # print(df.head())
        # print(df.info())
        print(df["dtir1"].describe())
        print((df["dtir1"] == 0).sum())
        print(df["dtir1"].median())
        # print(df.dtypes)
        # print(df.isnull().sum())
        # print(df.nunique())
        # print(df.columns)
        # print(df.shape)
        # print(df.columns.tolist())
        # Get the column names from the DataFrame
        column_names = df.columns.tolist()
        return column_names
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
       
       
def visualize_unique_values(file_path, column_name):
    print(plt.get_backend())
    df = pd.read_csv(file_path)
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x=column_name)
    plt.title(f"Unique Values in Column: {column_name}")
    plt.xlabel(column_name)
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

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



def plot_status_percentage_for_columns(
    file_path,
    column_names,
    target_column="Status"
):
    try:
        df = pd.read_csv(file_path)

        output_dir = Path("charts")
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for column_name in column_names:

            if column_name not in df.columns:
                print(f"Skipping '{column_name}' - column not found")
                continue

            cross_tab = (
                pd.crosstab(
                    df[column_name],
                    df[target_column],
                    normalize="index"
                ) * 100
            )

            plt.figure(figsize=(10, 6))

            ax = cross_tab.plot(
                kind="bar",
                stacked=True,
                figsize=(10, 6)
            )

            plt.title(
                f"{target_column} Distribution by {column_name}"
            )
            plt.xlabel(column_name)
            plt.ylabel("Percentage")
            plt.legend(title=target_column)
            plt.xticks(rotation=45)
            plt.tight_layout()

            file_name = (
                output_dir
                / f"{column_name}_{timestamp}.png"
            )
            plt.show()
            plt.savefig(file_name, bbox_inches="tight")
            plt.close()

            print(f"Saved: {file_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

def pie_for_none_vs_not_none(file_path, column_names):
    try:
        df = pd.read_csv(file_path)
        for column_name in column_names:
            none_count = df[column_name].isna().sum()
            not_none_count = df[column_name].notna().sum()

            labels = ["None", "Not None"]
            sizes = [none_count, not_none_count]
            colors = ["#ff9999", "#66b3ff"]

            plt.figure(figsize=(6, 6))
            plt.pie(
                sizes,
                labels=labels,
                colors=colors,
                autopct="%1.1f%%",
                startangle=140
            )
            plt.title(f"None vs Not None for {column_name}")
            plt.axis("equal")
            plt.tight_layout()
            plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")  
    
def raw_data_count(df):

    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Column names: {df.columns.tolist()}")
if __name__ == "__main__":
    file_path = env_config.RAW_DATA_PATH
    
    df = pd.read_csv(file_path)
    raw_data_count(df)
    column_names = [
    #  "ID",                          # drop the column
    #  "year",                        # drop the column
       
    #  "loan_type", 
    #  "loan_purpose", 
    #  "occupancy_type", 
    #  "credit_type", 
    #  "Region",
    #  "Gender",
    
    #  "loan_limit",                  # use mode for missing values maybe drop the column
    #  "approv_in_adv",               # use the mode
    #  "Credit_Worthiness",           # use the value as it l1 or l2 95.74% is l1
    #  "open_credit",                 # use the value as it 99.67 is nopc drop
    #  "business_or_commercial",      # use as is mode mode for missing values
    #  "Neg_ammortization",           # use as is mode for missing values
    #  "interest_only",               # use as is mode for missing values
    #  "lump_sum_payment",            # use as is mode for missing values
    #  "construction_type",           # use as is mode for missing values
    #  "Secured_by",                  # use as is mode for missing values
    #  "total_units",                 # drop the column
    #  "co_applicant_credit_type",    # use as is mode for missing values 
    #  "submission_of_application",   # use as is mode for missing values
    #  "Security_Type",               # use as is or drop the column
    #  "age",                         # use as is mode for missing values
                                      
    #  "loan_amount",                 # all value available use as is
    #  "rate_of_interest",            # 75 % data available use as is fillna with median
    #  "Interest_rate_spread",        # 75 % data available use as is fillna with median
    #  "Upfront_charges",             # 73 % data available use as is fillna with median
    #  "term",                        # all value available use as is
    #  "property_value",              # 89.8% data available use as is fillna with median
    #  "income",                      # 93.8% data available use as is fillna with median
    #  "Credit_Score",                # all value available use as is
    #  "LTV",                         # 89.8% data available use as is fillna with median
    #  "Status",                      # all value available use as is
    #  "dtir1",                       # 83.8% data available use as is fillna with median
    ]    
    # print("Visualizing unique values for the 'loan_type' column:")
    # visualize_unique_values(file_path, "loan_type")
    
    # ####### for a column that can be an enum ---------------
    # distribution = read_csv_and_get_column_distribution(file_path, column_names)
    # print(distribution)
    
    # to now echa column type effect on the status
    # plot_status_percentage_for_columns(file_path, column_names, "Status")
    
    # draw_column_distribution(file_path, column_names)
    
    # pie_for_none_vs_not_none(file_path, column_names)


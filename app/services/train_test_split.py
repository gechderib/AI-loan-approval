from sklearn.model_selection import train_test_split
import pandas as pd
from app.config.env_config import EnvConfig

env_config = EnvConfig()


def raw_train_test_split(file_path, test_size=0.2, random_state=42):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Split the DataFrame into training and testing sets
        train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
        
        # Save the training and testing sets to new CSV files
        train_df.to_csv(env_config.RAW_DATA_TRAIN_PATH, index=False)
        test_df.to_csv(env_config.RAW_DATA_TEST_PATH, index=False)
        
        print(f"Data successfully split into training and testing sets.")
        print(f"Training set saved to: {env_config.RAW_DATA_TRAIN_PATH}")
        print(f"Testing set saved to: {env_config.RAW_DATA_TEST_PATH}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    file_path = env_config.RAW_DATA_PATH
    raw_train_test_split(file_path)
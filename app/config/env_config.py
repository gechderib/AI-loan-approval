from dotenv import load_dotenv
import os

class EnvConfig:
    ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8007
    
    RAW_DATA_PATH: str = "./data/raw/loan_data.csv"
    RAW_DATA_TEST_PATH: str = "./data/raw/loan_test_data.csv"
    RAW_DATA_TRAIN_PATH: str = "./data/raw/loan_train_data.csv"
    
    PROCESSED_DATA_TEST_PATH: str = "./data/processed/loan_test_data.csv"
    PROCESSED_DATA_TRAIN_PATH: str = "./data/processed/loan_train_data.csv"
    
    PREPROCESSOR_PATH: str = "./data/processed/loan_preprocessor.pkl"
    
    MODEL_PATH: str = "./models/loan_approval_model"
    FEATURE_COLUMNS_PATH :str = "./models/feature_columns.pkl"
    THRESHOLD_PATH: str = "models/threshold.pkl"
    def __init__(self):
        
        load_dotenv()
        
        self.ENV = os.getenv("ENV", self.ENV)
        self.DEBUG = os.getenv("DEBUG", str(self.DEBUG)).lower() in ("true", "1", "t")
        self.PORT = int(os.getenv("PORT", self.PORT))
                
        self.RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", self.RAW_DATA_PATH)
        self.RAW_DATA_TEST_PATH = os.getenv("RAW_DATA_TEST_PATH", self.RAW_DATA_TEST_PATH)
        self.RAW_DATA_TRAIN_PATH = os.getenv("RAW_DATA_TRAIN_PATH", self.RAW_DATA_TRAIN_PATH)
        
        self.PROCESSED_DATA_TEST_PATH = os.getenv("PROCESSED_DATA_TEST_PATH", self.PROCESSED_DATA_TEST_PATH)
        self.PROCESSED_DATA_TRAIN_PATH = os.getenv("PROCESSED_DATA_TRAIN_PATH", self.PROCESSED_DATA_TRAIN_PATH)
        
        self.MODEL_PATH = os.getenv("MODEL_PATH", self.MODEL_PATH)
        self.FEATURE_COLUMNS_PATH = os.getenv("FEATURE_COLUMNS_PATH", self.FEATURE_COLUMNS_PATH)
        self.THRESHOLD_PATH = os.getenv("THRESHOLD_PATH", self.THRESHOLD_PATH)
        
        self.PREPROCESSOR_PATH = os.getenv("PREPROCESSOR_PATH", self.PREPROCESSOR_PATH)
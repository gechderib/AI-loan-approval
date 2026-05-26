from dotenv import load_dotenv
import os

class EnvConfig:
    ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8007
    RAW_DATA_PATH: str = "./data/raw/loan_data.csv"
    RAW_DATA_TEST_PATH: str = "./data/raw/loan_test_data.csv"
    RAW_DATA_TRAIN_PATH: str = "./data/raw/loan_train_data.csv"
    

    def __init__(self):
        
        load_dotenv()
        
        self.ENV = os.getenv("ENV", self.ENV)
        self.DEBUG = os.getenv("DEBUG", str(self.DEBUG)).lower() in ("true", "1", "t")
        self.PORT = int(os.getenv("PORT", self.PORT))
        
        self.RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", self.RAW_DATA_PATH)
        self.RAW_DATA_TEST_PATH = os.getenv("RAW_DATA_TEST_PATH", self.RAW_DATA_TEST_PATH)
        self.RAW_DATA_TRAIN_PATH = os.getenv("RAW_DATA_TRAIN_PATH", self.RAW_DATA_TRAIN_PATH)
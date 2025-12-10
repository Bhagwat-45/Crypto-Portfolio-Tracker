from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Settings():
    database_url: str = os.getenv("DATABASE_URL")

    def __post__init__(self):
        if not self.database_url:
            raise ValueError("The Database URL was not set!")
        
settings = Settings()


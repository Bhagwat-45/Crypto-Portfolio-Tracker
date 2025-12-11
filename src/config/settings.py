from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Settings():
    database_url: str = os.getenv("DATABASE_URL")
    api_url : str = os.getenv("API_URL")
    route : str = os.getenv("ROUTE")
    api_key : str = os.getenv("API_KEY")

    def __post__init__(self):
        if not self.database_url:
            raise ValueError("The Database URL was not set!")
        if not self.api_url:
            raise ValueError("The API URL was not set!")
        if not self.route:
            raise ValueError("The Route was not set!")
        if not self.api_key:
            raise ValueError("The API Key was not set!")
        
    endpoint : str = f"{api_url}{route}"
        
settings = Settings()



import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    login_url: str
    email: str
    password: str
    api_token: str

    @classmethod
    def from_env(cls):
        return cls(
            base_url=os.getenv("BASE_URL"),
            login_url=os.getenv("BASE_APP_URL"),
            email=os.getenv("EMAIL"),
            password=os.getenv("PASSWORD"),
            api_token=os.getenv("API_TOKEN", "")
        )

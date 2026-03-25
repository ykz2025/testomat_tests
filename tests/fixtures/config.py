import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    app_base_url: str
    email: str
    password: str


@pytest.fixture(scope="session")
def configs() -> Config:
    return Config(
        base_url=os.getenv("BASE_URL"),
        app_base_url=os.getenv("BASE_APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
    )

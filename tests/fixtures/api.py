from typing import Any, Generator

import pytest

from src.api.client import TestomatAPI
from tests.fixtures.config import Config


@pytest.fixture(scope="session")
def api_client(configs: Config) -> Generator[TestomatAPI, Any, None]:
    client = TestomatAPI(
        base_url=configs.app_base_url,
        api_token=configs.api_token,
    )
    client.login()
    yield client
    client.session.close()

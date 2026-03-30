from pathlib import Path

import pytest

# Project root: tests/conftest.py is always 1 level deep
PROJECT_ROOT = Path(__file__).parent.parent
TEST_RESULT_DIR = PROJECT_ROOT / "test-result"


def pytest_configure(config: pytest.Config) -> None:
    """Set report path to always be in project root."""
    if config.option.htmlpath:
        config.option.htmlpath = str(TEST_RESULT_DIR / "report.html")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    """Store test result on the item for fixture access."""
    outcome = yield
    rep = outcome.get_result()
    # Store each phase result: rep_setup, rep_call, rep_teardown
    setattr(item, f"rep_{rep.when}", rep)


pytest_plugins = [
    "tests.fixtures.config",
    "tests.fixtures.playwright",
    "tests.fixtures.app",
    "tests.fixtures.api",
]

from typing import Any, Generator

import pytest
from playwright.sync_api import Page, Browser, BrowserContext, Playwright

from src.config import Config
from src.web import App


@pytest.fixture(scope="session")
def config():
    return Config.from_env()


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "channel": "chrome",
        "headless": False,
        "slow_mo": 150,
        "timeout": 30000,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": "https://app.testomat.io",
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "videos/",
        "permissions": ["geolocation"],
    }


@pytest.fixture(scope="session")
def browser(playwright: Playwright, browser_type_launch_args: dict) -> Generator[Browser, Any, None]:
    browser = playwright.chromium.launch(**browser_type_launch_args)
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def context(browser: Browser, browser_context_args: dict) -> Generator[BrowserContext, Any, None]:
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, Any, None]:
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def app(page: Page) -> App:
    return App(page)


@pytest.fixture(scope="session")
def auth_context(browser: Browser, browser_context_args: dict, config: Config) -> Generator[BrowserContext, Any, None]:
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    app = App(page)

    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login(config.email, config.password)
    app.projects_page.is_loaded()

    page.close()
    yield context
    context.close()


@pytest.fixture(scope="function")
def auth_page(auth_context: BrowserContext) -> Generator[Page, Any, None]:
    page = auth_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def logged_app(auth_page: Page) -> App:
    return App(auth_page)


@pytest.fixture(scope="function")
def login(app: App, config: Config):
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login(config.email, config.password)

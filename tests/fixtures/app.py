import json
from pathlib import Path
from typing import Any, Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect

from src.web.app import App
from tests.conftest import TEST_RESULT_DIR
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import CookieHelper

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")
FREE_PROJECT_STORAGE_PATH = Path("test-result/.auth/free_project_state.json")
TRACES_DIR = TEST_RESULT_DIR / "traces"


def get_or_create_context(
    browser: Browser,
    base_url: str,
    storage_path: Path,
) -> tuple[BrowserContext, bool]:
    """
    Returns context and flag indicating if login is needed.
    If storage exists -> load it, no login needed
    If not -> create fresh context, login needed
    """
    has_state = storage_path.exists()

    kwargs = {
        "base_url": base_url,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": str(TEST_RESULT_DIR / "videos"),
        "permissions": ["geolocation"],
    }
    if has_state:
        kwargs["storage_state"] = str(storage_path)

    context = browser.new_context(**kwargs)
    return context, not has_state


def save_storage_state(context: BrowserContext, path: Path) -> None:
    """Save browser state for reuse."""
    path.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=path)


def start_tracing(page: Page) -> None:
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)


def stop_tracing_on_failure(page: Page, request: pytest.FixtureRequest) -> None:
    """Stop tracing and save only if test failed."""
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        trace_path = TRACES_DIR / f"{request.node.name}.zip"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        page.context.tracing.stop(path=trace_path)
    else:
        page.context.tracing.stop()


def create_free_project_state() -> None:
    """Create free project state by copying storage state with empty company_id."""
    if not STORAGE_STATE_PATH.exists():
        return

    state = json.loads(STORAGE_STATE_PATH.read_text())
    for cookie in state.get("cookies", []):
        if cookie.get("name") == "company_id":
            cookie["value"] = ""
            break

    FREE_PROJECT_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FREE_PROJECT_STORAGE_PATH.write_text(json.dumps(obj=state, indent=2))


def build_browser_context(
    browser: Browser,
    base_url: str,
    storage_state: Path | None = None,
) -> BrowserContext:
    kwargs = {
        "base_url": base_url,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "test-result/videos/",
        "permissions": ["geolocation"],
    }
    if storage_state and storage_state.exists():
        kwargs["storage_state"] = str(storage_state)
    return browser.new_context(**kwargs)


@pytest.fixture(scope="function")
def app(browser_instance: Browser, configs) -> Generator[App, None, None]:
    """Clean app - fresh page per test (function scope)."""
    context = build_browser_context(browser_instance, configs.app_base_url)
    page = context.new_page()
    yield App(page)
    page.close()
    context.close()


@pytest.fixture(scope="session")
def logged_page(browser_instance: Browser, configs) -> Generator[Page, Any, None]:
    """Session-scoped: reuses authentication."""
    context, needs_login = get_or_create_context(
        browser_instance, configs.app_base_url, storage_path=STORAGE_STATE_PATH
    )
    page = context.new_page()

    if needs_login:
        open_login_and_authorize(configs, page=page)
        save_storage_state(context, STORAGE_STATE_PATH)
        create_free_project_state()

    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_page: Page, request: pytest.FixtureRequest) -> Generator[App, Any, None]:
    """Function-scoped: tracing per test, saves trace only on failure."""
    start_tracing(logged_page)
    logged_page.goto("/projects")

    yield App(logged_page)

    stop_tracing_on_failure(logged_page, request)


@pytest.fixture(scope="function")
def cookies(logged_page: Page) -> CookieHelper:
    """Provides cookie manipulation helper for the logged-in context."""
    return CookieHelper(logged_page.context)


@pytest.fixture(scope="module")
def shared_browser(browser_instance: Browser, configs) -> Generator[Page, None, None]:
    """Shared page for parametrized tests (module scope) - reuses same page across test params."""
    context, _ = get_or_create_context(browser_instance, configs.app_base_url, storage_path=STORAGE_STATE_PATH)
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def shared_page(shared_browser: Page) -> Generator[App, None, None]:
    """Shared page with state clearing between tests."""
    yield App(shared_browser)
    CookieHelper.clear_browser_state(shared_browser)


@pytest.fixture(scope="session")
def free_project_page(logged_page: BrowserContext, browser_instance: Browser, configs) -> Generator[Page, Any, None]:
    if FREE_PROJECT_STORAGE_PATH.exists():
        context = build_browser_context(browser_instance, configs.app_base_url, storage_state=FREE_PROJECT_STORAGE_PATH)
        yield context.new_page()
        context.close()
        return

    context = build_browser_context(browser_instance, configs.app_base_url)
    page = context.new_page()
    app = App(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)

    app.projects_page.is_loaded()
    app.projects_page.open()
    app.projects_page.header.select_company("Free Projects")
    expect(app.projects_page.header.free_plan_label).to_be_visible()

    FREE_PROJECT_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=FREE_PROJECT_STORAGE_PATH)

    yield page
    context.close()


def open_login_and_authorize(configs: Config, page: Page) -> App:
    app = App(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    return app


@pytest.fixture(scope="function")
def free_project_app(free_project_page: Page, request: pytest.FixtureRequest) -> Generator[App, Any, None]:
    """Function-scoped: tracing per test, saves trace only on failure."""
    start_tracing(free_project_page)
    free_project_page.goto("/projects")

    yield App(free_project_page)

    stop_tracing_on_failure(free_project_page, request)

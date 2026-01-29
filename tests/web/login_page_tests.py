from faker import Faker
from playwright.sync_api import Page

from src.web.pages.App import App
from tests.conftest import Config


def test_login_page(page: Page, configs: Config, app: App):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(configs.email, Faker().password(length=10))
    app.login_page.invalid_login_message_visible()


def test_login_with_valid_creds(page: Page, configs: Config, app: App):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(configs.email, configs.password)

    app.projects_page.is_loaded()

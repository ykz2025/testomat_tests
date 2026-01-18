from faker import Faker
from playwright.sync_api import Page

from src.web.pages.LoginPage import LoginPage
from src.web.pages.homePage import HomePage
from tests.conftest import Config


def test_login_page(page: Page, configs: Config):
    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page = LoginPage(page)
    login_page.is_loaded()
    login_page.login(configs.email, Faker().password(length=10))
    login_page.invalid_login_message_visible()

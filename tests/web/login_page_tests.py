import pytest
from faker import Faker

from src.config import Config
from src.web import App

fake = Faker()
LOGIN_ATTEMPT_COOLDOWN_MS = 1500

INVALID_LOGIN_PARAMS = [
    ("valid", "invalid"),
    ("invalid", "valid"),
    ("invalid", "invalid"),
    ("empty", "valid"),
    ("valid", "empty"),
    ("valid", "short"),
    ("valid", "long"),
    ("sql_injection", "valid"),
    ("valid", "sql_injection"),
    ("xss", "valid"),
    ("valid", "xss")
]


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize("email_condition, password_condition", INVALID_LOGIN_PARAMS)
def test_login_invalid(app: App, config: Config, email_condition, password_condition):
    if email_condition == "valid":
        email = config.email
    elif email_condition == "invalid":
        email = fake.email()
    elif email_condition == "empty":
        email = ""
    elif email_condition == "sql_injection":
        email = '"\' OR \'1\'=\'1"@example.com'
    elif email_condition == "xss":
        email = '"<script>alert(\'XSS\')</script>"@example.com'
    else:
        email = fake.email()

    if password_condition == "valid":
        password = config.password
    elif password_condition == "invalid":
        password = fake.password()
    elif password_condition == "empty":
        password = ""
    elif password_condition == "short":
        password = fake.pystr(min_chars=6, max_chars=6)
    elif password_condition == "long":
        password = fake.pystr(min_chars=50, max_chars=50)
    elif password_condition == "sql_injection":
        password = "' OR '1'='1"
    elif password_condition == "xss":
        password = "<script>alert('XSS')</script>"
    else:
        password = fake.password()

    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(email, password)

    app.login_page.invalid_login_message_visible()
    app.page.wait_for_timeout(LOGIN_ATTEMPT_COOLDOWN_MS)


@pytest.mark.smoke
@pytest.mark.web
def test_login_with_valid_creds(app: App, config: Config):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(config.email, config.password)
    app.page.wait_for_timeout(LOGIN_ATTEMPT_COOLDOWN_MS)

    app.projects_page.is_loaded()

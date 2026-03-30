import pytest
from faker import Faker

from src.config import Config
from src.web import App

fake = Faker()

# Equivalence Class Partitioning & Boundary Value Analysis test data
invalid_login_test_data = [
    # Email Equivalence Classes
    pytest.param(fake.email(), fake.password(length=10), id="unregistered_valid_email"),
    pytest.param(fake.user_name(), fake.password(length=10), id="email_missing_at_symbol"),
    pytest.param("invalid@", fake.password(length=10), id="email_missing_domain"),
    pytest.param("@domain.com", fake.password(length=10), id="email_missing_local_part"),
    pytest.param("user@@domain.com", fake.password(length=10), id="email_double_at"),
    pytest.param("user name@domain.com", fake.password(length=10), id="email_with_space"),
    # Password Equivalence Classes
    pytest.param(fake.email(), "", id="empty_password"),
    pytest.param(fake.email(), "  ", id="password_only_spaces"),
    pytest.param(fake.email(), "ab", id="password_2_chars"),
    pytest.param(fake.email(), "a" * 256, id="password_256_chars"),
    # Boundary Value Analysis - Empty inputs
    pytest.param("", "", id="both_empty"),
    pytest.param("", fake.password(length=10), id="empty_email"),
    # Boundary Value Analysis - Min/Max lengths
    pytest.param("a@b.c", fake.password(length=10), id="min_valid_email_form"),
    pytest.param(f"{'a' * 64}@{'b' * 63}.com", fake.password(length=10), id="max_length_email"),
    # Special Characters
    pytest.param(fake.email(), "pass<script>alert(1)</script>", id="xss_in_password"),
    pytest.param(fake.email(), "pass'; DROP TABLE users;--", id="sql_injection_password"),
]


@pytest.mark.regression
@pytest.mark.web
@pytest.mark.parametrize("email, password", invalid_login_test_data)
def test_login_invalid(shared_page: App, email: str, password: str):
    shared_page.login_page.open()
    shared_page.login_page.is_loaded()
    shared_page.login_page.login_user(email, password)
    shared_page.login_page.invalid_login_message_visible()

    shared_page.page.wait_for_timeout(2000)


@pytest.mark.smoke
@pytest.mark.web
def test_login_with_valid_creds(logged_app: App):
    logged_app.projects_page.is_loaded()

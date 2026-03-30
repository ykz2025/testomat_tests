import pytest

from src.web.app import App
from tests.fixtures.cookie_helper import CookieHelper


@pytest.mark.smoke
@pytest.mark.web
def test_add_feature_flag_cookie(logged_app: App, cookies: CookieHelper):
    logged_app.page.pause()
    """Verify that a feature flag cookie can be added and retrieved."""
    cookies.add("feature_flag", "dark_mode_enabled", "app.testomat.io")

    assert cookies.exists("feature_flag")
    assert cookies.get_value("feature_flag") == "dark_mode_enabled"
    logged_app.page.reload()

    # do some staff


@pytest.mark.web
def test_clear_feature_flag_cookie(logged_app: App, cookies: CookieHelper):
    """Verify that a feature flag cookie can be cleared."""
    cookies.add("feature_flag", "beta_feature", "app.testomat.io")
    assert cookies.exists("feature_flag")

    cookies.clear(name="feature_flag")
    assert not cookies.exists("feature_flag")

    # do some staff

    @pytest.mark.web
    def test_add_multiple_feature_flags(logged_app: App, cookies: CookieHelper):
        """Verify that multiple feature flags cookies can be added."""
        cookies.add("feature_flag", "enabled", "app.testomat.io")
        cookies.add("feature_new_ui", "disabled", "app.testomat.io")

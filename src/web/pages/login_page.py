from typing import Self

from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self) -> Self:
        self.page.goto("/users/sign_in")
        return self

    def is_loaded(self) -> Self:
        expect(self.page.locator("#content-desktop form#new_user")).to_be_visible()
        return self

    def login_user(self, email: str, password: str, remember_me: bool = False) -> Self:
        self.page.locator("#content-desktop #user_email").fill(email)
        self.page.locator("#content-desktop #user_password").fill(password)

        if remember_me:
            self.page.locator("#user_remember_me").check()

        self.page.get_by_role("button", name="Sign in").click()
        return self

    def invalid_login_message_visible(self) -> Self:
        expect(self.page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
        return self

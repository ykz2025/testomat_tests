from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("/users/sign_in")

    def is_loaded(self):
        expect(self.page.locator("#content-desktop #new_user")).to_be_visible()

    def login(self, email: str, password: str):
        self.page.locator("#content-desktop #user_email").fill(email)
        self.page.locator("#content-desktop #user_password").fill(password)
        self.page.get_by_role("button", name='Sign in').click()

    def invalid_login_message_visible(self):
        expect(self.page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()

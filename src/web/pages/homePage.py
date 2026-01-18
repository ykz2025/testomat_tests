from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("https://testomat.io")

    def is_loaded(self):
        expect(self.page.locator("#headerMenuWrapper")).to_be_visible()
        expect(self.page.locator(".side-menu .login-item")).to_have_text("Log in")
        expect(self.page.locator(".side-menu .start-item")).to_have_text("Start for free")

    def click_login(self):
        self.page.get_by_text("Log in", exact=True).click()

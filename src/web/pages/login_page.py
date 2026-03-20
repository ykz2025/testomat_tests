from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("/users/sign_in")

    def is_loaded(self):
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.locator("#content-desktop #new_user")).to_be_visible(timeout=10000)

    def login(self, email: str, password: str, remember_me: bool = False):
        self.page.locator("#content-desktop #user_email").fill(email)
        self.page.locator("#content-desktop #user_password").fill(password)

        if remember_me:
            self.page.locator("#content-desktop #user_remember_me").check()

        self.page.get_by_role("button", name='Sign in').click()

    def invalid_login_message_visible(self):
        self.page.wait_for_function(
            """
            () => {
                const bodyText = document.body?.innerText || "";
                if (bodyText.includes("Invalid Email or password.")) return true;
                if (bodyText.includes("Rate Limit Reached.")) return true;
                if (bodyText.includes("Too Many Requests!")) return true;

                const email = document.querySelector("#content-desktop #user_email");
                const password = document.querySelector("#content-desktop #user_password");
                return Boolean(email?.validationMessage || password?.validationMessage);
            }
            """,
            timeout=10000,
        )

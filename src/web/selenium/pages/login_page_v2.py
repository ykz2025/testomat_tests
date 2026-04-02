from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.web.selenium.core.base_page import BasePage


class LoginPageV2(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @property
    def email_input(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_email")

    @property
    def password_input(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop #user_password")

    @property
    def remember_me_checkbox(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#user_remember_me")

    @property
    def sign_in_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop [value='Sign In']")

    @property
    def success_message(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "#content-desktop .common-flash-success")

    def email_input_visible(self) -> WebElement:
        return self.wait.for_visible((By.CSS_SELECTOR, "#content-desktop #user_email"))

    def sign_in_button_clickable(self) -> WebElement:
        return self.wait.for_clickable((By.CSS_SELECTOR, "#content-desktop [value='Sign In']"))

    def open(self, base_url: str = "") -> Self:
        self.driver.get(f"{base_url}/users/sign_in")
        return self

    def is_loaded(self) -> Self:
        self.email_input_visible()
        return self

    def login(self, email: str, password: str, remember_me: bool = False) -> Self:
        self.email_input.clear()
        self.email_input.send_keys(email)
        self.password_input.clear()
        self.password_input.send_keys(password)

        if remember_me and not self.remember_me_checkbox.is_selected():
            self.remember_me_checkbox.click()
        self.sign_in_button_clickable().click()

        return self

    def should_see_success_message(self) -> Self:
        self.wait.for_visible((By.CSS_SELECTOR, "#content-desktop .common-flash-success"))
        return self

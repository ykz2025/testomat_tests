from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

BySelector = tuple[str, str]
SelectorOrElement = BySelector | WebElement


class Wait:
    DEFAULT_TIMEOUT = 10
    DEFAULT_POLL = 0.2
    IGNORED_EXCEPTIONS = (NoSuchElementException, StaleElementReferenceException)

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self._wait = WebDriverWait(
            driver, timeout, poll_frequency=self.DEFAULT_POLL, ignored_exceptions=self.IGNORED_EXCEPTIONS
        )

    @staticmethod
    def _is_locator(target: SelectorOrElement) -> bool:
        return isinstance(target, tuple) and len(target) == 2

    def for_visible(self, target: SelectorOrElement, custom_timeout: int = None) -> WebElement:
        if custom_timeout:
            self._wait = WebDriverWait(self.driver, custom_timeout, poll_frequency=self.DEFAULT_POLL)
        if self._is_locator(target):
            return self._wait.until(ec.visibility_of_element_located(target))  # type: ignore

        return self._wait.until(ec.visibility_of(target))  # type: ignore

    def for_invisible(self, target: SelectorOrElement) -> bool:
        if self._is_locator(target):
            return self._wait.until(ec.invisibility_of_element_located(target))  # type: ignore

        return self._wait.until(ec.invisibility_of_element(target))  # type: ignore

    def for_present(self, locator: BySelector) -> WebElement:
        return self._wait.until(ec.presence_of_element_located(locator))

    def for_all_present(self, locator: BySelector) -> list[WebElement]:
        return self._wait.until(ec.presence_of_all_elements_located(locator))

    def for_clickable(self, target: SelectorOrElement) -> WebElement:
        if self._is_locator(target):
            return self._wait.until(ec.element_to_be_clickable(target))

        return self._wait.until(ec.element_to_be_clickable(target))

    def for_text_present(self, target: SelectorOrElement, text: str) -> bool:
        if self._is_locator(target):
            return self._wait.until(ec.text_to_be_present_in_element(target, text))  # type: ignore

        return self._wait.until(lambda d: text in target.text)  # type: ignore

    def for_selected(self, target: SelectorOrElement) -> bool:
        if self._is_locator(target):
            return self._wait.until(ec.element_located_to_be_selected(target))  # type: ignore

        return self._wait.until(ec.element_to_be_selected(target))  # type: ignore

    def for_stale(self, element: WebElement) -> bool:
        return self._wait.until(ec.staleness_of(element))

    def for_frame(self, target: SelectorOrElement) -> WebDriver:
        if self._is_locator(target):
            return self._wait.until(ec.frame_to_be_available_and_switch_to_it(target))  # type: ignore

        return self._wait.until(ec.frame_to_be_available_and_switch_to_it(target))  # type: ignore

    def until(self, condition):
        return self._wait.until(condition)

    def until_not(self, condition):
        return self._wait.until_not(condition)

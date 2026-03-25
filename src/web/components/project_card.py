from enum import Enum

from playwright.sync_api import Locator, expect


class Badges(Enum):
    DEMO = "Demo"
    CLASSICAL = "Classical"
    PYTEST = "Pytest"


class ProjectCard:
    def __init__(self, card: Locator):
        self._card = card
        self._link = card
        self._title = card.locator("h3.text-gray-700")
        self._test_count = card.locator("p.text-gray-500.text-sm")
        self._avatars = card.locator("img.rounded-full")
        self._badges = card.locator(".project-badges")

    @property
    def title(self) -> str:
        return self._title.text_content().strip()

    @property
    def test_count(self) -> str:
        return self._test_count.text_content().strip()

    @property
    def href(self) -> str:
        return self._link.get_attribute("href")

    def assert_has_badge(self, expected_badge: Badges):
        expect(self._badges).to_contain_text(expected_badge.value)

    def click(self):
        self._link.click()

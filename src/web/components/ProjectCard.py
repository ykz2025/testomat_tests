from enum import Enum

from playwright.sync_api import Locator, expect


class Badges(Enum):
    Demo = "Demo"
    Classical = "Classical"
    Pytest = "Pytest"


class ProjectCard:

    def __init__(self, card: Locator):
        self.card = card
        self._link = card.locator('a')
        self._title = card.locator('h3.text-gray-700')
        self._test_count = card.locator('p.text-gray-500.text-sm')
        self._avatars = card.locator('img.rounded-full')
        self._badges = card.locator('.project-badges')

    @property
    def title(self) -> str:
        return self._title.text_content().strip()

    @property
    def test_count(self) -> str:
        return self._test_count.text_content().strip()

    @property
    def href(self) -> str:
        return self._link.get_attribute('href')

    def get_badges_has(self, expected_badge: Badges):
        expect(self._badges).to_contain_text(expected_badge.value)

    def click(self):
        self._link.click()

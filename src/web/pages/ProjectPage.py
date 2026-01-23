from typing import Self

from playwright.sync_api import Page, expect


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page

    def is_loaded(self) -> Self:
        expect(self.page.locator(".sticky-header")).to_be_visible()
        expect(self.page.locator(".mainnav-menu")).to_be_visible()
        expect(self.page.locator("[placeholder='First Suite']")).to_be_visible()
        expect(self.page.get_by_role("button", name="Suite")).to_be_visible()
        return self

    def empty_project_name_is(self, expected_project_name: str) -> Self:
        expect(self.page.locator(".sticky-header h2")).to_have_text(expected_project_name)
        return self

    def close_read_me(self) -> Self:
        self.page.locator(".back .third-btn").click()

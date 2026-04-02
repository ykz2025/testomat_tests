from typing import Self

from playwright.sync_api import Page, expect

from src.web.components.side_bar import SideBar


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBar(page)

    def open_by_id(self, project_id: str) -> Self:
        self.page.goto(f"/projects/{project_id}")
        return self

    def is_loaded(self) -> Self:
        expect(self.page.locator(".sticky-header")).to_be_visible()
        expect(self.page.get_by_placeholder("First Suite")).to_be_visible()
        return self

    def empty_project_name_is(self, expected_project_name: str) -> Self:
        expect(self.page.locator(".sticky-header h2")).to_have_text(expected_project_name)
        return self

    def close_read_me(self) -> Self:
        button = self.page.locator(".back .third-btn")
        if button.is_visible():
            button.click()
            expect(button).to_be_hidden()
        return self

    def create_test_suite_via_popup(self) -> Self:
        self.page.locator(".md-icon-chevron-down").click()
        self.page.get_by_text("Collection of test cases").click()
        return self

    def create_first_suite(self, target_suite_name: str) -> Self:
        self.page.get_by_placeholder("First Suite").fill(target_suite_name)
        suite_button = self.page.get_by_role("button", name="Suite")
        suite_button.click()

        self.suite_with_name_is_visible(target_suite_name)
        return self

    def suite_with_name_is_visible(self, suite_name: str) -> None:
        locator = self.page.locator(f"a[href*='/suite/']").get_by_text(suite_name, exact=True)
        expect(locator).to_be_visible(timeout=10000)

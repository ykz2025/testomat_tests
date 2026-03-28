from typing import Self

from playwright.sync_api import Page, expect

from src.web.components.side_bar import SideBar


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBar(page)

    def open_by_id(self, project_id: str) -> Self:
        """Navigates directly to the project page using its ID."""
        self.page.goto(f"/projects/{project_id}")
        return self

    def is_loaded(self) -> Self:
        """Verifies that the main project page elements are visible."""
        expect(self.page.locator(".sticky-header")).to_be_visible()
        # Using get_by_placeholder for better stability
        expect(self.page.get_by_placeholder("First Suite")).to_be_visible()
        return self

    def empty_project_name_is(self, expected_project_name: str) -> Self:
        """Checks if the project name in the header matches the expected string."""
        expect(self.page.locator(".sticky-header h2")).to_have_text(expected_project_name)
        return self

    def close_read_me(self) -> Self:
        """Closes the 'Read Me' popup if it is visible."""
        button = self.page.locator(".back .third-btn")
        if button.is_visible():
            button.click()
            expect(button).to_be_hidden()
        return self

    def create_test_suite_via_popup(self) -> Self:
        """Clicks the dropdown icon and selects the option to create a new suite."""
        # Click the chevron icon to open the creation menu
        self.page.locator(".md-icon-chevron-down").click()
        # Click the specific text to initiate suite creation
        self.page.get_by_text("Collection of test cases").click()
        return self

    def create_first_suite(self, target_suite_name: str) -> Self:
        """Fills in the suite name and submits the form."""
        self.page.get_by_placeholder("First Suite").fill(target_suite_name)
        suite_button = self.page.get_by_role("button", name="Suite")
        suite_button.click()

        # Ensure the record appears in the UI before proceeding
        # This prevents race conditions in tests
        self.suite_with_name_is_visible(target_suite_name)
        return self

    def suite_with_name_is_visible(self, suite_name: str) -> None:
        """Checks if a suite with the specified name is visible in the list."""
        # Using span.mr-1 as identified in the HTML structure
        # exact=True ensures we find the specific suite, not just a partial match
        locator = self.page.locator("span.mr-1").get_by_text(suite_name, exact=True)
        expect(locator).to_be_visible(timeout=10000)

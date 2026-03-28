from playwright.sync_api import Page, expect


class TestModal:
    def __init__(self, page: Page):
        self.page = page
        self._title = page.locator("[placeholder='Title']")

    def is_loaded(self, artifact_type) -> TestModal:
        expect(self.page.get_by_role("heading", name=f"New {artifact_type}")).to_be_visible()
        expect(self._title).to_be_visible()
        return self

    def set_title(self, title: str) -> TestModal:
        self._title.fill(title)
        return self

    def save(self) -> TestModal:
        self.page.get_by_role(role="button", name="Save").click()
        return self

    def edit_is_visible(self, artifact_type) -> TestModal:
        expect(self.page.get_by_role(role="heading", name=f"Edit {artifact_type}")).to_be_visible()
        return self

    def saved_status_label_visible(self) -> TestModal:
        expect(self.page.get_by_role(role="heading", name="Saved")).to_be_visible()
        return self

from typing import Self

from playwright.sync_api import expect, Page


class NewProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self._form_container = page.locator("#content-desktop [action='/projects']")

    def open(self) -> Self:
        self.page.goto("/projects/new")
        return self

    def is_loaded(self) -> Self:
        expect(self._form_container).to_be_visible()
        expect(self._form_container.locator("#classical")).to_be_visible()
        expect(self._form_container.locator("#classical")).to_contain_text("Classical")
        expect(self._form_container.locator("#bdd")).to_be_visible()
        expect(self._form_container.locator("#bdd")).to_contain_text("BDD")
        expect(self._form_container.locator("#project_title")).to_be_visible()
        expect(self._form_container.locator("#demo-btn")).to_be_visible()
        expect(self._form_container.locator("#project-create-btn")).to_be_visible()
        expect(self.page.get_by_text("How to start?")).to_be_visible()
        expect(self.page.get_by_text("New Project")).to_be_visible()
        return self

    def fill_project_title(self, target_project_name: str) -> Self:
        self._form_container.locator("#project_title").fill(target_project_name)
        return self

    def click_create(self) -> Self:
        self._form_container.locator("input[type='submit'][value='Create']").click()
        expect(self._form_container.locator("#project_create-btn input")).to_be_hidden(timeout=10000)
        return self

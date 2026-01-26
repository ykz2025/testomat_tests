from typing import List

from playwright.sync_api import expect, Page

from src.web.components.ProjectCard import ProjectCard
from src.web.components.ProjectsPageHeader import ProjectsPageHeader


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = ProjectsPageHeader(page)

        self.success_message = page.locator('.common-flash-success-right p')
        self.info_message = page.locator('.common-flash-info-right p')

        self.projects_grid = page.locator('#grid')
        self._project_cards = page.locator('#grid ul li a[href*="/projects/"]')

        self.total_count = page.locator('.common-counter')

    def navigate(self, url: str = '/projects'):
        self.page.goto(url)
        self.page.wait_for_load_state('networkidle')

    def get_success_message(self) -> str:
        return self.success_message.text_content().strip()

    def get_projects(self) -> List[ProjectCard]:
        return [ProjectCard(card) for card in self._project_cards.all()]

    def get_project_by_title(self, title: str) -> ProjectCard:
        card = self._project_cards.filter(has=self.page.locator('h3', has_text=title)).first
        return ProjectCard(card)

    def count_of_project_visible(self, expected_count: int):
        return expect(self._project_cards.filter(visible=True)).to_have_count(expected_count)

    def get_total_projects(self) -> int:
        return int(self.total_count.text_content())

    def search_and_get_results(self, query: str) -> List[ProjectCard]:
        self.header.search_project(query)
        self.page.wait_for_timeout(300)
        return self.get_projects()

    def verify_page_loaded(self):
        expect(self.header.page_title).to_be_visible()
        expect(self.projects_grid).to_be_visible()

    def verify_success_message(self, expected_text: str):
        expect(self.success_message).to_have_text(expected_text)

    def get_demo_projects(self) -> List[ProjectCard]:
        return [project for project in self.get_projects() if project.is_demo_project()]

    def is_loaded(self):
        expect(self.page.locator(".common-flash-success")).to_be_visible()
        expect(self.page.locator(".common-flash-success")).to_have_text("Signed in successfully")

        expect(self.page.locator(".common-flash-success", has_text="Signed in successfully")).to_be_visible()

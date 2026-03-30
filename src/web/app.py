from playwright.sync_api import Page

from src.web.components.test_for_suite_popup import TestForSuitePopup
from src.web.components.test_modal import TestModal
from src.web.pages import HomePage, LoginPage, NewProjectPage, ProjectPage, ProjectsPage


class App:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.projects_page = ProjectsPage(page)
        self.new_project_page = NewProjectPage(page)
        self.project_page = ProjectPage(page)
        self.test_for_suite_popup = TestForSuitePopup(page)
        self.test_modal = TestModal(page)

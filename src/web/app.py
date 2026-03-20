from playwright.sync_api import Page

from src.web.pages import HomePage, LoginPage, NewProjectPage, ProjectPage, ProjectsPage


class App:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.projects_page = ProjectsPage(page)
        self.new_project_page = NewProjectPage(page)
        self.project_page = ProjectPage(page)
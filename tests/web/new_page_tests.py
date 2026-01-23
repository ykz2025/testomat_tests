from faker import Faker
from playwright.sync_api import Page

from src.web.pages.NewProjectsPage import NewProjectsPage
from src.web.pages.ProjectPage import ProjectPage


def test_new_project_page_elements(page: Page, login):
    new_projects = NewProjectsPage(page)
    new_projects.open()
    new_projects.is_loaded()


def test_new_project_creation(page: Page, login):
    new_projects = NewProjectsPage(page)
    new_projects.open()
    new_projects.is_loaded()

    target_project_name = Faker().company()
    new_projects.fill_project_title(target_project_name)
    new_projects.click_create()

    ProjectPage(page).is_loaded()

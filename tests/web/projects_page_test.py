from playwright.sync_api import Page

from src.web.components.ProjectCard import Badges
from src.web.pages.ProjectsPage import ProjectsPage


def test_projects_page_header(page: Page, login):
    projects_page = ProjectsPage(page)
    projects_page.navigate()

    projects_page.verify_page_loaded()

    assert projects_page.header.get_selected_company() == "QA Club Lviv"
    assert projects_page.header.get_plan_name() == "Enterprise plan"

    target_project_name = "manufacture light"
    projects_page.header.search_project(target_project_name)
    projects_page.count_of_project_visible(1)
    target_project = projects_page.get_project_by_title(target_project_name)
    target_project.get_badges_has(Badges.Demo)

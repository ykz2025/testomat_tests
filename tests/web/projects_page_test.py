from playwright.sync_api import Page

from src.web.components.ProjectCard import Badges
from src.web.pages.App import App


def test_projects_page_header(page: Page, login, app: App):
    app.projects_page.navigate()

    app.projects_page.verify_page_loaded()

    assert app.projects_page.header.get_selected_company() == "QA Club Lviv"
    assert app.projects_page.header.get_plan_name() == "Enterprise plan"

    target_project_name = "manufacture light"
    app.projects_page.header.search_project(target_project_name)
    app.projects_page.count_of_project_visible(1)
    target_project = app.projects_page.get_project_by_title(target_project_name)
    target_project.get_badges_has(Badges.Demo)

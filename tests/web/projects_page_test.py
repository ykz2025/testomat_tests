from src.web.components.ProjectCard import Badges
from src.web.pages.App import App


def test_projects_page_header(logged_app: App):
    logged_app.projects_page.navigate()

    logged_app.projects_page.verify_page_loaded()

    logged_app.projects_page.header.check_selected_company("QA Club Lviv")
    logged_app.projects_page.header.plan_name_should_be("Enterprise plan")

    target_project_name = "manufacture light"
    logged_app.projects_page.header.search_project(target_project_name)
    logged_app.projects_page.count_of_project_visible(2)
    target_project = logged_app.projects_page.get_project_by_title(target_project_name)
    target_project.get_badges_has(Badges.Classical)

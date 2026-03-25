import pytest

from src.web import App
from src.web.components import Badges

# Test data constants
DEMO_PROJECT_NAME = "python manufacture"
DEFAULT_COMPANY = "QA Club Lviv"
EXPECTED_PLAN = "Enterprise plan"


@pytest.mark.smoke
@pytest.mark.web
def test_projects_page_header(logged_app: App):
    """Test page header functionality"""
    logged_app.projects_page.open()

    logged_app.projects_page.is_loaded()

    logged_app.projects_page.header.check_selected_company(DEFAULT_COMPANY)
    logged_app.projects_page.header.plan_name_should_be(EXPECTED_PLAN)

    target_project_name = DEMO_PROJECT_NAME
    logged_app.projects_page.header.search_project(target_project_name)
    logged_app.projects_page.count_of_projects_visible(1)
    target_project = logged_app.projects_page.get_project_by_title(target_project_name)
    target_project.badges_has(Badges.DEMO)

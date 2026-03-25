import pytest
from playwright.sync_api import expect

from src.web.app import App


@pytest.mark.smoke
@pytest.mark.web
def test_projects_page_header(free_project_app: App):
    expect(free_project_app.page.get_by_text("You have not created any projects yet")).to_be_visible()
    expect(free_project_app.page.get_by_text("Free plan")).to_be_visible()

import pytest
from playwright.sync_api import expect

from src.web.app import App


@pytest.mark.smoke
@pytest.mark.web
def test_projects_page_header(logged_app: App):
    logged_app.projects_page.navigate()
    expect(logged_app.projects_page.header.enterprise_plan_label).to_be_visible()
    logged_app.projects_page.header.select_company("Free Projects")
    expect(logged_app.page.get_by_text("You have not created any projects yet")).to_be_visible()
    expect(logged_app.projects_page.header.free_plan_label).to_be_visible()
    logged_app.projects_page.header.free_plan_label.hover(timeout=500)
    expect(logged_app.page.get_by_text("You have a free subscription")).to_be_visible()

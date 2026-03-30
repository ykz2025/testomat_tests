import pytest
from faker import Faker

from src.api import TestomatAPI
from src.web import App


@pytest.mark.smoke
@pytest.mark.web
def test_new_project_creation_and_test_popup(logged_app: App):
    fake = Faker()
    target_project_name = fake.company()
    target_suite_name = f"Suite {fake.word()} {fake.random_int()}"  # Generate a unique suite name

    (logged_app.new_project_page.open().is_loaded().fill_project_title(target_project_name).click_create())

    project_page = logged_app.project_page
    (project_page.is_loaded().empty_project_name_is(target_project_name).close_read_me())

    (project_page.side_bar.is_loaded().click_logo().expect_tab_active("Tests"))

    project_page.create_first_suite(target_suite_name)
    project_page.suite_with_name_is_visible(target_suite_name)


@pytest.mark.smoke
@pytest.mark.web
def test_open_project_and_create_test_suite_from_side_bar(logged_app: App, api_client: TestomatAPI):
    all_projects = api_client.get_projects()
    target_project_id = all_projects[0].id

    (logged_app.project_page.open_by_id(target_project_id).side_bar.is_loaded())
    logged_app.project_page.create_test_suite_via_popup()

    suite_name = Faker().sentence()
    (logged_app.test_modal.is_loaded("Suite").set_title(suite_name).save())
    logged_app.project_page.suite_with_name_is_visible(suite_name)

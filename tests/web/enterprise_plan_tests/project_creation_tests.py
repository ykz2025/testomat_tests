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

    # Create a new project via UI
    (logged_app.new_project_page.open().is_loaded().fill_project_title(target_project_name).click_create())

    # Verify the project page is loaded and displays the correct name
    project_page = logged_app.project_page
    (project_page.is_loaded().empty_project_name_is(target_project_name).close_read_me())

    # Sidebar navigation and tab verification
    (project_page.side_bar.is_loaded().click_logo().expect_tab_active("Tests"))

    # Create the first suite and perform final visibility check
    # Note: create_first_suite method now includes internal visibility verification
    project_page.create_first_suite(target_suite_name)
    project_page.suite_with_name_is_visible(target_suite_name)


@pytest.mark.smoke
@pytest.mark.web
def test_open_project_and_create_test_suite_from_side_bar(logged_app: App, api_client: TestomatAPI):
    """
    Tests opening an existing project and creating a test suite from the sidebar.
    """
    # Retrieve existing projects via API to get a valid project ID
    all_projects = api_client.get_projects()
    target_project_id = all_projects[0].id

    # Open the specific project and verify sidebar state
    (logged_app.project_page.open_by_id(target_project_id).side_bar.is_loaded())

    # Initiate suite creation via the popup menu
    logged_app.project_page.create_test_suite_via_popup()

    # Fill in suite details in the modal and save
    suite_name = Faker().sentence()
    (logged_app.test_modal.is_loaded("Suite").set_title(suite_name).save())

    # Verify the newly created suite appears in the sidebar list
    logged_app.project_page.suite_with_name_is_visible(suite_name)

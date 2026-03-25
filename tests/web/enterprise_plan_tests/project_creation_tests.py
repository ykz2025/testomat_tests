import pytest
from faker import Faker

from src.web import App


@pytest.mark.smoke
@pytest.mark.web
def test_new_project_creation_and_test_popup(logged_app: App):
    fake = Faker()
    target_project_name = fake.company()

    logged_app.new_project_page.open().is_loaded().fill_project_title(target_project_name).click_create()

    project_page = logged_app.project_page
    project_page.is_loaded().empty_project_name_is(target_project_name).close_read_me()

    project_page.side_bar.is_loaded().click_logo().expect_tab_active("Tests")

    target_suite_name = fake.company()
    project_page.create_first_suite(target_suite_name)
    project_page.create_test_via_popup()
    logged_app.test_for_suite_popup.is_loaded().select_first_suite()

    test_name = fake.sentence()
    logged_app.page.pause()
    logged_app.test_modal.is_loaded().set_title(test_name).save()
    logged_app.test_modal.edit_is_visible()

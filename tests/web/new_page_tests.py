import pytest
from faker import Faker

from src.web.pages.App import App


@pytest.mark.web
def test_create_new_project(logged_app: App):
    target_project_name = Faker().company()

    (logged_app.new_project_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (logged_app.project_page
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_read_me())

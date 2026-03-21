import pytest
from playwright.sync_api import Page, expect

from src.web import App

TARGET_PROJECT = "Manufacture light"
pytestmark = pytest.mark.web


def test_open_home_page(page: Page, app: App):
    app.home_page.open()
    expect(page).to_have_title("AI Test Management Tool | Testomat.io")

    header_items = ["Features", "Pricing", "Docs", "Changelog", "Blog", "Log in"]
    for item in header_items:
        expect(page.get_by_role("link", name=item, exact=True)).to_be_visible()

    expect(page.locator("header").get_by_role("link", name="Meetups", exact=True)).to_be_visible()
    expect(page.locator("header").get_by_role("link", name="Start for free", exact=True)).to_be_visible()


def test_search_project_in_company(logged_app: App):
    logged_app.projects_page.navigate()
    logged_app.projects_page.search_and_get_results(TARGET_PROJECT)

    expect(logged_app.page.get_by_role("heading", name=TARGET_PROJECT, exact=True)).to_be_visible()


def test_should_be_possible_to_open_free_project(logged_app: App):
    logged_app.projects_page.navigate()
    logged_app.page.locator("#company_id").select_option("Free Projects")

    expect(logged_app.page.locator("#company_id")).to_contain_text("Free Projects")


def test_change_projects_view(logged_app: App):
    logged_app.projects_page.navigate()

    logged_app.page.locator("#company_id").select_option("789")
    logged_app.page.locator("#grid li").first.wait_for(state="visible", timeout=10000)

    logged_app.page.locator("#table-view").click()

    expect(logged_app.page.locator("table")).to_be_visible()
    expect(logged_app.page.locator("#grid")).to_be_hidden()

    logged_app.page.locator("#grid-view").click()

    expect(logged_app.page.locator("#grid")).to_be_visible()
    expect(logged_app.page.locator("#grid li").first).to_be_visible()
    expect(logged_app.page.locator("table")).to_be_hidden()


def test_create_classical_project(logged_app: App):
    logged_app.new_project_page.open()

    expect(logged_app.new_project_page._form_container.locator("#classical")).to_be_visible()


def test_create_bdd(logged_app: App):
    logged_app.new_project_page.open()
    logged_app.new_project_page._form_container.locator("#bdd").click()

    expect(logged_app.new_project_page._form_container.locator("#bdd")).to_be_visible()


def test_project_not_created_without_title(logged_app: App):
    logged_app.new_project_page.open()
    logged_app.new_project_page._form_container.locator("input[type='submit'][value='Create']").click()

    project_input = logged_app.new_project_page._form_container.locator("#project_title")
    expect(project_input).to_be_empty()

    validation_msg = project_input.evaluate("el => el.validationMessage")
    assert validation_msg == "Please fill out this field."

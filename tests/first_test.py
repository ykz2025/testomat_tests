from playwright.sync_api import Page, expect


def test_open_home_page(page: Page):
    open_home_page(page)

    expect(page).to_have_title('AI Test Management Tool | Testomat.io')

    # Check that all header elements are displayed as

    # Features, Pricing, Docs, Changelog, Meetups, Blog, Log in, Start for free

    header_items = ["Features", "Pricing", "Docs", "Changelog", "Blog", "Log in"]

    for item in header_items:
        expect(page.get_by_role("link", name=item, exact=True)).to_be_visible()

    expect(page.locator("header").get_by_role("link", name="Meetups", exact=True)).to_be_visible()

    expect(page.locator("header").get_by_role("link", name="Start for free", exact=True)).to_be_visible()


def test_invalid_login(page: Page):
    open_home_page(page)

    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    page.get_by_role("link", name='Log in', exact=True).click()

    login_user(page, email="ykzlearn@gmail.com", password="t3y4hjykdfk")

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()

    expect(page.locator("#content-desktop .common-flash-info")).to_have_text("Invalid Email or password.")


def test_search_project_in_company(page: Page):
    page.goto('https://app.testomat.io/users/sign_in')

    login_user(page, email="ykzlearn@gmail.com", password="9YFihit72@2cqh")

    target_project = "Manufacture light"

    search_for_project(page, target_project)

    expect(page.get_by_role("heading", name=target_project, exact=True)).to_be_visible()


def test_should_be_possible_to_open_free_project(page: Page):
    page.goto('https://app.testomat.io/users/sign_in')

    login_user(page, email="ykzlearn@gmail.com", password="9YFihit72@2cqh")

    select_free_projects(page)

    expect(page.locator("#company_id")).to_contain_text("Free Projects")


def test_change_projects_view(page: Page):
    page.goto('https://app.testomat.io/users/sign_in')

    login_user(page, email="ykzlearn@gmail.com", password="9YFihit72@2cqh")

    page.locator("#table-view").click()

    expect(page.locator("table")).to_be_visible()

    expect(page.locator("#grid")).to_be_hidden()

    page.locator("#grid-view").click()

    expect(page.locator("#grid")).to_be_visible()

    expect(page.locator("#grid li").first).to_be_visible()

    expect(page.locator("table")).to_be_hidden()


def test_create_classical_project(page: Page):
    page.goto('https://app.testomat.io/users/sign_in')

    login_user(page, email="ykzlearn@gmail.com", password="9YFihit72@2cqh")

    page.get_by_role("link", name="Create").click()

    expect(page.get_by_text("Classical", exact=True)).to_be_visible()


def test_create_bdd(page: Page):
    page.goto('https://app.testomat.io/users/sign_in')

    login_user(page, email="ykzlearn@gmail.com", password="9YFihit72@2cqh")

    page.get_by_role("link", name="Create").click()

    page.locator("#bdd").click()

    expect(page.get_by_text("BDD", exact=True)).to_be_visible()


def test_project_not_created_without_title(page: Page):
    page.goto('https://app.testomat.io/users/sign_in')

    login_user(page, email="ykzlearn@gmail.com", password="9YFihit72@2cqh")

    page.get_by_role("link", name="Create").click()

    page.get_by_role("button", name="Create", exact=True).click()

    project_input = page.get_by_placeholder("My Project")

    expect(project_input).to_be_empty()

    validation_msg = project_input.evaluate("el => el.validationMessage")

    assert validation_msg == "Please fill out this field."


def select_free_projects(page: Page):
    page.locator("#company_id").click()

    page.locator("#company_id").select_option("Free Projects")


def search_for_project(page: Page, target_project: str):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()

    page.locator("#content-desktop #search").fill(target_project)


def open_home_page(page: Page):
    page.goto('https://testomat.io')


def login_user(page: Page, email:
str, password: str):
    page.locator("#content-desktop #user_email").fill(email)

    page.locator("#content-desktop #user_password").fill(password)

    page.get_by_role("button", name='Sign in').click()

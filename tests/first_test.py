from playwright.sync_api import Page, expect


def test_open_home_page(page: Page):
    page.goto('https://testomat.io')
    expect(page).to_have_title('AI Test Management Tool | Testomat.io')

    # Check that all header elements are displayed as
    # Features, Pricing, Docs, Changelog, Meetups, Blog, Log in, Start for free

    header_items = ["Features", "Pricing", "Docs", "Changelog", "Blog", "Log in"]
    for item in header_items:
        expect(page.get_by_role("link", name=item, exact=True)).to_be_visible()

    expect(page.locator("header").get_by_role("link", name="Meetups", exact=True)).to_be_visible()
    expect(page.locator("header").get_by_role("link", name="Start for free", exact=True)).to_be_visible()


def test_invalid_login(page: Page):
    # User already opened the home page https://testomat.io
    # Fill invalid credits
    page.get_by_role("link", name='Log in', exact=True).click()
    page.locator("#content-desktop #user_email").fill("name@email.com")
    page.locator("#content-desktop #user_password").fill("********")

    expect(page.get_by_text("Invalid Email or password.")).to_be_visible()
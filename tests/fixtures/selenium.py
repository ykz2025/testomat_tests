import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(0)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()

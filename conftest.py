import pytest
from playwright.sync_api import Playwright

from utils.helper import Helper


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )
    parser.addoption(
        "--url_name", action="store", default="https://www.booking.com/", help="server selection"
    )


@pytest.fixture
def browser_instance(playwright: Playwright, request):
    browser_name = request.config.getoption("browser_name")
    browser = ''
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=False)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)
    elif browser_name == "safari":
        browser = playwright.webkit.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.booking.com/")
    yield page
    context.close()
    browser.close()
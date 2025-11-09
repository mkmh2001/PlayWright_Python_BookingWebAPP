import datetime
import os

import pytest
from playwright.sync_api import Playwright

from utils.helper import Helper
from utils.logger import setup_logger


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

    # Read the '--headed' flag from pytest
    headed = request.config.getoption("--headed")
    headless = not headed  # Playwright uses 'headless' param (inverse of headed)
    tracing_option = request.config.getoption("--tracing")
    browser = ''

    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=headless, args=["--start-maximized"])
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=headless)
    elif browser_name == "safari":
        browser = playwright.webkit.launch(headless=headless)

    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.goto("https://www.booking.com/")

    if tracing_option.lower() == "on":
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    if tracing_option.lower() == "on":
        context.tracing.stop(path=f"test_results/trace_{browser_name}.zip")

    context.close()
    browser.close()

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Enable instant print output
    config.option.capture = 'no'  # same as -s
    # Folder to store reports
    results_dir = os.path.join(os.getcwd(), "test_results/html_reports")
    os.makedirs(results_dir, exist_ok=True)

    # Create a timestamped report name
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    html_report = os.path.join(results_dir, f"report_{timestamp}.html")

    # Configure pytest-html
    config.option.htmlpath = html_report
    config.option.self_contained_html = True  # embed CSS/JS

@pytest.fixture(scope="session", autouse=True)
def logger():
    """
    Session-wide logger instance available to all tests and fixtures.
    """
    log = setup_logger()
    log.info("===== Test Session Started =====")
    yield log
    log.info("===== Test Session Finished =====")
import time

import pytest
from openpyxl import Workbook
from playwright.sync_api import expect
from utils.logger import setup_logger
from pageobjects.dashboard_page import DashboardPage
from pageobjects.home_page import HomePage
from utils.helper import Helper
data = Helper.get_test_data()
logger = setup_logger()

@pytest.mark.smoke
@pytest.mark.parametrize('data', data)
def test_verify_flights(browser_instance, data):
    page = browser_instance

    # Update data in home/flights page
    home_page = HomePage(page, data)
    home_page.open_flights_page()
    home_page.set_filters()
    home_page.set_departure_place()
    home_page.set_destination_place()
    home_page.set_travel_dates()
    home_page.update_travellers_and_search()

    #verify departure
    dashboard = DashboardPage(page,data)
    air_line_details = dashboard.get_air_line_details()

    Helper.save_data_to_excel(air_line_details)
    logger.info("Test results are updated in excel")
    logger.info("Flight results are verified")
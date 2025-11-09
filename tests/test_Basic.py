import time
from openpyxl import Workbook

from playwright.sync_api import Playwright, expect


def test_basic(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.booking.com/")

    source = "BLR"
    destination = "London"

    close_sign_in_form = page.locator("//button[@aria-label = 'Dismiss sign in information.']")
    if close_sign_in_form.is_visible():
        close_sign_in_form.click()
        print("Sign In form showed & it is closed")
    else:
        print("Sign In form not showed")

    page.locator("#flights").click()
    page.wait_for_load_state("networkidle")

    one_way = page.locator("#search_type_option_ONEWAY")
    one_way.wait_for()
    one_way.check()

    direct_flight_filter = page.locator("//label[@for = 'direct_flights_input_checkbox']/span[contains(@class, 'field')]")
    direct_flight_filter.wait_for()
    direct_flight_filter.click()

    cabin_class_option = "Business"
    cabin_class = page.locator("[data-ui-name = cabin_class_input]");
    cabin_class.wait_for()
    cabin_class.select_option(cabin_class_option)

    # Set Departure

    leave_from_btn = page.locator("//button[@data-ui-name = 'input_location_from_segment_0']")
    leave_from_btn.wait_for()
    leave_from_btn.click()

    page.wait_for_selector("//span[contains(@class , 'Chip-module')]//span[contains(@class, 'Icon-module')]")
    xbtns = page.locator("//span[contains(@class , 'Chip-module')]//span[contains(@class, 'Icon-module')]")
    count = xbtns.count()
    print(count)
    for i in range(count):
        print("clicking  th button")
        xbtns.nth(i).click()
        time.sleep(1)

    #Enter the destination
    dst_input = page.locator("//input[contains(@class, 'textInput')]")
    dst_input.wait_for()
    dst_input.press_sequentially(source)

    dst_result = page.locator("//ul[@id = 'flights-searchbox_suggestions']//li/span")
    dst_result.nth(0).wait_for()

    dst_name = dst_result.nth(1).text_content()
    print(dst_name)
    dst_result.nth(2).click()

    selected_dst = page.locator("//span[contains(@class , 'title__content')]")
    selected_dst.nth(0).wait_for()
    print(selected_dst.nth(0).text_content())

    # Set Destination
    page.wait_for_selector("//span[contains(text(), 'Going to')]")
    page.locator("//span[contains(text(), 'Going to')]").first.click()


    # Enter the destination
    dst_input2 = page.locator("//input[contains(@class, 'textInput_')]")
    dst_input2.wait_for()
    dst_input2.click()
    dst_input2.press_sequentially(destination)

    dst_resultt = page.locator("//ul[@id = 'flights-searchbox_suggestions']//li[1]/span")
    dst_resultt.nth(0).wait_for()

    dst_namee = dst_resultt.nth(1).text_content()
    print(dst_namee)
    dst_resultt.nth(2).click()

    selected_dst = page.locator("//span[contains(@class , 'title__content')]")
    selected_dst.nth(2).wait_for()
    print(selected_dst.nth(2).text_content())

    # calendar
    calendar_btn = page.locator("//button[@data-ui-name = 'button_date_segment_0']")
    calendar_btn.wait_for()
    calendar_btn.click()
    #time.sleep(3)

    #from date
    select_date(page, "January 2026", "20")
    #to date
    # select_date(page, "January 2026", "20")

    #Travellers
    traveller_btn = page.locator("//button[@data-ui-name = 'button_occupancy']")
    traveller_btn.wait_for()
    traveller_btn.click()

    adults = 5
    childern = 1

    addAdults = page.locator("[data-ui-name = button_occupancy_adults_plus]")
    addAdults.wait_for()
    addChildren = page.locator("[data-ui-name = button_occupancy_children_plus]")
    for i in range(adults-1):
        addAdults.click()

    for i in range(childern):
        addChildren.click()


    children_age = page.locator("//select[contains(@class , 'InputSelect-module__field')]")
    children_age.first.wait_for()
    children_age.first.select_option("5")

    done_btn = page.locator("//button[@data-ui-name = 'button_occupancy_action_bar_done']")
    done_btn.wait_for()
    done_btn.click()

    #Click search
    search_btn = page.locator("//button[@data-ui-name = 'button_search_submit']")
    search_btn.wait_for()
    search_btn.scroll_into_view_if_needed()
    search_btn.click()

    plane_list = page.locator("//ul[contains(@class, 'List-module__root')]")
    plane_list.wait_for(timeout=60000)

    #verify departure
    air_line_details = [["AirLine Name", "Price", "Departure Time", "Arrival Time"]]

    departure_in_result = page.locator("//span[@data-testid = 'flight_card_segment_departure_airport_0']")
    departure_in_result.nth(0).wait_for()
    destination_in_result = page.locator("//span[@data-testid = 'flight_card_segment_destination_airport_0']")
    air_line_name = page.locator("//div[@data-testid = 'flight_card_carriers']")
    air_line_price = page.locator("//div[@data-testid = 'upt_price']")
    air_line_departure_time = page.locator("//div[@data-testid = 'flight_card_segment_departure_time_0']")
    air_line_arrival_time = page.locator("//div[@data-testid = 'flight_card_segment_destination_time_0']")

    for i in range(departure_in_result.count()):
        # expect(departure_in_result.nth(i)).to_contain_text(source)
        # expect(destination_in_result.nth(i)).to_contain_text(destination)
        nth_air_line_details = []

        nth_air_line_details.append(air_line_name.nth(i).text_content())
        curr_price = air_line_price.nth(i).text_content()
        curr_price = curr_price.replace("INR", "")
        nth_air_line_details.append(curr_price)
        nth_air_line_details.append(air_line_departure_time.nth(i).text_content())
        nth_air_line_details.append(air_line_arrival_time.nth(i).text_content())
        air_line_details.append(nth_air_line_details)

    print(air_line_details)
    time.sleep(10)
    save_data_to_excel(air_line_details)

    context.close()
    browser.close()


def select_date(page, month_year: str, day: str):
    # keep clicking next until month visible  //h3[contains(text(), '{month_year}')]
    while not page.locator(f"//h3[contains(text(), '{month_year}')]").first.is_visible():
        next_btn = page.locator("//button[contains(@class, 'control--next')]")
        expect(next_btn).to_be_visible()
        next_btn.click()
        page.wait_for_timeout(300)  # short wait for re-render

    # click the specific day
    #//h3[contains(text(), '{month_year}')]/following-sibling::table//span[text() = '{day}']']
    day_locator = page.locator(f"//h3[contains(text(), '{month_year}')]/following-sibling::table//span[text() = '{day}']")
    expect(day_locator).to_be_visible()
    day_locator.click()


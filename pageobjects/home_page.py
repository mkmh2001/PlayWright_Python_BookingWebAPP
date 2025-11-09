from playwright.sync_api import expect

from utils.helper import Helper
class HomePage :

    def __init__(self, page, data):
        self.page = page
        self.data = data
        self.helper = Helper(page)

        # Main Page
        self.close_sign_in_form = page.locator("//button[contains(@aria-label, 'Dismiss sign')]")
        self.flights = page.locator("#flights")

        # Filters
        self.one_way = page.locator("#search_type_option_ONEWAY")
        self.direct_flights = page.locator("//label[@for = 'direct_flights_input_checkbox']/span[contains(@class, 'field')]")
        self.cabin_class = page.locator("[data-ui-name = cabin_class_input]")

        # From location
        self.leave_from_btn = page.locator("//button[@data-ui-name = 'input_location_from_segment_0']")
        self.selected_places = page.locator("//span[contains(@class , 'Chip-module')]//span[contains(@class, 'Icon-module')]")
        self.depr_input = page.locator("//input[contains(@class, 'textInput')]")
        self.depr_result = page.locator("//ul[@id = 'flights-searchbox_suggestions']//li/span")
        self.selected_depr = page.locator("//span[contains(@class , 'title__content')]")

        # To location
        self.go_to_btn = page.locator("//span[contains(text(), 'Going to')]")
        self.dst_input2 = page.locator("//input[contains(@class, 'textInput_')]")
        self.dst_result = page.locator("//ul[@id = 'flights-searchbox_suggestions']//li[1]/span")
        self.selected_dst = page.locator("//span[contains(@class , 'title__content')]")

        # Travellers Details
        self.traveller_btn = page.locator("//button[@data-ui-name = 'button_occupancy']")
        self.addAdults = page.locator("[data-ui-name = button_occupancy_adults_plus]")
        self.addChildren = page.locator("[data-ui-name = button_occupancy_children_plus]")
        self.children_age = page.locator("//select[contains(@class , 'InputSelect-module__field')]")
        self.done_btn = page.get_by_role("button", name="Done")

        # Search
        self.search_btn = page.get_by_role("button", name="Search")
        self.plane_list = page.locator("ul[class*='List-module__root']")

    def open_flights_page(self):
        # Closing the Sign in Pop up
        if self.close_sign_in_form.is_visible():
            self.close_sign_in_form.click()
            print("Sign In form showed & it is closed")
        else:
            print("Sign In form not showed")

        Helper.click_btn(self.flights)

        # waiting for all APIs to load
        self.page.wait_for_load_state("networkidle")

    def set_filters(self):
        # apply selected filters based on user input

        if self.data["round_trip"] == "No" :
            Helper.check_radio_btn(self.one_way)

        if self.data["direct_flights"] == "Yes":
            Helper.click_btn(self.direct_flights)

        Helper.set_dropdown_value(self.cabin_class, self.data["cabin_class"])

    def set_departure_place(self):
        Helper.click_btn(self.leave_from_btn)

        # Remove the selected from locations
        self.selected_places.wait_for()
        count = self.selected_places.count()
        for i in range(count):
            print("clicking  th button")
            self.selected_places.nth(i).click()

        # Enter the Departure
        Helper.set_value_in_el(self.depr_input, self.data["source"])

        # Select the Departure after verify the location code
        self.depr_result.nth(0).wait_for()
        location_code = self.depr_result.nth(1).text_content().split(" ")[0]
        if location_code == Helper.get_location_code(self.data["source"]):
            self.depr_result.nth(2).click()
            self.selected_depr.nth(0).wait_for()

        # Verify correct location is selected
        selected_location = self.selected_depr.nth(0).text_content()
        assert selected_location.split(" ")[0] == Helper.get_location_code(self.data["source"])

    def set_destination_place(self):
        destination = self.data["destination"]
        Helper.click_btn(self.go_to_btn.first)

        # Enter the destination
        Helper.set_value_in_el(self.dst_input2, destination)

        # Select the destination
        self.dst_result.nth(0).wait_for()
        location_code = self.dst_result.nth(1).text_content().split(" ")[0]
        if location_code == Helper.get_location_code(destination):
            self.dst_result.nth(2).click()

        self.selected_dst.nth(2).wait_for()
        selected_destination = self.selected_dst.nth(2).text_content()
        print(">>> "+selected_destination)
        assert selected_destination.split(" ")[0] == Helper.get_location_code(destination)

    def set_travel_dates(self):
        # travel_date = str(self.data["travel_date"])
        # temp = travel_date.split(" ", 1)
        # day = temp[0]
        # month_year = temp[1]
        # self.helper.select_date(self.page, month_year, day)
        self.helper.select_date(self.page, "February 2026", "20")

    def update_travellers_and_search(self):
        adults = self.data["adults"]
        children = self.data["children"]
        if adults > 1 or children > 0:
            Helper.click_btn(self.traveller_btn)

            self.addAdults.wait_for()
            for i in range(adults - 1):
                self.addAdults.click()

            for i in range(children):
                self.addChildren.click()

            Helper.set_dropdown_value(self.children_age, str(self.data["child_age"]))

            Helper.click_btn(self.done_btn)

        # Click search & wait for list to load
        Helper.click_btn(self.search_btn)
        self.plane_list.wait_for(timeout=60000)
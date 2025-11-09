from utils.helper import Helper
class HomePage :

    def __init__(self, page):
        self.page = page
        self.helper = Helper(page)

    def open_flights_page(self):
        close_sign_in_form = self.page.locator("//button[contains(@aria-label, 'Dismiss sign')]")
        if close_sign_in_form.is_visible():
            close_sign_in_form.click()
            print("Sign In form showed & it is closed")
        else:
            print("Sign In form not showed")

        self.page.locator("#flights").click()
        self.page.wait_for_load_state("networkidle")

    def set_filters(self):
        one_way = self.page.locator("#search_type_option_ONEWAY")
        one_way.wait_for()
        one_way.check()

        direct_flight_filter = self.page.locator(
            "//label[@for = 'direct_flights_input_checkbox']/span[contains(@class, 'field')]")
        direct_flight_filter.wait_for()
        direct_flight_filter.click()

        cabin_class_option = "Business"
        cabin_class = self.page.locator("[data-ui-name = cabin_class_input]");
        cabin_class.wait_for()
        cabin_class.select_option(cabin_class_option)

    def set_departure_place(self, source):
        leave_from_btn = self.page.locator("//button[@data-ui-name = 'input_location_from_segment_0']")
        leave_from_btn.wait_for()
        leave_from_btn.click()

        self.page.wait_for_selector("//span[contains(@class , 'Chip-module')]//span[contains(@class, 'Icon-module')]")
        xbtns = self.page.locator("//span[contains(@class , 'Chip-module')]//span[contains(@class, 'Icon-module')]")
        count = xbtns.count()
        print(count)
        for i in range(count):
            print("clicking  th button")
            xbtns.nth(i).click()


        # Enter the destination
        dst_input = self.page.locator("//input[contains(@class, 'textInput')]")
        dst_input.wait_for()
        dst_input.press_sequentially(source)

        dst_result = self.page.locator("//ul[@id = 'flights-searchbox_suggestions']//li/span")
        dst_result.nth(0).wait_for()

        dst_name = dst_result.nth(1).text_content()
        print(dst_name)
        dst_result.nth(2).click()

        selected_dst = self.page.locator("//span[contains(@class , 'title__content')]")
        selected_dst.nth(0).wait_for()
        print(selected_dst.nth(0).text_content())

    def set_destination_place(self, destination):
        self.page.wait_for_selector("//span[contains(text(), 'Going to')]")
        self.page.locator("//span[contains(text(), 'Going to')]").first.click()

        # Enter the destination
        dst_input2 = self.page.locator("//input[contains(@class, 'textInput_')]")
        dst_input2.wait_for()
        dst_input2.click()
        dst_input2.press_sequentially(destination)

        dst_resultt = self.page.locator("//ul[@id = 'flights-searchbox_suggestions']//li[1]/span")
        dst_resultt.nth(0).wait_for()

        dst_namee = dst_resultt.nth(1).text_content()
        print(dst_namee)
        dst_resultt.nth(2).click()

        selected_dst = self.page.locator("//span[contains(@class , 'title__content')]")
        selected_dst.nth(2).wait_for()
        print(selected_dst.nth(2).text_content())

    def set_travel_dates(self):
        self.helper.select_date(self.page, "January 2026", "20")
        # to date
        # select_date(page, "January 2026", "20")

    def update_travellers_and_search(self, adults, children):
        if adults > 1 or children > 0:
            traveller_btn = self.page.locator("//button[@data-ui-name = 'button_occupancy']")
            traveller_btn.wait_for()
            traveller_btn.click()

            addAdults = self.page.locator("[data-ui-name = button_occupancy_adults_plus]")
            addAdults.wait_for()
            addChildren = self.page.locator("[data-ui-name = button_occupancy_children_plus]")
            for i in range(adults - 1):
                addAdults.click()

            for i in range(children):
                addChildren.click()

            children_age = self.page.locator("//select[contains(@class , 'InputSelect-module__field')]")
            children_age.first.wait_for()
            children_age.first.select_option("5")

            done_btn = self.page.locator("//button[@data-ui-name = 'button_occupancy_action_bar_done']")
            done_btn.wait_for()
            done_btn.click()

        # Click search
        search_btn = self.page.locator("//button[@data-ui-name = 'button_search_submit']")
        search_btn.wait_for()
        search_btn.scroll_into_view_if_needed()
        search_btn.click()

        plane_list = self.page.locator("//ul[contains(@class, 'List-module__root')]")
        plane_list.wait_for(timeout=60000)
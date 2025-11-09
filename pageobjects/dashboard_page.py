class DashboardPage:

    def __init__(self, page):
        self.page = page

    def get_air_line_details(self):
        air_line_details = []

        departure_in_result = self.page.locator("//span[@data-testid = 'flight_card_segment_departure_airport_0']")
        departure_in_result.nth(0).wait_for()
        destination_in_result = self.page.locator("//span[@data-testid = 'flight_card_segment_destination_airport_0']")
        air_line_name = self.page.locator("//div[@data-testid = 'flight_card_carriers']")
        air_line_price = self.page.locator("//div[@data-testid = 'upt_price']")
        air_line_departure_time = self.page.locator("//div[@data-testid = 'flight_card_segment_departure_time_0']")
        air_line_arrival_time = self.page.locator("//div[@data-testid = 'flight_card_segment_destination_time_0']")

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

        return air_line_details
from playwright.sync_api import expect

from utils.helper import Helper


class DashboardPage:

    def __init__(self, page, data):
        self.page = page
        self.data = data
        self.air_line_name = page.locator("//div[@data-testid = 'flight_card_carriers']")
        self.air_line_price = page.locator("//div[@data-testid = 'upt_price']")
        self.air_line_departure_time = page.locator("div[data-testid*= 'departure_time_']")
        self.air_line_arrival_time = page.locator("div[data-testid*= 'destination_time_']")
        self.departure_code = page.locator("span[data-testid*='departure_airport']")
        self.destination_code = page.locator("span[data-testid*='destination_airport']")
        self.stops = page.locator("span[data-testid*= 'segment_stops']")
        self.no_stops = page.locator("div[class*= 'DismissibleContainer']")

    def get_air_line_details(self):
        departure_code = Helper.get_location_code(self.data["source"])
        destination_code = Helper.get_location_code(self.data["destination"])
        air_line_details = []
        self.air_line_name.nth(0).wait_for()

        for i in range(self.air_line_name.count()):
            expect(self.departure_code.nth(i)).to_contain_text(departure_code)
            expect(self.destination_code.nth(i)).to_contain_text(destination_code)
            if self.data["direct_flights"] == "Yes" and self.no_stops.is_visible() == False:
                assert self.stops.nth(i).text_content() == "Direct"

            nth_air_line_details = [self.air_line_name.nth(i).text_content()]
            nth_air_line_details.append(departure_code + " " + self.data["source"])
            nth_air_line_details.append(destination_code + " " + self.data["destination"])
            curr_price = self.air_line_price.nth(i).text_content()
            curr_price = curr_price.replace("INR", "").replace(",", "")
            nth_air_line_details.append(float(curr_price.replace(',', '').replace("INR", "")))
            nth_air_line_details.append(self.air_line_departure_time.nth(i).text_content())
            nth_air_line_details.append(self.air_line_arrival_time.nth(i).text_content())
            air_line_details.append(nth_air_line_details)
        return self.sort_air_line_details(air_line_details)

    def sort_air_line_details(self, air_line_details):
        air_line_details.sort(key = lambda x: x[3])
        return air_line_details


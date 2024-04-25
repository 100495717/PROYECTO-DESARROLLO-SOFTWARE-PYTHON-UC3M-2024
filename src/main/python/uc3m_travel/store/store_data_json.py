import json
from uc3m_travel.hotel_management_exception import HotelManagementException


class StoreDataJson():
    def __init__(self):
        pass

    def readjson_create_if_not(self, file_input):
        try:
            with open(file_input, "r", encoding="utf-8", newline="") as file:
                input_list = json.load(file)
        except FileNotFoundError:
            input_list = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException(
                "JSON Decode Error - Wrong JSON Format") from ex
        return input_list

    def check_item_in_json(self, input_list, my_reservation):
        for item in input_list:
            if (my_reservation.localizer ==
                    item["_HotelReservation__localizer"]):
                raise HotelManagementException("Reservation already exists")
            if my_reservation.id_card == item["_HotelReservation__id_card"]:
                raise HotelManagementException("This ID card has another reservation")

    def write_json(self, file_input, input_list):
        try:
            with open(file_input, "w", encoding="utf-8", newline="") as file:
                json.dump(input_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file  or file path") from ex

    def write_item(self, input_list, my_reservation):
        input_list.append(my_reservation.__dict__)

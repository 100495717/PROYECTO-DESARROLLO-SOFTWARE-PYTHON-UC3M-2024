
import json

from uc3m_travel.hotel_management_exception import HotelManagementException


class JsonParser:
    def __init__(self, file_input):
        self.file_input = file_input

    def parse(self, message):
        try:
            with (open(self.file_input, "r", encoding="utf-8", newline="")
                  as file):
                input_list = json.load(file)
        except FileNotFoundError as ex:
            raise HotelManagementException(message) from ex
        except json.JSONDecodeError as ex:
            raise HotelManagementException(
                "JSON Decode Error - Wrong JSON Format") from ex
        try:
            my_localizer = input_list["Localizer"]
            my_id_card = input_list["IdCard"]
        except KeyError as e:
            raise HotelManagementException("Error - Invalid Key in JSON") \
                from e
        return my_id_card, my_localizer

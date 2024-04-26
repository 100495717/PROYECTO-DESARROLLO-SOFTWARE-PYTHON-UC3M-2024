import json

from uc3m_travel.store.store_datajson_root import StoreDataRoot
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException


class SaveCheckin():

    _input_list = []

    class __SaveCheckin(StoreDataRoot):
        _input_file = JSON_FILES_PATH + "store_check_in.json"

        def __init__(self):
            self._input_list = []
            self._input_file = JSON_FILES_PATH + "store_check_in.json"

        def check_reservation(self, localizer, store_list):
            for element in store_list:
                if localizer == element["_HotelReservation_localizer"]:
                    return element
                raise HotelManagementException("Error. localizer not found")

        def load_reservation_store(self):
            try:
                with (open(self._input_file, "r", encoding="utf-8", newline="")
                      as f):
                    self._input_list = json.load(f)
            except FileNotFoundError as exc:
                raise HotelManagementException("Error: store reservation not "
                                               "found") from exc
            except json.JSONDecodeError as exc:
                raise HotelManagementException(
                    "JSON Decode Error - Wrong JSON Format") from exc
            return self._input_list

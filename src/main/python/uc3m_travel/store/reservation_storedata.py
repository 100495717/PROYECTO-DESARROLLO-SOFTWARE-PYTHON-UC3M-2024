import json

from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.store.store_datajson_root import StoreDataRoot
from uc3m_travel.hotel_management_config import JSON_FILES_PATH


class SaveReservation(StoreDataRoot):
    class __SaveReservation(StoreDataRoot):

        def __init__(self):
            self._input_list = []
            self._input_file = JSON_FILES_PATH + "store_reservation.json"
            self._mensaje_encontrado = ""

        def check_item(self, valor1, key1, valor2, key2):
            self.readjson_create_if_not(self._input_file)
            self._mensaje_encontrado = "Reservation already exists"
            super().check_item(valor1, key1)
            self._mensaje_encontrado = "This ID card has another reservation"
            super().check_item(valor2, key2)

        def load_reservation_store(self):
            try:
                with (open(self._input_file, "r", encoding="utf-8", newline="")
                      as f):
                    self._input_list = json.load(f)
            except FileNotFoundError as exc:
                raise HotelManagementException(
                    "Error: store reservation not found") from exc
            except json.JSONDecodeError as exc:
                raise HotelManagementException(
                    "JSON Decode Error - Wrong JSON Format") from exc
            return self._input_list

    __instance = None

    def __new__(cls):
        if not SaveReservation.__instance:
            SaveReservation.__instance = SaveReservation.__SaveReservation()
        return SaveReservation.__instance

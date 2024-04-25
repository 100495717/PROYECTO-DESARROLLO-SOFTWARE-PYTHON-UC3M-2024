import json

from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.store.store_datajson_root import StoreDataRoot
from uc3m_travel.hotel_management_config import JSON_FILES_PATH

class SaveReservation(StoreDataRoot):
    class __SaveReservation(StoreDataRoot):
        _input_list = []
        _input_file = JSON_FILES_PATH + "store_reservation.json"
        _mensaje_encontrado = ""

        def find_item(self, valor1, key1, valor2, key2):
            self.readjson_create_if_not(self._input_file)
            self._mensaje_encontrado = "Reservation already exists"
            super().find_item(valor1, key1)
            self._mensaje_encontrado = "This ID card has another reservation"
            super().find_item(valor2, key2)

        def load_reservation_store(self):
            try:
                with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                    self._input_list = json.load(file)
            except FileNotFoundError as exception:
                raise HotelManagementException("Error: store reservation not found") from exception
            except json.JSONDecodeError as exception:
                raise HotelManagementException(
                    "JSON Decode Error - Wrong JSON Format") from exception
            return self._input_list


    # esto en la clase reservation_json_store
    __instance = None

    def _new_(cls):
        if not SaveReservation.__instance:
            SaveReservation._instance = SaveReservation.__SaveReservation()
        return SaveReservation.__instance
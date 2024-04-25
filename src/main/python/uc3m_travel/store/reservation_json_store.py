import json
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.store.store_datajson_root import StoreDataRoot
from uc3m_travel.hotel_management_config import JSON_FILES_PATH

class SaveReservation(StoreDataRoot):
    class __SaveReservation(StoreDataRoot):
        __input_file = JSON_FILES_PATH + "store_reservation.json"
        __input_list = []

        def check_item(self, value1, key1, value2, key2):
            self.readjson_create_if_not(self.__input_file)
            self._mensaje_encontrado = "Reservation already exists"
            super().check_item(value1,key1)
            self._mensaje_encontrado = "This ID card has another reservation"
            super().check_item(value2,key2)

        def read_reservation_create_if_not(self):
            try:
                with open(self.__input_file, "r", encoding= "utf-8", newline="")\
                        as f:
                    self.__input_list = json.load(f)
            except FileNotFoundError as exc:
                raise HotelManagementException("Error: store reservation not "
                                               "found") from exc
            except json.JSONDecodeError as exc:
                raise HotelManagementException("JSON Decode Error - Wrong JSON "
                                               "Format") from exc
            return self.__input_list


    __instance = None

    def _new_(cls):
        if not SaveReservation.__instance:
            SaveReservation._instance = SaveReservation._SaveReservation()
        return SaveReservation.__instance
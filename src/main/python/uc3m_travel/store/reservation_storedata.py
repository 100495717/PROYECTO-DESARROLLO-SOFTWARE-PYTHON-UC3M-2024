from uc3m_travel.store.store_datajson_root import StoreDataRoot
from uc3m_travel.hotel_management_config import JSON_FILES_PATH


class SaveReservation(StoreDataRoot):
    class __SaveReservation(StoreDataRoot):
        def __init__(self):
            self._input_list = []
            self._file_input = JSON_FILES_PATH + "store_reservation.json"
            self._error_message_find = ""
        def find_item(self,value1,key1,value2,key2):
            self.load_store(self._file_input)
            self._error_message_find = "Reservation already exists"
            super().find_item(value1,key1)
            self._error_message_find = "This ID card has another reservation"
            super().find_item(value2,key2)

    __instance = None

    def __new__(cls):
        if not SaveReservation.__instance:
            SaveReservation.__instance = SaveReservation.__SaveReservation()
        return SaveReservation.__instance

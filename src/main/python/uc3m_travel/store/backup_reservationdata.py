from uc3m_travel.store.store_datajson_root import StoreDataRoot
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
##??? revisar luego

class SaveReservation(StoreDataRoot):
    class __SaveReservation(StoreDataRoot):
        _input_list = []
        __input_file = JSON_FILES_PATH + "store_reservation.json"
        __mensaje_error_existente = "Reservation already exists"


        def __init__(self):
            pass

        def check_item_in_reservation(self,valor1,key1,valor2,key2):
            self.readjson_create_if_not(self.__input_file)
            super().check_item(valor1,key1)
            self.__mensaje_error_existente = "This ID card has another reservation"
            super().check_item(valor2,key2)

        __instance = None

        def __new__(cls):
            if not SaveReservation.__instance:
                SaveReservation.__instance = SaveReservation.__SaveReservation()
            return SaveReservation.__instance
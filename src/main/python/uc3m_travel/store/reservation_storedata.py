from uc3m_travel.store.store_datajson_root import StoreDataRoot
from uc3m_travel.hotel_management_config import JSON_FILES_PATH


class SaveReservation(StoreDataRoot):
    __input_file = JSON_FILES_PATH + "store_reservation.json"
    __input_list = []

    def check_item(self,value1,key1,value2,key2):
        self.readjson_create_if_not(self.__input_file)
        self._mensaje_encontrado = "Reservation already exists"
        super().check_item(value1,key1)
        self._mensaje_encontrado = "This ID card has another reservation"
        super().check_item(value2,key2)

    __instance = None



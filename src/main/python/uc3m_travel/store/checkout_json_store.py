from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.store.store_datajson_root import StoreDataRoot


class SaveCheckout(StoreDataRoot):

    _mensaje_encontrado = "Guest is already out"

    class __SaveCheckout(StoreDataRoot):
        _input_file = JSON_FILES_PATH + "store_check_out.json"

        def __init__(self):
            self._input_list = []
            self._input_file = JSON_FILES_PATH + "store_check_out.json"

        def find_item(self, key, value):
            super().readjson_create_if_not()
            return super().find_item(key, value)

    __instance = None

    def __new__(cls):
        if not SaveCheckout.__instance:
            SaveCheckout.__instance = SaveCheckout.__SaveCheckout()
        return SaveCheckout.__instance

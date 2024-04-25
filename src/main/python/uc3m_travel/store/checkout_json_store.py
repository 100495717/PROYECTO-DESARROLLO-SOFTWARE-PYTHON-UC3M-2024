from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from store_datajson_root import StoreDataRoot

class SaveCheckout(StoreDataRoot):
    _input_file = JSON_FILES_PATH + "store_check_out.json"
    _input_list = []
    _mensaje_encontrado = "Guest is already out"



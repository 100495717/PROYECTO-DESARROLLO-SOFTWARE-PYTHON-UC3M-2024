from uc3m_travel.store.store_datajson_root import StoreDataRoot
from uc3m_travel.hotel_management_config import JSON_FILES_PATH

class SaveReservation(StoreDataRoot):


    def __init__(self):
        self._input_file = JSON_FILES_PATH + "store_reservation.json"
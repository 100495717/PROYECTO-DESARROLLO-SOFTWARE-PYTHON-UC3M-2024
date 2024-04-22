from uc3m_travel.attributes.attribute import Attribute
from uc3m_travel.hotel_management_exception import HotelManagementException


class Idcard(Attribute):

    def __init__(self, valor_attr):
        self._regex_pattern = r'^[0-9]{8}[A-Z]{1}$'
        self._mensaje_error = "Invalid Idcard format"
        self._valor_attr = self._validate(valor_attr)

    def _validate(self, id_card):
        super()._validate(id_card)
        if not self.validate_dni(id_card):
            raise HotelManagementException("Invalid Idcard symbols")
        return id_card

    def validate_dni(self, dni):
        """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
        valid_symbols = {
            "0": "T", "1": "R", "2": "W", "3": "A", "4": "G",
            "5": "M",
            "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
            "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
            "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        int_dni = int(dni[0:8])
        str_dni = str(int_dni % 23)
        return dni[8] == valid_symbols[str_dni]

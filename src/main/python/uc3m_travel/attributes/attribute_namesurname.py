from attribute import Attribute
from uc3m_travel.hotel_management_exception import HotelManagementException

class NameSurname(Attribute):
    def __init__(self, valor_attr):
        self._regex_pattern = r"^(?=^.{10,50}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._error_mensaje = "Invalid NameSurname format"
        self.valor_attr = self._validate(valor_attr)

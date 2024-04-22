import re

from uc3m_travel.hotel_management_exception import HotelManagementException


class Attribute:
    def __init__(self):
        self._regex_pattern = ""
        self._mensaje_error = ""
        self._valor_attr = ""

    def _validate(self, _valor_attr):
        expresion = self._regex_pattern
        myregex = re.compile(expresion)
        regex_match = myregex.fullmatch(_valor_attr)
        if not regex_match:
            raise HotelManagementException(self._mensaje_error)
        return _valor_attr

    @property
    def valor(self):
        return self._valor_attr

    @valor.setter
    def valor(self, valor_attr):
        self._valor_attr = valor_attr

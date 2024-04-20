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
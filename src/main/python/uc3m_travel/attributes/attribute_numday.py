from uc3m_travel.attributes.attribute import Attribute
from uc3m_travel.hotel_management_exception import HotelManagementException


class NumDays(Attribute):
    def __init__(self, valor_attr):
        self._regex_pattern = ""
        self._mensaje_error = ""
        self._valor_attr = self._validate(valor_attr)

    def _validate(self, num_days):
        """validates the number of days"""
        try:
            dias = int(num_days)
        except ValueError as ex:
            raise HotelManagementException("Invalid num_days datatype") from ex
        if dias < 1 or dias > 10:
            raise HotelManagementException(
                "Numdays should be in the range 1-10")
        return num_days

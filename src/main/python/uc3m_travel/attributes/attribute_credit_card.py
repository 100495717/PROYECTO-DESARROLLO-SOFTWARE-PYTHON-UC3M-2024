from uc3m_travel.attributes.attribute import Attribute
from uc3m_travel.hotel_management_exception import HotelManagementException


class Creditcard(Attribute):

    def __init__(self, valor_attr):
        self._regex_pattern = r"^[0-9]{16}"
        self._mensaje_error = "Invalid credit card format"
        self._valor_attr = self._validate(valor_attr)

    def _validate(self, card_number):
        super()._validate(card_number)
        def digitsof(number):
            return [int(i) for i in str(number)]

        digits = digitsof(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digitsof(d * 2))
        if not checksum % 10 == 0:
            raise HotelManagementException("Invalid credit card number (not luhn)")
        return card_number
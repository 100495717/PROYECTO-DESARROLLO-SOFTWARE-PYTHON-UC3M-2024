from uc3m_travel.attributes.attribute import Attribute

class PhoneNumber(Attribute):
    def __init__(self, valor_attr):
        self._regex_pattern = r"^(\+)[0-9]{9}"
        self._error_message = "Invalid phone number format"
        self._valor_attr = self._validate(valor_attr)

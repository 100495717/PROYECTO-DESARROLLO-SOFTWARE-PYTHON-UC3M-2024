from uc3m_travel.attributes.attribute import Attribute

class RoomType(Attribute):
    def __init__(self, valor_attr):
        self._regex_pattern = r"(SINGLE|DOUBLE|SUITE)"
        self._error_message = "Invalid roomtype format"
        self._valor_attr = self._validate(valor_attr)
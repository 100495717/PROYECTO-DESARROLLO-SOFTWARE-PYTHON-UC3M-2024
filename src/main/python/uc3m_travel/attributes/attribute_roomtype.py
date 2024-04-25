from uc3m_travel.attributes.attribute import Attribute


class RoomType(Attribute):
    def __init__(self, valor_attr):
        self._regex_pattern = r"(SINGLE|DOUBLE|SUITE)"
        self._mensaje_error = "Invalid roomtype value"
        self._valor_attr = self._validate(valor_attr)

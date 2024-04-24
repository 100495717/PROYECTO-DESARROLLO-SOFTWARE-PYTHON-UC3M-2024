from uc3m_travel.attributes.attribute import Attribute


class Localizer(Attribute):

    def __init__(self, valor_attr):
        self._regex_pattern = r"^[a-fA-F0-9]{32}$"
        self._mensaje_error = "Invalid localizer"
        self._valor_attr = self._validate(valor_attr)

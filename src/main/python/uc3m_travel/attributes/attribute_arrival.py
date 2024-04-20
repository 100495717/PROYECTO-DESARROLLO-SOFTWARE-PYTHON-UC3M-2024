from uc3m_travel.attributes.attribute import Attribute

class Arrivaldate(Attribute):

    def __init__(self, valor_attr):
        self._regex_pattern = r"^(([0-2]\d|-3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self._mensaje_error = "Invalid date format"
        self._valor_attr = self._validate(valor_attr)
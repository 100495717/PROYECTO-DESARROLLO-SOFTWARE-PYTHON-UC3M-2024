import json
from uc3m_travel.hotel_management_exception import HotelManagementException


class StoreDataRoot:
    _input_file = ""
    _input_list = []
    _mensaje_encontrado = ""
    _mensaje_no_encontrado = ""
    def __init__(self):
        self.readjson_create_if_not(self._input_file)

    def readjson_create_if_not(self, file_almacen):
        try:
            with (open(file_almacen, "r", encoding="utf-8", newline="") as
                  file):
                self._input_list = json.load(file)
        except FileNotFoundError:
            self._input_list = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException(
                "JSON Decode Error - Wrong JSON Format") from ex
        return self._input_list

    def write_json(self):
        try:
            with (open(self._input_file, "w", encoding="utf-8", newline="") as
                  file):
                json.dump(self._input_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file  or file path") from ex

    def write_item(self, my_reservation):
        self.readjson_create_if_not(self._input_file)
        self._input_list.append(my_reservation.__dict__)
        self.write_json()

    def check_item(self, dato, llave):
        self.readjson_create_if_not(self._input_file)
        for item in self._input_list:
            if dato == item[llave]:
                raise HotelManagementException(self._mensaje_encontrado)

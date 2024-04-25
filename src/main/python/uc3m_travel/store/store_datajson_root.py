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

    #def check_item_in_json(self, my_reservation):
        #for item in self._input_list:
            #if (my_reservation.localizer ==
                    #item["_HotelReservation__localizer"]):
                #raise HotelManagementException("Reservation already exists")
            #if my_reservation.id_card == item["_HotelReservation__id_card"]:
                #raise HotelManagementException("This ID card has another reservation")

    def write_json(self, file_almacen):
        try:
            with (open(file_almacen, "w", encoding="utf-8", newline="") as
                  file):
                json.dump(file_almacen, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file  or file path") from ex

    def write_item(self, my_reservation):
        self.readjson_create_if_not(self._input_file)
        self._input_list.append(my_reservation.__dict__)
        self.write_json(self._input_file)

    def check_item(self,dato,llave):
        self.readjson_create_if_not(self._input_file)
        for x in self._input_list:
            if dato == x[llave]:
                raise HotelManagementException(self._mensaje_encontrado)

"""Module for the hotel manager"""
import re
import json
from datetime import datetime, timezone
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from freezegun import freeze_time
from uc3m_travel.attributes.attribute_idcard import Idcard
from uc3m_travel.attributes.attribute_localizer import Localizer
from uc3m_travel.store.store_data_json import StoreDataJson
from uc3m_travel.store.reservation_storedata import SaveReservation
from uc3m_travel.JsonParser import JsonParser


class HotelManager:
    class __HotelManager:
        """Class with all the methods for managing reservations and stays"""
        def __init__(self):
            pass


        def validate_roomkey(self, room_key):
            """validates the roomkey format using a regex"""
            r = r'^[a-fA-F0-9]{64}$'
            myregex = re.compile(r)
            if not myregex.fullmatch(room_key):
                raise HotelManagementException("Invalid room key format")
            return room_key



        # pylint: disable=too-many-arguments
        def room_reservation(self,
                             credit_card: str,
                             name_surname: str,
                             id_card: str,
                             phone_number: str,
                             room_type: str,
                             arrival_date: str,
                             num_days: int) -> str:
            """manges the hotel reservation:
            creates a reservation and saves it into a json file"""

            my_reservation = HotelReservation(id_card=id_card,
                                              credit_card_number=credit_card,
                                              name_surname=name_surname,
                                              phone_number=phone_number,
                                              room_type=room_type,
                                              arrival=arrival_date,
                                              num_days=num_days)
            #guardamos la reserva
            HotelReservation.save_reservation(self, my_reservation)

            return my_reservation.localizer

        def guest_arrival(self, file_input: str) -> str:
            """manages the arrival of a guest with a reservation"""
            input_list = self.checkout_file(file_input)

            id_card, localizer = JsonParser(file_input).parse("Error: file input not found")


            reservation = HotelReservation.create_reservation(id_card, localizer)


            # compruebo si hoy es la fecha de checkin
            reservation_format = "%d/%m/%Y"
            date_obj = datetime.strptime(reservation.arrival,
                                         reservation_format)
            if date_obj.date() != datetime.date(timezone.utc).date():
                raise HotelManagementException("Error: "
                                               "today is not reservation date")

            # genero la room key para ello llamo a Hotel Stay
            my_checkin = HotelStay(idcard=id_card,
                                   numdays=int(reservation.num_days),
                                   localizer= localizer,
                                   roomtype= reservation.room_type)

            # Ahora lo guardo en el almacen nuevo de checkin
            # escribo el fichero Json con todos los datos
            file_input = JSON_FILES_PATH + "store_check_in.json"

            # leo los datos del fichero si existe ,
            # y si no existe creo una lista vacia
            store_reservation = StoreDataJson()
            room_key_list = store_reservation.readjson_create_if_not(file_input)

            # comprobar que no he hecho otro ckeckin antes
            self.check_checkin(my_checkin,room_key_list)

            # añado los datos de mi reserva a la lista , a lo que hubiera
            lista_store = StoreDataJson()
            lista_store.write_item(room_key_list, my_checkin)
            # se añade a reservas
            reservas_backup = StoreDataJson()
            reservas_backup.write_json(file_input, room_key_list)

            return my_checkin.room_key

       
        def readjson_only(self, file_input):
            try:
                with open(file_input, "r", encoding="utf-8", newline="") as file:
                    input_list = json.load(file)
            except FileNotFoundError as ex:
                raise HotelManagementException(
                    "Error: file input not found") from ex
            except json.JSONDecodeError as ex:
                raise HotelManagementException(
                    "JSON Decode Error - Wrong JSON Format") from ex
            return input_list

        def check_reservation(self, localizer, input_list):
            for item in input_list:
                if localizer == item["HotelReservation_localizer"]:
                    return item
                raise HotelManagementException("Error: localizer not found")
        def guest_checkout(self, room_key: str) -> bool:
            """manages the checkout of a guest"""
            self.validate_roomkey(room_key)
            # check thawt the roomkey is stored in the checkins file
            input_file = JSON_FILES_PATH + "store_check_in.json"
            input_list = self.checkout_file(input_file)

            # comprobar que esa room_key es la que me han dado
            departure_date_timestamp = self.check_incheckout(room_key, input_list)

            today = datetime.utcnow().date()
            if datetime.fromtimestamp(departure_date_timestamp).date() != today:
                raise HotelManagementException(
                    "Error: today is not the departure day")

            file_input = JSON_FILES_PATH + "store_check_out.json"
            store_reservation = StoreDataJson()
            input_list = store_reservation.readjson_create_if_not(file_input)

            for checkout in input_list:
                if checkout["room_key"] == room_key:
                    raise HotelManagementException("Guest is already out")

            room_checkout = {
                "room_key":  room_key, "checkout_time":
                datetime.timestamp(datetime.utcnow())}

            input_list.append(room_checkout)

            lista_backup = StoreDataJson()
            lista_backup.write_json(file_input, input_list)

            return True

        def check_incheckout(self, room_key, input_list):
            found = False
            for item in input_list:
                if room_key == item["_HotelStay__room_key"]:
                    departure_date_timestamp = item["_HotelStay__departure"]
                    found = True
            if not found:
                raise HotelManagementException("Error: room key not found")

            return departure_date_timestamp
        def check_checkin(self,my_checkin,input_list):
            for item in input_list:
                if my_checkin.room_key == item["_HotelStay__room_key"]:
                    raise HotelManagementException("checkin  ya realizado")

        def read_input_data_from_file(self, input_list):
            try:
                localizer = input_list["Localizer"]
                id_card = input_list["IdCard"]
            except KeyError as exception:
                raise HotelManagementException("Error - Invalid Key in JSON") from exception
            return id_card, localizer

        def checkout_file(self, input_file):
            try:
                with open(input_file, "r", encoding="utf-8", newline="") as file:
                    room_key_list = json.load(file)
            except FileNotFoundError as exception:
                raise HotelManagementException("Error: store checkin not found") from exception
            except json.JSONDecodeError as exception:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
            return room_key_list

    __instance = None

    def __new__(cl):
        if not HotelManager.__instance:
            HotelManager.__instance = HotelManager.__HotelManager()
        return HotelManager.__instance

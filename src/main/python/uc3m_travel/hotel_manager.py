"""Module for the hotel manager"""
import re
import json
from datetime import datetime
from .hotel_management_exception import HotelManagementException
from .hotel_reservation import HotelReservation
from .hotel_stay import HotelStay
from .hotel_management_config import JSON_FILES_PATH
from freezegun import freeze_time
from .attributes.attribute_idcard import Idcard
from .attributes.attribute_localizer import Localizer
from .store.store_data_json import StoreDataJson
from .store.reservation_storedata import SaveReservation


class HotelManager:
    """Class with all the methods for managing reservations and stays"""
    def __init__(self):
        pass

    def validatecreditcard( self, x ):
        """validates the credit card number using luhn altorithm"""
        #taken form
        # https://allwin-raju-12.medium.com/
        # credit-card-number-validation-using-luhns-algorithm-in-python-c0ed2fac6234
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE

        myregex = re.compile(r"^[0-9]{16}")
        res = myregex.fullmatch(x)
        if not res:
            raise HotelManagementException("Invalid credit card format")
        def digits_of(n):
            return [int(d) for d in str(n)]


        digits = digits_of(x)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        if not checksum % 10 == 0:
            raise HotelManagementException("Invalid credit card number (not luhn)")
        return x

    def validate_room_type(self, room_type):
        """validates the room type value using regex"""
        myregex = re.compile(r"(SINGLE|DOUBLE|SUITE)")
        res = myregex.fullmatch(room_type)
        if not res:
            raise HotelManagementException("Invalid roomtype value")
        return room_type

    def validate_arrival_date(self, arrival_date):
        """validates the arrival date format  using regex"""
        myregex = re.compile(r"^(([0-2]\d|-3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        res = myregex.fullmatch(arrival_date)
        if not res:
            raise HotelManagementException("Invalid date format")
        return arrival_date

    def validate_phonenumber(self, phone_number):
        """validates the phone number format  using regex"""
        myregex = re.compile(r"^(\+)[0-9]{9}")
        res = myregex.fullmatch(phone_number)
        if not res:
            raise HotelManagementException("Invalid phone number format")
        return phone_number
    def validate_numdays(self,num_days):
        """validates the number of days"""
        try:
            days = int(num_days)
        except ValueError as ex:
            raise HotelManagementException("Invalid num_days datatype") from ex
        if (days < 1 or days > 10):
            raise HotelManagementException("Numdays should be in the range 1-10")
        return num_days


    @staticmethod
    def validate_dni( dni ):
        """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
        valid_format = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G",
                     "5": "M",
             "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
             "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
             "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        int_dni = int(dni[ 0:8 ])
        str_dni = str(int_dni % 23)
        return dni[8] == valid_format[str_dni]


    def validate_localizer(self, localizer):
        """validates the localizer format using a regex"""
        r = r'^[a-fA-F0-9]{32}$'
        myregex = re.compile(r)
        if not myregex.fullmatch(localizer):
            raise HotelManagementException("Invalid localizer")
        return localizer

    def validate_roomkey(self, localizer):
        """validates the roomkey format using a regex"""
        r = r'^[a-fA-F0-9]{64}$'
        myregex = re.compile(r)
        if not myregex.fullmatch(localizer):
            raise HotelManagementException("Invalid room key format")
        return localizer

    def read_data_from_json(self, file_input):
        """reads the content of a json file with two fields: CreditCard and phoneNumber"""
        try:
            with open(file_input, encoding='utf-8') as file:
                json_data = json.load(file)
        except FileNotFoundError as e:
            raise HotelManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from e
        try:
            credit_card = json_data["CreditCard"]
            phone_number = json_data["phoneNumber"]
            request = HotelReservation(id_card="12345678Z",
                                   credit_card_number=credit_card,
                                   name_surname="John Doe",
                                   phone_number=phone_number,
                                   room_type="single",
                                   num_days=3,
                                   arrival="20/01/2024")
        except KeyError as e:
            raise HotelManagementException("JSON Decode Error - Invalid JSON Key") from e
        if not self.validatecreditcard(credit_card):
            raise HotelManagementException("Invalid credit card number")
        # Close the file
        return request

    # pylint: disable=too-many-arguments
    def room_reservation(self,
                         credit_card:str,
                         name_surname:str,
                         id_card:str,
                         phone_number:str,
                         room_type:str,
                         arrival_date: str,
                         num_days:int)->str:
        """manges the hotel reservation: creates a reservation and saves it into a json file"""



        my_reservation = HotelReservation(id_card=id_card,
                                          credit_card_number=credit_card,
                                          name_surname=name_surname,
                                          phone_number=phone_number,
                                          room_type=room_type,
                                          arrival=arrival_date,
                                          num_days=num_days)



        #lee el fichero y en caso de no existir crea una lista vacía
        new_reservation = SaveReservation()

        #se comprueba que la reserva no exista
        new_reservation.check_item_in_json(my_reservation)

        #lleno la lista con los datos de la reserva
        new_reservation.write_item(my_reservation)

        #lo añado al fichero
        new_reservation.write_json()



        return my_reservation.localizer





    def guest_arrival(self, file_input:str)->str:
        """manages the arrival of a guest with a reservation"""
        input_list = self.readjson_only(file_input)

        # comprobar valores del fichero
        try:
            my_localizer = input_list["Localizer"]
            my_id_card = input_list["IdCard"]
        except KeyError as e:
            raise HotelManagementException("Error - Invalid Key in JSON") from e

        #Validamos id_card
        Idcard(my_id_card)
        #Y el localizer
        Localizer(my_localizer)

        #buscar en almacen
        file_input = JSON_FILES_PATH + "store_reservation.json"

        #leo los datos del fichero , si no existe deber dar error porque el almacen de reservaa
        # debe existir para hacer el checkin
        input_list = self.readjson_only(file_input)
        # compruebo si esa reserva esta en el almacen

        reservation_days, reservation_room_type, reservation_date_timestamp, reservation_credit_card, \
        reservation_date_arrival, reservation_name, reservation_phone, reservation_id_card = self.mi_reserva(my_id_card,my_localizer,input_list)
        # regenrar clave y ver si coincide
        reservation_date = datetime.fromtimestamp(reservation_date_timestamp)

        with freeze_time(reservation_date):
            new_reservation = HotelReservation(credit_card_number=reservation_credit_card,
                                               id_card= reservation_id_card,
                                               num_days=reservation_days,
                                               room_type=reservation_room_type,
                                               arrival=reservation_date_arrival,
                                               name_surname=reservation_name,
                                               phone_number=reservation_phone)
        if new_reservation.localizer != my_localizer:
            raise HotelManagementException("Error: reservation has been manipulated")

        # compruebo si hoy es la fecha de checkin
        reservation_format = "%d/%m/%Y"
        date_obj = datetime.strptime(reservation_date_arrival, reservation_format)
        if date_obj.date()!= datetime.date(datetime.utcnow()):
            raise HotelManagementException("Error: today is not reservation date")

        # genero la room key para ello llamo a Hotel Stay
        my_checkin = HotelStay(idcard=my_id_card, numdays=int(reservation_days),
                               localizer=my_localizer, roomtype=reservation_room_type)

        #Ahora lo guardo en el almacen nuevo de checkin
        # escribo el fichero Json con todos los datos
        file_input = JSON_FILES_PATH + "store_check_in.json"

        # leo los datos del fichero si existe , y si no existe creo una lista vacia
        store_reservation = StoreDataJson()
        room_key_list = store_reservation.readjson_create_if_not(file_input)

        # comprobar que no he hecho otro ckeckin antes
        for item in input_list:
            if my_checkin.room_key == item["_HotelStay__room_key"]:
                raise HotelManagementException ("ckeckin  ya realizado")

        #añado los datos de mi reserva a la lista , a lo que hubiera
        lista_store = StoreDataJson()
        lista_store.write_item(room_key_list,my_checkin)
        #se añade a reservas
        reservas_backup = StoreDataJson()
        reservas_backup.write_json(file_input,room_key_list)

        return my_checkin.room_key


    def mi_reserva(self, my_id_card,my_localizer,input_list):
        found = False
        for item in input_list:
            if my_localizer == item["_HotelReservation__localizer"]:
                reservation_days = item["_HotelReservation__num_days"]
                reservation_room_type = item["_HotelReservation__room_type"]
                reservation_date_timestamp = item["_HotelReservation__reservation_date"]
                reservation_credit_card = item["_HotelReservation__credit_card_number"]
                reservation_date_arrival = item["_HotelReservation__arrival"]
                reservation_name = item["_HotelReservation__name_surname"]
                reservation_phone = item["_HotelReservation__phone_number"]
                reservation_id_card = item["_HotelReservation__id_card"]
                found = True

        if not found:
            raise HotelManagementException("Error: localizer not found")
        if my_id_card != reservation_id_card:
            raise HotelManagementException("Error: Localizer is not correct for this IdCard")
        return reservation_days, reservation_room_type, reservation_date_timestamp, reservation_credit_card, \
                reservation_date_arrival, reservation_name, reservation_phone, reservation_id_card
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

    def guest_checkout(self, room_key:str)->bool:
        """manages the checkout of a guest"""
        self.validate_roomkey(room_key)
        #check thawt the roomkey is stored in the checkins file
        file_input = JSON_FILES_PATH + "store_check_in.json"
        input_list = self.readjson_only(file_input)

        # comprobar que esa room_key es la que me han dado
        departure_date_timestamp = self.check_incheckout(room_key,input_list)

        today = datetime.utcnow().date()
        if datetime.fromtimestamp(departure_date_timestamp).date() != today:
            raise HotelManagementException("Error: today is not the departure day")

        file_input = JSON_FILES_PATH + "store_check_out.json"
        store_reservation = StoreDataJson()
        input_list = store_reservation.readjson_create_if_not(file_input)

        for checkout in input_list:
            if checkout["room_key"] == room_key:
                raise HotelManagementException("Guest is already out")

        room_checkout={"room_key":  room_key, "checkout_time":datetime.timestamp(datetime.utcnow())}

        input_list.append(room_checkout)

        lista_backup = StoreDataJson()
        lista_backup.write_json(file_input,input_list)

        return True


    def check_incheckout(self,room_key,input_list):
        found = False
        for item in input_list:
            if room_key == item["_HotelStay__room_key"]:
                departure_date_timestamp = item["_HotelStay__departure"]
                found = True
        if not found:
            raise HotelManagementException("Error: room key not found")

        return departure_date_timestamp
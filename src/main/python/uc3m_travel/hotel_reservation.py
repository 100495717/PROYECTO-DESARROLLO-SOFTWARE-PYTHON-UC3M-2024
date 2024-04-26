"""Hotel reservation class"""
import hashlib
import json
from datetime import datetime, timezone
import re
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.attributes.attribute_idcard import Idcard
from uc3m_travel.attributes.attribute_localizer import Localizer
from uc3m_travel.attributes.attribute_namesurname import NameSurname
from uc3m_travel.attributes.attribute_phonenumber import PhoneNumber
from uc3m_travel.attributes.attribute_arrival import Arrivaldate
from uc3m_travel.attributes.attribute_roomtype import RoomType
from uc3m_travel.attributes.attribute_creditcard import Creditcard
from uc3m_travel.attributes.attribute_numday import NumDays
from uc3m_travel.store.reservation_storedata import SaveReservation
from uc3m_travel.store.store_data_json import StoreDataJson


class HotelReservation:
    """Class for representing hotel reservations"""
    # pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(self,
                 id_card: str,
                 credit_card_number: str,
                 name_surname: str,
                 phone_number: str,
                 room_type: str,
                 arrival: str,
                 num_days: int):
        """constructor of reservation objects"""
        self.__credit_card_number = Creditcard(credit_card_number)._valor_attr
        self.__id_card = Idcard(id_card)._valor_attr
        justnow = datetime.now(timezone.utc)
        self.__arrival = Arrivaldate(arrival)._valor_attr
        self.__reservation_date = datetime.timestamp(justnow)
        self.__name_surname = NameSurname(name_surname)._valor_attr
        self.__phone_number = PhoneNumber(phone_number)._valor_attr
        self.__room_type = RoomType(room_type)._valor_attr
        self.__num_days = NumDays(num_days)._valor_attr
        self.__localizer = hashlib.md5(str(self).encode()).hexdigest()

    def __str__(self):
        """return a json string with the
        elements required to calculate the localizer"""
        # VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
        json_info = {"id_card": self.__id_card,
                     "name_surname": self.__name_surname,
                     "credit_card": self.__credit_card_number,
                     "phone_number:": self.__phone_number,
                     "reservation_date": self.__reservation_date,
                     "arrival_date": self.__arrival,
                     "num_days": self.__num_days,
                     "room_type": self.__room_type,
                     }
        return "HotelReservation:" + json_info.__str__()
    def save_reservation(self, my_reservation):
        reservation = SaveReservation()
        reservation.check_item(my_reservation.localizer,
                              "_HotelReservation__localizer", my_reservation.id_card,
                              "_HotelReservation__id_card")
        reservation.write_item(my_reservation)

    @property
    def credit_card(self):
        """property for getting and setting the credit_card number"""
        return self.__credit_card_number

    @credit_card.setter
    def credit_card(self, value):
        self.__credit_card_number = value

    @property
    def id_card(self):
        """property for getting and setting the id_card"""
        return self.__id_card

    @id_card.setter
    def id_card(self, value):
        self.__id_card = value

    @property
    def localizer(self):
        """Returns the md5 signature"""
        return self.__localizer

    @property
    def arrival(self):
        """property for getting the arrival"""
        return self.__arrival

    @property
    def room_type(self):
        """property for getting the room_type"""
        return self.__room_type

    @property
    def num_days(self):
        """property for getting the num_days"""
        return self.__num_days


    @classmethod
    def create_reservation(cls,id_card, localizer):
        id_card = Idcard(id_card)._valor_attr
        localizer = Localizer(localizer)._valor_attr

        reservation = SaveReservation()

        check = reservation.check_item(id_card, "_HotelReservation__id_card",localizer,
                                       "_HotelReservation__localizer")
        if check is None:
            raise HotelManagementException("Error: localizer not found")

        if id_card != reservation["_HotelReservation__id_card"]:
            raise HotelManagementException("Error: Localizer is not correct for this IdCard")

            # regenrar clave y ver si coincide
            reservation_date = datetime.fromtimestamp(reservation_date_timestamp)

            with freeze_time(reservation_date):
                new_reservation = HotelReservation(
                    credit_card_number=reservation["_HotelReservation__credit_card"],
                    id_card=reservation["_HotelReservation__id_card"],
                    num_days=reservation["_HotelReservation__num_days"],
                    room_type=reservation["_HotelReservation__room_type"],
                    arrival=reservation["_HotelReservation__arrival"],
                    name_surname=reservation["_HotelReservation__name_surname"],
                    phone_number=reservation["_HotelReservation__phone_number"])
            if new_reservation.localizer != localizer:
                raise HotelManagementException("Error: "
                                               "reservation has been manipulated")
            return new_reservation
    @classmethod
    def load_reservation_store(self, input_file):
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                store_list = json.load(file)
        except FileNotFoundError as exception:
            raise HotelManagementException("Error: store reservation not found") from exception
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return store_list

    @classmethod
    def find_reservation(self, localizer, input_list):
        for element in input_list:
            if localizer == element["HotelReservation_localizer"]:
                return element
            raise HotelManagementException("Error: localizer not found")
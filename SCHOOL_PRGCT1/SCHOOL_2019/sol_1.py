import requests
import time
import write_read_csv
import json
import pprint
import pathlib


YEAR_DAYS = 365  # days
MODEL_TIME = 48 * 60 * 60  # in seconds
TIME_DELAY = MODEL_TIME / YEAR_DAYS  # delay in sec representing 1 day
NUMBER_OF_CITIES = 16
CITE_URL = 'http://dt.miet.ru/ppo_it/api'
HTTP_HEADER = {'X-Auth-Token': 'dsnxki67uruwhadh'}


class City:
    city_count = 0

    def __init__(self, data: dict):
        self._id = data["city_id"]
        self._city_name = data["city_name"]
        self._house_count = data["house_count"]
        self._area_count = data["area_count"]
        self._apartment_count = data["apartment_count"]
        self._temperature = data["temperature"]
        self._data_dict = data
        City.city_count += 1

    def get_dict_info(self) -> dict:
        return self._data_dict

    def __str__(self):
        return f"Город: {self._city_name} с номером: {self._id}"

    def __repr__(self):
        return f"C{self._id}"

c = City()

class Area:
    def __init__(self, data: dict):
        self._city_id = data["city_id"]
        self._area_id = data["area_id"]
        self._house_count = data["house_count"]
        # self._apartment_count = data["apartment_count"]
        self._data_dict = data

    def get_dict_info(self) -> dict:
        return self._data_dict

    def __str__(self):
        return f"Район №{self._area_id} города: {self._city_id}"

    def __repr__(self):
        return f"A{self._area_id}"


class House:
    def __init__(self, data: dict):
        self._city_id = data["city_id"]
        self._area_id = data["area_id"]
        self._house_id = data["house_id"]
        self._apartment_count = data["apartment_count"]
        self._data_dict = data

    def get_dict_info(self) -> dict:
        return self._data_dict

    def __str__(self):
        return f"Дом №{self._house_id}, район №{self._area_id}, город №{self._city_id}"

    def __repr__(self):
        return f"H{self._house_id}"


class Apartment:
    def __init__(self, data: dict):
        self._city_id = data["city_id"]
        self._area_id = data["area_id"]
        self._house_id = data["house_id"]
        self._apartment_id = data["apartment_id"]
        # self._temperature = data["temperature"]
        self._data_dict = data

    def get_dict_info(self) -> dict:
        return self._data_dict

    def __str__(self):
        return f"Квартира №{self._apartment_id}, дом №{self._house_id}, район №{self._area_id}," \
               f" город №{self._city_id}"

    def __repr__(self):
        return f"F{self._apartment_id}"

    def get_temperature(self):
        pass


def get(url: str):
    try:
        data = requests.get(url, timeout=30, headers=HTTP_HEADER).json()
        return data["data"]
    except requests.Timeout:
        print("timeout exceeded")
        return dict


def get_city_temp():
    cities_temp = []
    for i in range(1, 17):
        url = CITE_URL + f"/{i}/temperature"
        data = get(url)["data"] # Надо написать ниже обработчик ошибок в случае с get
        cities_temp.append(data)
    return cities_temp


def get_apartment_temp() -> int:
    area_id = int(input("Введите номер города (от 1 до 16): "))
    pass


def get_city_main_info():
    cities_info = {}

    # получаем инфу про города и делаем из них объекты типа City
    for city_id in range(1, NUMBER_OF_CITIES + 1):
        url_city_main = CITE_URL + f"/{city_id}"
        city_data = get(url_city_main)
        current_city = City(city_data)  # создали экзмепляр класса City
        print("city data has been received")
        # cities_info.append(City(city_data))
        # city_i_area_data = dict()

        areas_dict = dict()
        # получам инфу про районы города
        for area_id in range(1, city_data["area_count"] + 1):
            url_area_main = CITE_URL + f"/{city_id}/{area_id}"
            area_data = get(url_area_main)  # -> [{"house_id": number, "apartment_count": number}]

            # создаем объект типа Area дополнительно подсчитав количество домов на районе
            house_count = len(area_data)
            current_area = Area({"area_id": area_id, "city_id": city_id, "house_count": house_count})

            houses_dict = dict()
            # добавяем в полученный словарь номер города и номер района и генерим объекты типв House
            for houses in area_data:
                houses.update({"city_id": city_id, "area_id": area_id})
                current_house = House(houses)

                # генерируем объекты типа Apartment (квартиры) в домах:
                apartment_list = []
                for apartment in range(1, houses["apartment_count"] + 1):
                    current_apartment = Apartment({"city_id": city_id, "area_id": area_id,
                                                   "house_id": houses["house_id"], "apartment_id": apartment})
                    apartment_list.append(current_apartment)

                houses_dict.update({current_house: apartment_list})

            areas_dict.update({current_area: houses_dict})

        cities_info.update({current_city: areas_dict})
    # pprint.pprint(cities_info)
    return cities_info


def _main():
    path = pathlib.Path(__file__).parent.absolute()
    data = get_city_main_info()
    # print(data)

    # fieldnames = list(data[0]["1"].keys())
    # write_read_csv.write_to_csv(path, "city_main_info", fieldnames, json.dumps(data[0]))
    city_i_to_write = dict()
    area_i_to_write = dict()
    house_i_to_write = dict()
    apartment_i_to_write = dict()
    city_fieldnames = []
    area_fieldnames = []
    house_fieldnames = []
    apartment_fieldnames = []
    a_i = 1
    h_i = 1
    f_i = 1

    for c_i, city_key in enumerate(data.keys(), 1):
        city_fieldnames = list(city_key.get_dict_info().keys())
        city_i_to_write.update({c_i: city_key.get_dict_info()})
        for area_key in data[city_key].keys():
            area_fieldnames = list(area_key.get_dict_info().keys())
            area_i_to_write.update({a_i: area_key.get_dict_info()})
            a_i += 1
            for house_key in data[city_key][area_key].keys():
                house_fieldnames = list(house_key.get_dict_info().keys())
                house_i_to_write.update({h_i: house_key.get_dict_info()})
                h_i += 1
                for apartments in data[city_key][area_key][house_key]:
                    apartment_fieldnames = list(apartments.get_dict_info().keys())
                    apartment_i_to_write.update({f_i: apartments.get_dict_info()})
                    f_i += 1
    # pprint.pprint(city_i_to_write)
    # pprint.pprint(area_i_to_write)
    # pprint.pprint(house_i_to_write)
    # pprint.pprint(apartment_i_to_write)

    write_read_csv.write_to_csv(path, "city_main_info.csv", city_fieldnames, json.dumps(city_i_to_write))
    write_read_csv.write_to_csv(path, "area_main_info.csv", area_fieldnames, json.dumps(area_i_to_write))
    write_read_csv.write_to_csv(path, "house_main_info.csv", house_fieldnames, json.dumps(house_i_to_write))
    write_read_csv.write_to_csv(path, "apartment_main_info.csv", apartment_fieldnames, json.dumps(apartment_i_to_write))


if __name__ == "__main__":
    print(__name__)
    _main()

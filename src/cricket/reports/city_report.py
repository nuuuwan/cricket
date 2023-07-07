from cricket.core import CITY_TO_COUNTRY, ODI


def main():
    odis = ODI.load_list()

    city_to_n = {}
    for odi in odis:
        city = odi.city
        city_to_n[city] = city_to_n.get(city, 0) + 1

    for city, n in sorted(city_to_n.items(), key=lambda x: x[1]):
        country = CITY_TO_COUNTRY.get(city)
        print(n, city, country)


if __name__ == "__main__":
    main()

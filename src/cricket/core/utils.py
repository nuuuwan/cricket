from cricket.core.VENUE_TO_CITY import VENUE_TO_CITY


def extract_city(info):
    city = info.get('city')
    if city is not None:
        return city

    venue = info.get('venue')
    if venue is None:
        raise Exception("No city or venue found: " + info)

    city = VENUE_TO_CITY.get(info.get('venue'))
    if city is not None:
        return city
    raise Exception("Unknown venue: " + venue)

import csv
from geopy.distance import vincenty
import requests


def find_closest(markets):
    markets = map(add_distance_info, markets)
    return min(markets, key=lambda x: x['dist'])


def add_distance_info(market):
    market['dist'] = vincenty(
        (market['X'], market['Y']),
        (-75.1991014, 39.9567835)
    ).miles
    return market


def get_farmers_market_data(url):
    response = requests.get(url, stream=True)
    markets = csv.DictReader(response.iter_lines(decode_unicode=True), delimiter=',')
    return list(markets)


def load_markets():
    pass


if __name__ == '__main__':
    print(find_closest())

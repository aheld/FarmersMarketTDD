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
    response.encoding = 'utf-8-sig'
    markets = csv.DictReader(response.iter_lines(decode_unicode=True),
                             delimiter=',')
    return list(markets)


def main():
    url = 'http://data.phl.opendata.arcgis.com/datasets/0707c1f31e2446e881d680b0a5ee54bc_0.csv' #noqa
    markets = get_farmers_market_data(url)
    closest = find_closest(markets)
    return closest


if __name__ == '__main__':
    print(main())

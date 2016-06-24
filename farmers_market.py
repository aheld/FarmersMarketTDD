import csv
import sys
from geopy.distance import vincenty
import requests


def find_closest(markets, coordinates):
    def find_this_market(market):
        return add_distance_info(market, coordinates)
    markets = list(map(find_this_market, markets))
    writer = csv.DictWriter(open('testout.csv','w'),
        fieldnames=markets[0].keys())
    writer.writeheader()
    writer.writerows(markets)

    return min(markets, key=lambda x: x['dist'])


def add_distance_info(market, coordinates):
    market['dist'] = vincenty(
        (market['X'], market['Y']),
        coordinates
    ).miles
    return market


def get_farmers_market_data(url):
    response = requests.get(url, stream=True)
    response.encoding = 'utf-8-sig'
    markets = csv.DictReader(response.iter_lines(decode_unicode=True),
                             delimiter=',')
    return list(markets)


def main(target):
    config = {'philly':{
            'url': 'http://data.phl.opendata.arcgis.com/datasets/0707c1f31e2446e881d680b0a5ee54bc_0.csv', #noqa
            'location':  (-75.1991014, 39.9567835)},
            'houston':{
            'url': 'http://data.phl.opendata.arcgis.com/datasets/0707c1f31e2446e881d680b0a5ee54bc_0.csv', #noqa
            'location':  (-95.3654083, 29.7542307)}
        }
    markets = get_farmers_market_data(config[target]['url'])
    closest = find_closest(markets, config[target]['location'])
    return closest


if __name__ == '__main__':
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = 'philly'
    print(main(target))

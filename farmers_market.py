from geopy.distance import vincenty

def find_closest(markets):
    markets = map(add_distance_info, markets)        
    return min(markets, key=lambda x: x['dist'])

def add_distance_info(market):
    market['dist'] = vincenty(
        (market['X'], market['Y']),
        (-75.1991014,39.9567835)
    ).miles
    return market

if __name__ == '__main__':
     print(get_farmers_data())

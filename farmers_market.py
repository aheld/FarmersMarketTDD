import csv
import requests
from geopy.distance import vincenty

CSV_URL = 'http://data.phl.opendata.arcgis.com/datasets/0707c1f31e2446e881d680b0a5ee54bc_0.csv'

def get_farmers_data():
    request = requests.get(CSV_URL, stream=True)
    request.encoding = 'utf-8-sig'
    markets = csv.DictReader(request.iter_lines(decode_unicode=True), delimiter=',')
    return list(markets)
        
def find_nearest(farmers_markets):
    market_street = (39.95654, -75.19631)
    records = []
    for rec in farmers_markets:
        lat_log = (rec["Y"], rec["X"])
        rec['dist'] = vincenty(market_street, lat_log).miles
        if rec['dist'] < 1:
            records.append(rec)
    return records


if __name__ == '__main__':
     for nearby_market in find_nearest(get_farmers_data()):
        print('{0:25} at {1:100}'.format(nearby_market['NAME'], 
                                nearby_market['ADDRESS']))

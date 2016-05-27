import csv
import requests
from geopy.distance import vincenty

CSV_URL = 'http://data.phl.opendata.arcgis.com/datasets/0707c1f31e2446e881d680b0a5ee54bc_0.csv'

def get_farmers_data():
    download = requests.get(CSV_URL, stream=True)
    cr = csv.DictReader((x.decode('utf-8-sig') 
                         for x in download.iter_lines()
                         ), delimiter=',')
    my_list = list(cr)
    return my_list
        
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
     print( find_nearest(get_farmers_data()))

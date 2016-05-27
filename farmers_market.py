import csv
import requests

CSV_URL = 'http://data.phl.opendata.arcgis.com/datasets/0707c1f31e2446e881d680b0a5ee54bc_0.csv'

def get_farmers_data():
    request = requests.get(CSV_URL, stream=True)
    markets = csv.DictReader(request.iter_lines(decode_unicode=True), delimiter=',')
    return list(markets)
        
if __name__ == '__main__':
     print(get_farmers_data())

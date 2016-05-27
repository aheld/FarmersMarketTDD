import csv
import requests

CSV_URL = 'http://data.phl.opendata.arcgis.com/datasets/0707c1f31e2446e881d680b0a5ee54bc_0.csv'

def get_farmers_data():
    download = requests.get(CSV_URL, stream=True)
    cr = csv.DictReader(download.iter_lines(decode_unicode='utf-8'), delimiter=',')
    my_list = list(cr)
    return my_list
        
if __name__ == '__main__':
     print(get_farmers_data())

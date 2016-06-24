from unittest import TestCase
from unittest.mock import patch
import responses

from farmers_market import (add_distance_info, find_closest,
                            get_farmers_market_data, main)


class TestMarkets(TestCase):
    def setUp(self):
        self.sample_market_data = [
                {'X': -75.17270125,
                 'Y': 39.94084192,
                 'NAME': '18th and Christian*'},
                {'X': -75.20926373,
                 'Y': 39.94955888,
                 'NAME': 'Clark Park*'}
                ]

    def test_decorate_market(self):
        sample_market = {'X': -75.20926373,
                         'Y': 39.94955888}
        assert 'dist' not in sample_market.keys()

        decorated = add_distance_info(sample_market, 
                    (-75.1991014, 39.9567835))
        assert 'dist' in decorated.keys()

    def test_find_dist(self):
        clark_park = add_distance_info(self.sample_market_data[1],
        (-75.1991014, 39.9567835))
        assert clark_park['dist'] < 1

        christian = add_distance_info(self.sample_market_data[0],
        (-75.1991014, 39.9567835))
        assert christian['dist'] > 1

    def test_find_the_closest(self):
        closest_park = find_closest(self.sample_market_data,(-75.1991014, 39.9567835) )
        assert closest_park['NAME'] == 'Clark Park*'


class TestMarketsLoader(TestCase):

    @responses.activate
    def test_can_load_market(self):
        CSV_URL = 'http://data.phl.opendata.arcgis.com/datasets/0707c1f31e2446e881d680b0a5ee54bc_0.csv' #noqa
        test_csv = open('farmers_market_test.csv', encoding='utf-8').read()
        responses.add(responses.GET, CSV_URL,
                      body=test_csv, status=200,
                      stream=True)
        market_data = get_farmers_market_data(CSV_URL)
        assert market_data == TEST_CSV_DATA


class TestMarketsEndToEnd(TestCase):

    @responses.activate
    def test_main(self):
        CSV_URL = 'http://data.phl.opendata.arcgis.com/datasets/0707c1f31e2446e881d680b0a5ee54bc_0.csv' #noqa
        test_csv = open('farmers_market_test.csv', encoding="utf-8").read()
        responses.add(responses.GET, CSV_URL,
                      body=test_csv, status=200,
                      stream=True)
        assert main('philly')['NAME'] == '29th & Wharton*' 


    @responses.activate
    def test_mainfix(self):
        CSV_URL = 'http://data.phl.opendata.arcgis.com/datasets/0707c1f31e2446e881d680b0a5ee54bc_0.csv' #noqa
        test_csv = open('farmers_market_testfix.csv').read()
        responses.add(responses.GET, CSV_URL,
                      body=test_csv, status=200,
                      stream=True)
        assert main('philly')['NAME'] == '29th & Wharton*' 



TEST_CSV_DATA = [{'ADDRESS': '18th and Christian St', 'MONTHS': 'June - November', 'DAY': 'Thurs', 'ADDRESS_NOTES': 'at the YMCA', 'ACCEPT_PHILLY_FOOD_BUCKS': 'Y', 'Y': '39.940841916695057', 'TIME': '3-7pm', 'ACCEPT_FMNP': 'Y', 'OBJECTID': '1', 'ACCEPT_SNAP_ACCESS': 'Y', 'NEIGHBORHOOD': 'South', 'X': '-75.172701252171919', 'MAJOR_BUS_SUBWAY_ROUTES': '2, 17', 'NAME': '18th and Christian*', 'ZIP': '19146'}, {'ADDRESS': '22nd and Tasker St', 'MONTHS': 'End June/Early July – November', 'DAY': 'Tues', 'ADDRESS_NOTES': '', 'ACCEPT_PHILLY_FOOD_BUCKS': 'Y', 'Y': '39.932178999784682', 'TIME': '2-6pm', 'ACCEPT_FMNP': 'Y', 'OBJECTID': '2', 'ACCEPT_SNAP_ACCESS': 'Y', 'NEIGHBORHOOD': 'South', 'X': '-75.181423846357561', 'MAJOR_BUS_SUBWAY_ROUTES': '7, 29', 'NAME': '22nd & Tasker*', 'ZIP': '19145'}, {'ADDRESS': '26th St and Allegheny Ave', 'MONTHS': 'July 8th - November', 'DAY': 'Wed', 'ADDRESS_NOTES': '', 'ACCEPT_PHILLY_FOOD_BUCKS': 'Y', 'Y': '40.004104443998102', 'TIME': '1-5pm', 'ACCEPT_FMNP': 'Y', 'OBJECTID': '3', 'ACCEPT_SNAP_ACCESS': 'Y', 'NEIGHBORHOOD': 'North', 'X': '-75.172283714309913', 'MAJOR_BUS_SUBWAY_ROUTES': '48, 60', 'NAME': '26th and Allegheny*', 'ZIP': '19129'}, {'ADDRESS': '29th and Wharton St', 'MONTHS': 'June – November', 'DAY': 'Tues', 'ADDRESS_NOTES': '', 'ACCEPT_PHILLY_FOOD_BUCKS': 'Y', 'Y': '39.937297083281905', 'TIME': '2-6pm', 'ACCEPT_FMNP': 'Y', 'OBJECTID': '4', 'ACCEPT_SNAP_ACCESS': 'Y', 'NEIGHBORHOOD': 'South', 'X': '-75.1920388833027', 'MAJOR_BUS_SUBWAY_ROUTES': '12, 64', 'NAME': '29th & Wharton*', 'ZIP': '19146'}, {'ADDRESS': '33rd & Diamond Sts', 'MONTHS': 'June -November', 'DAY': 'Thurs', 'ADDRESS_NOTES': 'In front of Mander Playground', 'ACCEPT_PHILLY_FOOD_BUCKS': 'Y', 'Y': '39.988682579276201', 'TIME': '2-6pm', 'ACCEPT_FMNP': 'Y', 'OBJECTID': '5', 'ACCEPT_SNAP_ACCESS': 'Y', 'NEIGHBORHOOD': 'North', 'X': '-75.187063935483323', 'MAJOR_BUS_SUBWAY_ROUTES': '7, 32, 39, 54, 61', 'NAME': '33rd & Diamond*', 'ZIP': '19121'}, {'ADDRESS': '4th St & Lehigh Ave', 'MONTHS': 'July 7th - November', 'DAY': 'Tues', 'ADDRESS_NOTES': '', 'ACCEPT_PHILLY_FOOD_BUCKS': 'Y', 'Y': '39.991869006387248', 'TIME': '1-5pm', 'ACCEPT_FMNP': 'Y', 'OBJECTID': '6', 'ACCEPT_SNAP_ACCESS': 'Y', 'NEIGHBORHOOD': 'North', 'X': '-75.138355706471373', 'MAJOR_BUS_SUBWAY_ROUTES': '47, 54', 'NAME': '4th and Lehigh*', 'ZIP': '19133'}, {'ADDRESS': '52nd St and Haverford Ave', 'MONTHS': 'Early July – November', 'DAY': 'Wed', 'ADDRESS_NOTES': '', 'ACCEPT_PHILLY_FOOD_BUCKS': 'Y', 'Y': '39.964913169362674', 'TIME': '1-5pm', 'ACCEPT_FMNP': 'Y', 'OBJECTID': '7', 'ACCEPT_SNAP_ACCESS': 'Y', 'NEIGHBORHOOD': 'West ', 'X': '-75.224594826060098', 'MAJOR_BUS_SUBWAY_ROUTES': '30, 52', 'NAME': '52nd & Haverford*', 'ZIP': '19139'}, {'ADDRESS': '58th and Chester Street', 'MONTHS': 'June -November', 'DAY': 'Wed', 'ADDRESS_NOTES': '', 'ACCEPT_PHILLY_FOOD_BUCKS': 'Y', 'Y': '39.935749877733862', 'TIME': '2-6pm', 'ACCEPT_FMNP': 'Y', 'OBJECTID': '8', 'ACCEPT_SNAP_ACCESS': 'Y', 'NEIGHBORHOOD': 'Southwest', 'X': '-75.228537854068307', 'MAJOR_BUS_SUBWAY_ROUTES': '13 trolley, G', 'NAME': '58th & Chester*', 'ZIP': '19143'}, {'ADDRESS': '8th & Poplar Sts, 19123', 'MONTHS': 'May  – November', 'DAY': 'Wed', 'ADDRESS_NOTES': '', 'ACCEPT_PHILLY_FOOD_BUCKS': '', 'Y': '39.967988514708807', 'TIME': '3-6pm', 'ACCEPT_FMNP': 'Y', 'OBJECTID': '9', 'ACCEPT_SNAP_ACCESS': 'Y', 'NEIGHBORHOOD': 'Lower North', 'X': '-75.150519176937692', 'MAJOR_BUS_SUBWAY_ROUTES': '47', 'NAME': '8th & Poplar', 'ZIP': '19123'}, {'ADDRESS': '54th & Lindbergh Blvd', 'MONTHS': 'June-November', 'DAY': 'Thurs', 'ADDRESS_NOTES': 'In front of Bartrams Village Apartments', 'ACCEPT_PHILLY_FOOD_BUCKS': '', 'Y': '39.932759682718938', 'TIME': '3:30-7pm', 'ACCEPT_FMNP': 'Y', 'OBJECTID': '10', 'ACCEPT_SNAP_ACCESS': 'Y ', 'NEIGHBORHOOD': 'Southwest', 'X': '-75.216078112569335', 'MAJOR_BUS_SUBWAY_ROUTES': '36 trolley', 'NAME': 'Bartram’s Farm Market', 'ZIP': '19143'}]  # noqa
from unittest import TestCase
from unittest.mock import patch

from farmers_market import add_distance_info, find_closest


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

        decorated = add_distance_info(sample_market)
        assert 'dist' in decorated.keys()

    def test_find_dist(self):
        clark_park = add_distance_info(self.sample_market_data[1])
        assert clark_park['dist'] < 1

        christian = add_distance_info(self.sample_market_data[0])
        assert christian['dist'] > 1

    def test_find_the_closest(self):
        closest_park = find_closest(self.sample_market_data)
        assert closest_park['NAME'] == 'Clark Park*'


class TestMarketsLoader(TestCase):

    @patch('farmers_market.add_distance_info')
    def test_load_market(self, mock_add_distance_info):
        find_closest({"bad": "data"})
        assert mock_add_distance_info.called
        assert mock_add_distance_info.assert_called_once_with([{'a': 1},
                                                               {'b': 2}])

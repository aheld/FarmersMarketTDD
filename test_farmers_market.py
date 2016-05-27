import requests
import responses
from unittest.mock import MagicMock, patch

from farmers_market import get_farmers_data, CSV_URL


@responses.activate
def test_my_api():
    sample_data = open('farmers_market_test.csv', 'rb').read()
    responses.add(responses.GET, CSV_URL,
                  body=sample_data, status=200,
                  content_type='text/csv; charset=utf-8',
                  stream=True
                  )

    farm_list = get_farmers_data()
    assert len(farm_list) == 10
    assert farm_list[0]["NAME"] == "18th and Christian*"
    assert farm_list[1]["NAME"] == "22nd & Tasker*"
  
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == CSV_URL
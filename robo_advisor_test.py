import pytest
import os

from app.robo_advisor import to_usd, get_response

def test_to_usd():   # to test price formatting
    assert to_usd(18.50) == "$18.50"

    assert to_usd(18.5) == "$18.50"

    assert to_usd(18.5099999) == "$18.51"
    
    assert to_usd(3195849.65) == "$3,195,849.65"

def test_get_response(): #> Issuing API Requests
    symbol = "AMZN"

    parsed_response = get_response(symbol)

    assert isinstance(parsed_response, dict)
    assert "Meta Data" in parsed_response.keys()
    assert "Time Series (Daily)" in parsed_response.keys()
    assert parsed_response["Meta Data"]["2. Symbol"] == symbol



#def test_write_to_csv():
#
#    example_rows = [
#        {"timestamp": "2019-06-21", "open": "1916.1000", "high": "1925.9500", "low": "1907.5800", "close": "1911.3000", "volume": "3906945"},
#        {"timestamp": "2019-06-20", "open": "1933.3300", "high": "1935.2000", "low": "1905.8000", "close": "1918.1900", "volume": "3217153"},
#        {"timestamp": "2019-06-19", "open": "1907.8400", "high": "1919.5800", "low": "1892.4700", "close": "1908.7900", "volume": "2895347"},
#        {"timestamp": "2019-06-18", "open": "1901.3500", "high": "1921.6700", "low": "1899.7900", "close": "1901.3700", "volume": "3895728"},
#        {"timestamp": "2019-06-17", "open": "1876.5000", "high": "1895.6900", "low": "1875.4500", "close": "1886.0300", "volume": "2634342"}
#        
#    ]
#
#    file_name = symbol +".csv"
#    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices_" + file_name)
#
#    if os.path.isfile(csv_filepath):
#        os.remove(csv_filepath)
#
#    assert os.path.isfile(csv_filepath) == False # just making sure the test was setup properly
#
#    # INVOCATION
#
#    result = write_to_csv(example_rows, csv_filepath)
#
#    # EXPECTATIONS
#
#    assert result == True
#    assert os.path.isfile(csv_filepath) == True
#    # TODO: consider also testing the file contents!
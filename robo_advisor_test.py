import pytest
import os

from app.robo_advisor import to_usd, get_response

def test_to_usd():   # to test price formatting
    assert to_usd(18.50) == "$18.50"

    assert to_usd(18.5) == "$18.50"

    assert to_usd(18.5099999) == "$18.51"
    
    assert to_usd(3195849.65) == "$3,195,849.65"

def test_get_response(): #> to test issuing API Requests
    symbol = "AMZN"

    parsed_response = get_response(symbol)

    assert isinstance(parsed_response, dict)
    assert "Meta Data" in parsed_response.keys()
    assert "Time Series (Daily)" in parsed_response.keys()
    assert parsed_response["Meta Data"]["2. Symbol"] == symbol



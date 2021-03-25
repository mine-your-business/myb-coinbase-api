# DISCLAIMER: Without the presence of a "sandbox" API like Coinbase Pro provides,
# this will only be testing "public" endpoints that don't require
# authentication
import pytest
from datetime import datetime, timedelta
import time
import os

from coinbase import CoinbaseApi


@pytest.fixture(scope='module')
def client():
    return CoinbaseApi(
        api_url="https://api.coinbase.com",
        verbose=True
    )    

# A bit hacky but fullfills the need of allowing for code 
# to be run before (or after) each test
@pytest.fixture(autouse=True)
def run_around_tests():
    # Delay at the start of each test because apparently
    # the public request endpoints may require a CAPTCHA
    # if you make requests too quickly
    time.sleep(0.1)
    # A test function will be run at this point
    yield
    # Code that will run after each test


# @pytest.fixture(scope='module')
# def authed_client():
#     return CoinbaseApi(
#         os.environ.get('COINBASE_API_KEY'),
#         os.environ.get('COINBASE_API_KEY_SECRET'),
#         api_url="https://api.coinbase.com",
#         verbose=True
#     )


@pytest.mark.usefixtures('client')
class TestClient(object):

    def test_get_buy_price_gets_eth_prices(self, client):
        currency_pair = 'ETH-USD'

        price = client.get_buy_price(currency_pair)

        assert price is not None
        assert price.amount > 0
        assert price.currency == 'USD'

    def test_get_sell_price_gets_eth_price(self, client):
        currency_pair = 'ETH-USD'
        price = client.get_sell_price(currency_pair)
        assert price is not None
        assert price.amount > 0
        assert price.currency == 'USD'

    def test_get_spot_price_gets_eth_price(self, client):
        currency_pair = 'ETH-USD'
        price = client.get_spot_price(currency_pair)
        assert price is not None
        assert price.amount > 0
        assert price.currency == 'USD'

    def test_get_spot_price_gets_eth_price_for_date(self, client):
        currency_pair = 'ETH-USD'
        date = datetime.today() - timedelta(days=25)

        price = client.get_spot_price(currency_pair, date)

        assert price is not None
        assert price.amount > 0
        assert price.currency == 'USD'

    def test_get_server_time_gets_server_time(self, client):
        now = int(time.time())

        server_time = client.get_server_time()

        assert server_time is not None
        # Just check for presence - epoch is easier to test against
        assert server_time.iso is not None
        assert server_time.epoch > 0
        time_diff = server_time.epoch - now
        assert time_diff >= 0
        # number of seconds between the time before making the
        # request and the server's time
        # this could fail on occasion but generally shouldn't
        assert time_diff < 120

# @pytest.mark.usefixtures('authed_client')
# class TestAuthedClient(object):

#     def test_get_accounts(self, authed_client):
#         accounts = authed_client.list_accounts()

#         assert accounts is not None

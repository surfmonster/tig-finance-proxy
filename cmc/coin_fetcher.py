from influxdb.exceptions import InfluxDBClientError
from typing import Sequence
from cmc.coin import CoinInfo, BuiltInCoin
from datetime import datetime, timedelta
import requests, json
import dateutil.parser
import Config
from dto.quote_dto import ProxyQuote
from utils import coin_utils

measurement = Config.env('influxdb.quote.measurement')

# https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id=1&convert=USD&time_start=1201245530&time_end=1615218330

category = 'cryptocurrency'


class CoinFetcher:

    def __init__(self, ci: CoinInfo):
        self.info = ci

    def parseHistorical(self, s: datetime, e: datetime) -> Sequence[ProxyQuote]:
        url = self.info.getOhlcvHistoricalUrl(s, e)
        resp = requests.get(url)
        jr = json.loads(resp.text)
        idata = jr['data']['quotes']
        return [coin_utils.to_proxy_quote(q, self.info.symbol, self.info.name) for q in idata]

    def get_last_when_now(self) -> ProxyQuote:
        current_date = datetime.now()
        today_morning = datetime(current_date.year, current_date.month, current_date.day)
        before_day = today_morning + timedelta(days=-1)
        return self.parseHistorical(before_day, today_morning)[0]


def toFloat(i):
    ans = float(i)
    return ans


_fetcher_map = {}


def get_built_in(bi: BuiltInCoin) -> CoinFetcher:
    if bi not in _fetcher_map.keys():
        _f = CoinFetcher(bi.getCoinInfo())
        _fetcher_map[bi] = _f
    return _fetcher_map.get(bi)


if __name__ == '__main__':
    import unittest


    class SymbolTest(unittest.TestCase):
        def test_saveUntilNow(self):
            cf = CoinFetcher(BuiltInCoin.BTC.getCoinInfo())
            cf.saveUntilNow()
            print(cf)
            self.assertIsNotNone(cf)

        def test_getInitAt(self):
            cf = CoinFetcher(BuiltInCoin.BTC.getCoinInfo())
            ans = cf.getInitAt()
            print(ans)
            self.assertIsNotNone(ans)


    tests = [
        SymbolTest('test_saveUntilNow'),
        SymbolTest('test_getInitAt'),

    ]
    suite = unittest.TestSuite()
    suite.addTests(tests)

    runner = unittest.TextTestRunner()
    runner.run(suite)

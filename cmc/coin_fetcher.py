from datetime import datetime, timedelta
from typing import Sequence

import json
import requests

import Config
from cmc.coin import CoinInfo, BuiltInCoin
from dto.quote_dto import ProxyQuote
from utils import coin_utils

measurement = Config.env('influxdb.quote.measurement')

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

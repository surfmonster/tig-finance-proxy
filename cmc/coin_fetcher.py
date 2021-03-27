from influxdb.exceptions import InfluxDBClientError

from cmc.coin import CoinInfo, BuiltInCoin
from datetime import datetime, timedelta
import requests, json
from tsdb.influxdb_service import insertData, queryToPoints, deleteByTags
import dateutil.parser
import Config
from dto.quote_dto import ProxyQuote

measurement = Config.env('influxdb.quote.measurement')

# https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id=1&convert=USD&time_start=1201245530&time_end=1615218330

category = 'cryptocurrency'


class CoinFetcher:

    def __init__(self, ci: CoinInfo):
        self.info = ci

    def parseHistorical(self, s: datetime, e: datetime) ->:
        url = self.info.getOhlcvHistoricalUrl(s, e)
        resp = requests.get(url)
        jr = json.loads(resp.text)
        idata = jr['data']['quotes']
        return [self._to_proxy_quote(q) for q in idata]

    def get_last_when_now(self) -> ProxyQuote:
        current_date = datetime.now()
        today_morning = datetime(current_date.year, current_date.month, current_date.day)
        before_day = today_morning + timedelta(days=-1)
        return self._to_proxy_quote(self.parseHistorical(before_day, today_morning)[0])

    def saveInfluxDB(self, s: datetime, e: datetime):
        idata = self.parseHistorical(s, e)
        iList = [self._to_proxy_quote(q).to_point() for q in idata]
        insertData(iList)

    def deleteAll(self):
        deleteByTags(measurement=measurement, tags={
            "name": self.info.name
        })


def toFloat(i):
    ans = float(i)
    return ans


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

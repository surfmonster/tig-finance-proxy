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

    def parseHistorical(self, s: datetime, e: datetime):
        url = self.info.getOhlcvHistoricalUrl(s, e)
        resp = requests.get(url)
        jr = json.loads(resp.text)
        return jr['data']['quotes']

    def getInitAt(self):
        queryTemp = 'SELECT * FROM "quote" WHERE "category"=\'{0}\' AND "name" = \'{1}\'   ORDER BY time ASC LIMIT 1'
        qstr = queryTemp.format("cryptocurrency", self.info.name)
        try:
            points = queryToPoints(qstr, measurement)
            if len(points) <= 0:
                return dateutil.parser.parse(Config.env("coinmarketcap.init.time"))
        except InfluxDBClientError:
            pass
        lAt: datetime = dateutil.parser.parse(points[0]['time'])
        # lAt = lAt + timedelta(days=1)
        return lAt

    def check_regular_all(self):
        qsql = f'SELECT * FROM "quote" WHERE "category"=\'{category}\' AND "name" = \'{self.info.name}\' ORDER BY time ASC LIMIT 1'


    def get_last_when_now(self) -> ProxyQuote:
        current_date = datetime.now()
        today_morning = datetime(current_date.year, current_date.month, current_date.day)
        before_day = today_morning + timedelta(days=-1)
        return self._to_proxy_quote(self.parseHistorical(before_day, today_morning)[0])

    def saveUntilNow(self):
        sAt = self.getInitAt()
        eAt = datetime.now()
        self.saveInfluxDB(sAt, eAt)

    def saveInfluxDB(self, s: datetime, e: datetime):
        idata = self.parseHistorical(s, e)
        iList = [self._to_proxy_quote(q).to_point() for q in idata]
        insertData(iList)

    def deleteAll(self):
        deleteByTags(measurement=measurement, tags={
            "name": self.info.name
        })

    def _to_proxy_quote(self, q) -> ProxyQuote:
        ans = ProxyQuote()
        ans.symbol = self.info.symbol
        ans.name = self.info.name
        ans.category = 'cryptocurrency'

        ans.time_open = q['time_open']
        ans.time_close = q['time_close']
        ans.time_high = q['time_high']
        ans.time_low = q['time_low']
        vals = q['quote']['USD']
        ans.open = toFloat(vals['open'])
        ans.high = toFloat(vals['high'])
        ans.low = toFloat(vals['low'])
        ans.close = toFloat(vals['close'])
        ans.volume = toFloat(vals['volume'])
        ans.market_cap = toFloat(vals['market_cap'])
        ans.timestamp = dateutil.parser.parse(vals['timestamp'])
        ans.source = 'coinmarketcap'
        return ans


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

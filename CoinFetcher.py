from Coin import CoinInfo, BuiltInCoin
from datetime import datetime, date
from CMCBrowserUtils import getBrowser, WebDriverWait, EC, By
import requests, json
from InfluxDBService import Point, insertData
import dateutil.parser
import Config


# https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id=1&convert=USD&time_start=1201245530&time_end=1615218330

class CoinFetcher:

    def __init__(self, ci: CoinInfo):
        self.info = ci

    def goToHistoricalPage(self):
        bser = getBrowser()
        sd = date(2007, 1, 1)
        bser.get(self.info.getDateHistoricalUrl(sd, datetime.now()))
        WebDriverWait(bser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".reply-button"))).click()

    def parseOhlcvHistorical(self, s: datetime, e: datetime):
        url = self.info.getOhlcvHistoricalUrl(s, e)
        resp = requests.get(url)
        jr = json.loads(resp.text)
        return jr['data']['quotes']

    def saveInfluxDB(self, s: datetime, e: datetime):
        idata = self.parseOhlcvHistorical(s, e)
        iList = [self.toPoint(q) for q in idata]
        insertData(iList)

    def toPoint(self, q):
        # {
        #     "time_open": "2021-03-04T00:00:00.000Z",
        #     "time_close": "2021-03-04T23:59:59.999Z",
        #     "time_high": "2021-03-04T02:11:49.000Z",
        #     "time_low": "2021-03-04T20:13:59.000Z",
        #     "quote": {
        #         "USD": {
        #             "open": 50522.30503036,
        #             "high": 51735.09105293,
        #             "low": 47656.92904603,
        #             "close": 48561.1661539,
        #             "volume": 52343816679.73,
        #             "market_cap": 905414104807.24,
        #             "timestamp": "2021-03-04T23:59:59.999Z"
        #         }
        #     }
        # }
        vals = q['quote']['USD']
        tt = dateutil.parser.parse(vals['timestamp'])
        point = Point(measurement=Config.env('influxdb.quote.measurement'),
                      tags={
                          "symbol": self.info.symbol,
                          "name": self.info.name,
                          "category": 'cryptocurrency'
                      },
                      fields={
                          "time_open": q['time_open'],
                          "time_close": q['time_close'],
                          "time_high": q['time_high'],
                          "time_low": q['time_low'],
                          "open": vals['open'],
                          "high": vals['high'],
                          "low": vals['low'],
                          "close": vals['close'],
                          "volume": vals['volume'],
                          "market_cap": vals['market_cap'],
                      },
                      time=tt
                      )
        return point


if __name__ == '__main__':
    import unittest


    class SymbolTest(unittest.TestCase):
        def test_saveInfluxDB(self):
            cf = CoinFetcher(BuiltInCoin.BTC.getCoinInfo())
            cf.saveInfluxDB(datetime(2021, 3, 3), datetime.now())
            print(cf)
            self.assertIsNotNone(cf)


    tests = [
        SymbolTest('test_saveInfluxDB'),

    ]
    suite = unittest.TestSuite()
    suite.addTests(tests)

    runner = unittest.TextTestRunner()
    runner.run(suite)

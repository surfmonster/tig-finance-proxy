from Coin import CoinInfo, BuiltInCoin
from datetime import datetime, date
from CMCBrowserUtils import getBrowser, WebDriverWait, EC, By
import requests, json


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


if __name__ == '__main__':
    import unittest


    class SymbolTest(unittest.TestCase):
        def test_parseOhlcvHistorical(self):
            cf = CoinFetcher(BuiltInCoin.BTC.getCoinInfo())
            ans = cf.parseOhlcvHistorical(datetime(2021, 3, 3), datetime.now())
            print(ans)
            self.assertIsNotNone(ans)


    tests = [
        SymbolTest('test_parseOhlcvHistorical'),

    ]
    suite = unittest.TestSuite()
    suite.addTests(tests)

    runner = unittest.TextTestRunner()
    runner.run(suite)

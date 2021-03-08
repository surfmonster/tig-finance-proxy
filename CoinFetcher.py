from Coin import CoinInfo, BuiltInCoin
from datetime import datetime, date
from CMCBrowserUtils import getBrowser, WebDriverWait, EC, By

# https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id=1&convert=USD&time_start=1201245530&time_end=1615218330

class CoinFetcher:

    def __init__(self, ci: CoinInfo):
        self.info = ci

    def goToHistoricalPage(self):
        bser = getBrowser()
        sd = date(2007, 1, 1)
        bser.get(self.info.getDateHistoricalUrl(sd, datetime.now()))
        WebDriverWait(bser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".reply-button"))).click()


if __name__ == '__main__':
    import unittest


    class SymbolTest(unittest.TestCase):
        def test_goToHistoricalPage(self):
            cf = CoinFetcher(BuiltInCoin.BTC.getCoinInfo())
            cf.goToHistoricalPage()
            print(cf)
            self.assertIsNotNone(cf)


    tests = [
        SymbolTest('test_goToHistoricalPage'),

    ]
    suite = unittest.TestSuite()
    suite.addTests(tests)

    runner = unittest.TextTestRunner()
    runner.run(suite)

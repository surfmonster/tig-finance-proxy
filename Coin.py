import requests
from bs4 import BeautifulSoup, Tag
from datetime import datetime
from enum import Enum
import time

HOST = 'https://coinmarketcap.com/'
COINS_PAGE_URL: str = HOST + 'coins/?page=%i'
Historical_SUBFIX = 'historical-data/'


class CoinInfo:

    def __init__(self, n: str, s: str, i: int):
        self.name = n
        self.symbol = s
        self.id = i
        self.path = 'currencies/' + self.name + '/'

    def getHistoricalPath(self):
        return self.path + Historical_SUBFIX

    def getHistoricalUrl(self):
        return HOST + self.getHistoricalPath()

    def getDateHistoricalUrl(self, s: datetime, e: datetime):
        fomt = '%Y/%m/%d'
        temp = self.getHistoricalUrl() + '?start={0}&end={1}'
        ans = temp.format(s.strftime(fomt), e.strftime(fomt))
        return ans

    def getOhlcvHistoricalUrl(self, s: datetime, e: datetime):
        sts = int( s.timestamp())
        ets = int(e.timestamp())
        temp = 'https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id={0}&convert=USD&time_end={1}&time_start={2}'
        return temp.format(self.id, ets,sts)


class BuiltInCoin(Enum):

    def __init__(self, n: str, s: str, i: int):
        self.pid = n
        self.id = i
        self.symbol = s

    BTC = ('bitcoin', 'BTC', 1)
    ETH = ('ethereum', 'ETH', 3)

    def getCoinInfo(self):
        return CoinInfo(self.pid, self.symbol, self.id)


def loadSymbols():
    curPidx = 0
    ans = []
    ca = []
    while (ca != None):
        ca = loadSymbolsByPage(curPidx)
        curPidx += 1
        ans.extend(ca)

    return ans


def loadSymbolsByPage(page: int):
    ans = []

    try:
        resp = requests.get(getPageUrl(page))
        soup = BeautifulSoup(resp.text, 'html5lib')
        tb = soup.find('table', 'cmc-table')
        es = tb.find_all('tr')
        for e in es:
            try:
                ans.append(parseCoinInfo(e))
            except IndexError:
                print('may it`s th')
        return ans
    except AttributeError:
        return ans


def parseCoinInfo(e: Tag):
    cols = e.find_all('td')
    nameCol = cols[2]
    nameInfos = nameCol.find_all('span')
    ans = CoinInfo(nameInfos[1].text, nameInfos[2].text)
    ans.path = nameCol.find('a')['href']
    print(ans.path)
    return ans


def getPageUrl(n: int):
    return COINS_PAGE_URL % n


if __name__ == '__main__':
    import unittest


    class SymbolTest(unittest.TestCase):
        def test_getPageUrl(self):
            sp = getPageUrl(10)
            print(sp)
            self.assertIsNotNone(sp)

        def test_loadSymbolsByPage(self):
            result = loadSymbolsByPage(1)
            print(result)
            self.assertIsNotNone(result)
            for r in result:
                print(r.getDateHistoricalUrl(datetime.now(), datetime.now()))

        def test_loadSymbols(self):
            result = loadSymbols()
            print(result)
            self.assertIsNotNone(result)

        def test_getCoinPageUrl(self):
            c = BuiltInCoin.BTC
            st = datetime(2021,3,3)
            u = c.getCoinInfo().getOhlcvHistoricalUrl(st, datetime.now())
            print(u)
            self.assertIsNotNone(u)

        def test_getEnumCoinInfo(self):
            bc = BuiltInCoin.BTC
            print(bc.getCoinInfo().path)
            self.assertIsNotNone(bc)


    tests = [
        SymbolTest('test_getPageUrl'),
        SymbolTest('test_getCoinPageUrl'),
        SymbolTest('test_getEnumCoinInfo')
    ]
    suite = unittest.TestSuite()
    suite.addTests(tests)

    runner = unittest.TextTestRunner()
    runner.run(suite)

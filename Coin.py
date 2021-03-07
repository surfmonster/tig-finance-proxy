import requests
from bs4 import BeautifulSoup, Tag

HOST = 'https://coinmarketcap.com/'
COINS_PAGE_URL: str = HOST + 'coins/?page=%i'
Historical_SUBFIX = 'historical-data/'


class CoinInfo:
    def __init__(self, n: str):
        self.name = n
        self.symbol = ''
        self.path = ''

    def getHistoricalPath(self):
        return self.path + '/' + Historical_SUBFIX

    def getHistoricalUrl(self):
        return HOST + self.getHistoricalPath()


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
    ans = CoinInfo(nameInfos[1].text)
    ans.symbol = nameInfos[2].text
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

        def test_loadSymbols(self):
            result = loadSymbols()
            print(result)
            self.assertIsNotNone(result)


    tests = [
        SymbolTest('test_getPageUrl'),
        SymbolTest('test_loadSymbolsByPage')
    ]
    suite = unittest.TestSuite()
    suite.addTests(tests)

    runner = unittest.TextTestRunner()
    runner.run(suite)

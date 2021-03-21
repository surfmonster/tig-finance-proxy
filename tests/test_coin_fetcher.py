import datetime

from cmc.coin import BuiltInCoin
from cmc.coin_fetcher import CoinFetcher


def test_fetch_today():
    cinfo = BuiltInCoin.BTC.getCoinInfo()
    fetcher = CoinFetcher(cinfo)
    lastData = fetcher.getLast()
    print(lastData.__dict__)

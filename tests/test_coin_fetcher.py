import datetime

from cmc.coin import BuiltInCoin
from cmc.coin_fetcher import CoinFetcher


def test_fetch_today():
    cinfo = BuiltInCoin.BTC.getCoinInfo()
    fetcher = CoinFetcher(cinfo)
    lastData = fetcher.get_last_when_now()
    print(lastData.__dict__)

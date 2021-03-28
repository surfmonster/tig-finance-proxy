from collections import Sequence
from datetime import datetime

from cmc.coin import BuiltInCoin
from dto.quote_dto import ProxyQuote
from tsdb import coin_dao

dao = coin_dao.get_built_in(BuiltInCoin.BTC)


def test_save():
    pq = ProxyQuote()
    _t = '_test'
    pq.symbol = _t
    pq.name = _t
    pq.category = _t
    pq.source = _t
    pq.open = 999
    pq.timestamp = datetime.now()
    qs = [pq]
    dao.save_all(quotes=qs)

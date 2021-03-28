from datetime import datetime
from typing import Sequence

import dateutil
from influxdb.exceptions import InfluxDBClientError

import Config
from cmc.coin import CoinInfo, BuiltInCoin
from dto.quote_dto import ProxyQuote
from tsdb.base_dao import BaseDao
from tsdb.influxdb_service import queryToPoints, insertData

measurement = Config.env('influxdb.quote.measurement')
category = 'cryptocurrency'


class CoinDao(BaseDao):

    def __init__(self, ci: CoinInfo):
        self.info = ci
        super().__init__(category, ci.name)

    def save_all(self, quotes: Sequence[ProxyQuote]):
        insertData(quotes)

    def get_init_at(self) -> datetime:
        return dateutil.parser.parse(Config.env("coinmarketcap.init.time"))


_dao_map = {}


def get_built_in(bie: BuiltInCoin) -> CoinDao:
    if bie not in _dao_map.keys():
        _dao = CoinDao(bie.getCoinInfo())
        _dao_map[bie] = _dao
    return _dao_map.get(bie)

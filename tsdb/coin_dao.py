from datetime import datetime

import dateutil
from influxdb.exceptions import InfluxDBClientError

import Config
from cmc.coin import CoinInfo
from tsdb.base_dao import BaseDao
from tsdb.influxdb_service import queryToPoints

measurement = Config.env('influxdb.quote.measurement')
category = 'cryptocurrency'


class CoinDao(BaseDao):
    def __init__(self, ci: CoinInfo):
        self.info = ci
        super().__init__(category, ci.name)

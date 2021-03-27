from abc import ABCMeta, abstractmethod
from datetime import datetime

import dateutil
from influxdb.exceptions import InfluxDBClientError

import Config
from cmc.coin import CoinInfo
from tsdb.influxdb_service import queryToPoints

measurement = Config.env('influxdb.quote.measurement')


class BaseDao(metaclass=ABCMeta):
    def __init__(self, category: str, name: str):
        self.category = category
        self.name = name

    def getInitAt(self):
        queryTemp = 'SELECT * FROM "quote" WHERE "category"=\'{0}\' AND "name" = \'{1}\'   ORDER BY time ASC LIMIT 1'
        qstr = queryTemp.format("cryptocurrency", self.info.name)
        try:
            points = queryToPoints(qstr, measurement)
            if len(points) <= 0:
                return dateutil.parser.parse(Config.env("coinmarketcap.init.time"))
            else:
                return dateutil.parser.parse(points[0]['time'])
        except InfluxDBClientError:
            return dateutil.parser.parse(Config.env("coinmarketcap.init.time"))

    def saveUntilNow(self):
        sAt = self.getInitAt()
        eAt = datetime.now()
        self.saveInfluxDB(sAt, eAt)

    def check_regular_all(self):
        qsql = f'SELECT * FROM "quote" WHERE "category"=\'{self.category}\' AND "name" = \'{self.name}\' ORDER BY time ASC'
        points = queryToPoints(qsql, measurement)
        lastAt: datetime = None
        for point in points:
            if lastAt is None:
                lastAt = point.timestamp
                continue

    @abstractmethod
    def save_all(self, quotes: list,in_type:type):
        pass

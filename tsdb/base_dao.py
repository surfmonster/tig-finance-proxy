from typing import Callable

from abc import ABCMeta, abstractmethod
from datetime import datetime

import dateutil
from influxdb.exceptions import InfluxDBClientError

import Config
from constant.enums import AscDesc
from dto.quote_dto import ProxyQuote
from tsdb.influxdb_service import queryToPoints, deleteByTags

measurement = Config.env('influxdb.quote.measurement')


class BaseDao(metaclass=ABCMeta):
    def __init__(self, category: str, name: str):
        self.category = category
        self.name = name

    def get_first_save_at(self):
        return self.get_node_save_at(AscDesc.ASC)

    def get_Last_save_at(self):
        return self.get_node_save_at(AscDesc.DESC)

    def get_node_save_at(self, asc_desc: AscDesc):
        queryTemp = 'SELECT * FROM "quote" WHERE "category"=\'{0}\' AND "name" = \'{1}\' ORDER BY time {2} LIMIT 1'
        qstr = queryTemp.format("cryptocurrency", self.info.name, asc_desc.value)
        try:
            points = queryToPoints(qstr, measurement)
            if len(points) <= 0:
                return self.get_init_at()
            else:
                return points[0].timestamp
        except InfluxDBClientError:
            return self.get_init_at()

    def saveUntilNow(self):
        sAt = self.get_first_save_at()
        eAt = datetime.now()
        self.saveInfluxDB(sAt, eAt)

    def check_regular_all(self, row_apply: Callable[[datetime, datetime, datetime, ProxyQuote], datetime]):
        qsql = f'SELECT * FROM "quote" WHERE "category"=\'{self.category}\' AND "name" = \'{self.name}\' ORDER BY time ASC'
        points = queryToPoints(qsql, measurement)
        init_at = self.get_init_at()
        now = datetime.now()
        last_check_at: datetime = None
        for point in points:
            last_check_at = row_apply(init_at, now, last_check_at, point)

    def deleteAll(self):
        deleteByTags(measurement=measurement, tags={
            "name": self.info.name
        })

    @abstractmethod
    def save_all(self, quotes: list, in_type: type):
        pass

    @abstractmethod
    def get_init_at(self) -> datetime:
        pass

import dateutil
from influxdb.exceptions import InfluxDBClientError

import Config
from cmc.coin import CoinInfo
from tsdb.influxdb_service import queryToPoints

measurement = Config.env('influxdb.quote.measurement')


class CoinDao:
    def __init__(self, ci: CoinInfo):
        self.info = ci

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

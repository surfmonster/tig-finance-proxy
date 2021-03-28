from dataclasses import dataclass
from datetime import datetime

import dateutil

import Config
from utils import comm_utils

measurement = Config.env('influxdb.quote.measurement')


class Point:

    def __init__(self, measurement: str, source: str, tags={}, time=datetime.now(), fields={}):
        self.measurement = measurement
        self.tags = tags
        self.tags['source'] = source
        self.time = time.isoformat()
        self.fields = fields


# @dataclass
class ProxyQuote:
    symbol: str
    name: str
    category: str
    time_open: datetime
    time_close: datetime
    time_high: datetime
    time_low: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    market_cap: float
    timestamp: datetime
    source: str

    def hash_id(self):
        return comm_utils.dict_hash(self.__dict__)

    def to_point(self):

        fields: dict = {}
        for key, value in self.__dict__.items():
            if key in ['symbol', 'name', 'category', 'timestamp']:
                continue
            if type(value) is int:
                value = comm_utils.to_float(value)
                print(f'convert <<<float>>> {key} {value} is int')
            fields[key] = value
        fields['id'] = self.hash_id()

        return Point(measurement=measurement,
                     tags={
                         "symbol": self.symbol,
                         "name": self.name,
                         "category": self.category
                     },
                     fields=fields,
                     time=self.timestamp,
                     source=self.source
                     )


def parse_dict(obj: dict) -> ProxyQuote:
    ans = ProxyQuote()
    data_type_map = ans.__annotations__
    for key, vtype in data_type_map.items():
        if key == 'timestamp':
            ans.timestamp = dateutil.parser.parse(obj['time'])
            del obj['time']
            continue
        try:
            if vtype is datetime:
                obj[key] = dateutil.parser.parse(obj.get(key))
        except Exception as e:
            print('error:' + key)
            print(e)
            raise e

    ans.__dict__.update(**obj)
    return ans

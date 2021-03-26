from dataclasses import dataclass
from datetime import datetime

import dateutil

import Config

measurement = Config.env('tsdb.quote.measurement')


class Point:

    def __init__(self, measurement: str, source: str, tags={}, time=datetime.now(), fields={}):
        self.measurement = measurement
        self.tags = tags
        self.tags['source'] = source
        self.time = time.isoformat()
        self.fields = fields


@dataclass
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

    def to_point(self):

        fields: dict = {}
        for key, value in self.__dict__.items():
            if key in ['symbol', 'name', 'category', 'timestamp']:
                continue
            fields[key] = value

        return Point(measurement=measurement,
                     tags={
                         "symbol": self.info.symbol,
                         "name": self.info.name,
                         "category": self.category
                     },
                     fields=fields,
                     time=self.timestamp,
                     source=self.source
                     )


def parse_dict(obj: dict) -> ProxyQuote:
    ans = ProxyQuote()
    ans.__dict__.update(**obj)
    data_type_map = ans.__annotations__
    for key, vtype in data_type_map:
        if vtype is datetime:
            ans[key] = dateutil.parser.parse( obj.get(key))

    return ans

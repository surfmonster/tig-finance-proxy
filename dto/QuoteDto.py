from datetime import datetime
import json


class Point:

    def __init__(self, measurement: str, source: str, tags={}, time=datetime.now(), fields={}):
        self.measurement = measurement
        self.tags = tags
        self.tags['source'] = source
        self.time = time.isoformat()
        self.fields = fields


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

from datetime import datetime
import json


class Point:

    def __init__(self, measurement: str, source: str, tags={}, time=datetime.now(), fields={}):
        self.measurement = measurement
        self.tags = tags
        self.tags['source'] = source
        self.time = time.isoformat()
        self.fields = fields

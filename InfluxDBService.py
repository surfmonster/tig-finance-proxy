from datetime import datetime
import json

from influxdb import InfluxDBClient
import Config

client = InfluxDBClient(Config.env('influxdb.url'), Config.envInt('influxdb.port'), Config.env('influxdb.username'),
                        Config.env('influxdb.password'), Config.env('influxdb.db'))


class Point():

    def __init__(self, measurement: str, tags={}, time=datetime.now(), fields={}):
        self.measurement = measurement
        self.tags = tags
        self.time = time.isoformat()
        self.fields = fields


def insertData(ps: []):
    arr = [p.__dict__ for p in ps]
    # js = json.dumps(arr)
    print(arr)
    client.write_points(arr)


if __name__ == '__main__':
    results = client.query('SELECT * FROM quote')

    print(results.raw)
    # p = Point(measurement='test', fields={
    #     'testV': 123
    # })
    # insertData([p])
    # # js = json.dumps(ps)
    # # print(js)
    # print(p)

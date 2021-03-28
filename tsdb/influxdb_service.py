from typing import Sequence

import influxdb

import tsdb

import Config
from dto import quote_dto
from dto.quote_dto import ProxyQuote

client = influxdb.InfluxDBClient(Config.env('influxdb.url'), Config.envInt('influxdb.port'),
                                 Config.env('influxdb.username'),
                                 Config.env('influxdb.password'), Config.env('influxdb.db'))

INSER_BATCH_SIZE = 1


def insertData(ps: Sequence[ProxyQuote]):
    # arr = [p.__dict__ for p in ps]
    # # js = json.dumps(arr)
    # print(arr)
    # client.write_points(points=arr,batch_size=100)
    iList = []
    for i in range(len(ps)):
        iList.append(ps[i].to_point().__dict__)
        if len(iList) >= INSER_BATCH_SIZE:
            print(iList)
            client.write_points(points=iList, batch_size=100)
            iList = []


def queryToPoints(q: str, measurement: str)->Sequence[ProxyQuote]:
    rss = client.query(q)
    ans = list(quote_dto.parse_dict(p) for p in rss.get_points(measurement=measurement))
    return ans


def deleteByTags(measurement: str, tags={}):
    client.delete_series(measurement=measurement, tags=tags)


if __name__ == '__main__':
    client.drop_measurement('quote')
    client.query('DROP SERIES FROM "quote"')
    results = client.query('select * from "quote"')
    print(results.raw)

    results = client.query('show series')
    print(results.raw)

    # client.delete_series(measurement='quote', tags={
    # })
    # p = Point(measurement='test', fields={
    #     'testV': 123
    # })
    # insertData([p])
    # # js = json.dumps(ps)
    # # print(js)
    # print(p)

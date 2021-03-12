from influxdb import InfluxDBClient
import Config

client = InfluxDBClient(Config.env('influxdb.url'), Config.envInt('influxdb.port'), Config.env('influxdb.username'),
                        Config.env('influxdb.password'), Config.env('influxdb.db'))


def insertData(ps: []):
    arr = [p.__dict__ for p in ps]
    # js = json.dumps(arr)
    print(arr)
    client.write_points(arr)


def queryToPoints(q: str, measurement: str):
    rss = client.query(q)
    ans = list(rss.get_points(measurement=measurement))
    return ans


if __name__ == '__main__':
    results = client.query('SELECT * FROM "quote"  WHERE "name" = \'bitcoin\'  ')

    print(results.raw)
    # p = Point(measurement='test', fields={
    #     'testV': 123
    # })
    # insertData([p])
    # # js = json.dumps(ps)
    # # print(js)
    # print(p)

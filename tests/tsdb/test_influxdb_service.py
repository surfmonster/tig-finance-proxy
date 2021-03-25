import Config
from tsdb import influxdb_service

measurement = Config.env('influxdb.quote.measurement')


def test_fetch_today():
    category = 'cryptocurrency'
    sname = 'bitcoin'
    qsql = f'SELECT * FROM "quote" WHERE "category"=\'{category}\' AND "name" = \'{sname}\' ORDER BY time ASC '
    ans= influxdb_service.queryToPoints(qsql, measurement)
    print(ans)


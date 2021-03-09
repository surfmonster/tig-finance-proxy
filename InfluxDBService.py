from influxdb import InfluxDBClient
import Config

client = InfluxDBClient(Config.env('influxdb.url'), Config.envInt('influxdb.port'), Config.env('influxdb.username'),
                        Config.env('influxdb.password'), Config.env('influxdb.db'))




if __name__ == '__main__':
    print
    client.get_list_database()
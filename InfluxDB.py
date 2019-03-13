from influxdb import InfluxDBClient

class InfluxDB:
    def __init__(self, args):
        self.influx_client = InfluxDBClient(args.influx_host, 
                                            args.influx_port, 
                                            args.influx_user, 
                                            args.influx_pass, 
                                            args.influx_database)
    
    
    def write_rank(self, page: str, iteration: int, rank: float):
        json_body = [
        {
            "measurement": "rankings",
            "tags": {
                "page": page,
                "iteration": iteration,
            },
            "fields": {
                "rank": rank
            }
        }
        ]
        self.influx_client.write_points(json_body)

    def create_database(self):
        self.influx_client.create_database("pagerank")
    def drop_database(self):
        self.influx_client.drop_database("pagerank")

    def get_rank(self, page: str, iteration: int) -> dict:
        query = 'SELECT rank ' \
                'FROM pagerank."autogen"."rankings" ' \
                'WHERE page =~ /%s/ AND iteration =~ /%d/;' % (page, iteration)
        result = list(self.influx_client.query(query))
        if result:
            return result[0][0]['rank']
        else:
            return None

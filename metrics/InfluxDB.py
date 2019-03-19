from influxdb import InfluxDBClient

class InfluxDB:
    def __init__(self, args):
        self.influx_client = InfluxDBClient(args.influx_host, 
                                            args.influx_port, 
                                            args.influx_user, 
                                            args.influx_pass, 
                                            args.influx_database)
    
    
    def write_rank(self, page, iteration, rank):
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

    def å(self, page, iteration):
        query = 'SELECT rank ' \
                'FROM pagerank."autogen"."rankings" ' \
                'WHERE page =~ /%s/ AND iteration =~ /%d/;' % (page, iteration)
        result = list(self.influx_client.query(query))
        while not result:
            result = list(self.influx_client.query(query))    
        return result[0][0]['rank']

    def get_power_node(self, node_name, begin, end):
        query = 'SELECT max(value) ' \
                'FROM k8s."default"."power/node_utilization" ' \
                'WHERE "nodename" = \'%s\' and ' \
                'time >= %s and time <= %s ' \
                'GROUP BY time(1s) FILL(linear)' % (node_name, begin, end)
        return list(self.influx_client.query(query))

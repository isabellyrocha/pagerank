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

    def get_rank(self, page, iteration):
        query = 'SELECT rank ' \
                'FROM pagerank."autogen"."rankings" ' \
                'WHERE page =~ /%s/ AND iteration =~ /%d/;' % (page, iteration)
        result = list(self.influx_client.query(query))
        while not result:
            result = list(self.influx_client.query(query))    
        return result[0][0]['rank']

    def get_power_node(self, node_name, begin, end):
        query = 'SELECT value ' \
                'FROM k8s."default"."power/node_utilization" ' \
                'WHERE "nodename" = \'%s\' and ' \
                'time >= %d and time <= %d ' % (node_name, begin, end)
        print(query)
        return list(self.influx_client.query(query))

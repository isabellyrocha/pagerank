from influxdb import InfluxDBClient

class InfluxDB:
    def __init__(self, args):
        self.influx_client = InfluxDBClient(args.influx_host, 
                                            args.influx_port, 
                                            args.influx_user, 
                                            args.influx_pass, 
                                            args.influx_database)
    
    
    def write_rank(self, iteration, page, rank):
        json_body = [
        {
            "measurement": "rankings",
            "tags": {
                "iteration": iteration,
                "page": page
            },
            "fields": {
                "rank": rank
            }
        }
        ]
        self.influx_client.write_points(json_body)

    def write_cpu(self, timestamp, node, cpu):
        json_body = [
        {
            "measurement": "custom_cpu/node_utilization",
            "tags": {
                "nodename": node,
            },
            "time": timestamp,
            "fields": {
                "value": cpu
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


    def get_power(self, node_name, begin, end):
        query = 'SELECT value ' \
                'FROM k8s."default"."power/node_utilization" ' \
                'WHERE "nodename" = \'%s\' and ' \
                'time >= %d and time <= %d ' % (node_name, begin, end)
       # print(query)
        result = list(self.influx_client.query(query))[0]
        power_values = []
        for index in range(len(result)):
            power_values.append(result[index]['value'])

        return power_values

    def get_grouped_power(self, node_name, begin, end):
        query = 'SELECT mean(value) ' \
                'FROM k8s."default"."power/node_utilization" ' \
                'WHERE "nodename" = \'%s\' and ' \
                'time >= %d and time <= %d ' \
                'group by time(60s) fill(previous)' % (node_name, begin, end)
        #print(query)
        result = list(self.influx_client.query(query))[0]
        power_values = []
        for index in range(len(result)):
            mean = result[index]['mean']
            if mean == None:
                mean = 0
            power_values.append(result[index]['mean'])

        return power_values

    def get_cpu(self, node_name, begin, end):
        query = 'SELECT value ' \
                'FROM k8s."default"."custom_cpu/node_utilization" ' \
                'WHERE "nodename" = \'%s\' and ' \
                'time >= %d and time <= %d ' % (node_name, begin, end)
        #print(query)
        result = list(self.influx_client.query(query))[0]
        #print(result)
        power_values = []
        for index in range(len(result)):
            power_values.append(result[index]['value'])

        return power_values

    def get_grouped_cpu(self, node_name, begin, end):
        query = 'SELECT mean(value) ' \
                'FROM k8s."default"."custom_cpu/node_utilization" ' \
                'WHERE "nodename" = \'%s\' and ' \
                'time >= %d and time <= %d ' \
                'group by time(60s) fill(previous)' % (node_name, begin, end)
        #print(query)
        result = list(self.influx_client.query(query))[0]
        #print(result)
        power_values = []
        for index in range(len(result)):
            mean = result[index]['mean']
            if mean == None:
                mean = 0
            power_values.append(mean)
        return power_values

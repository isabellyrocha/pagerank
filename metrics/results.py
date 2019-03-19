from influxdb import InfluxDBClient
from datetime import datetime
from datetime import timedelta
import numpy as np
from argparse import ArgumentParser
from k8s import Kubernetes 

def query_last(query, influx_client):
    req = list(influx_client.query(query))
    result = {}
    if len(req) == 0:
        return result
    sec = -1
    for r in req[0]:
        sec = sec +1
        value = r['max']
        #time = datetime.strptime(r['time'], '%Y-%m-%dT%H:%M:%SZ').second
        result[sec] = value
    
    i = 0

    while (result[i] == None):
        i = i + 1
    k = sec
    while (result[k] == None):
        k = k - 1
    for j in range(i):
        result[j] = result[i+1]
    for j in range(k,sec):
        result[j] = result[k-1]

    return result

def energy(power_map):
    values = power_map.values()
    v = []
    for value in values:
        #print(value)
        new_value = value 
        v.append(new_value)
    return np.trapz(v, power_map.keys())
    #return np.trapz(power_map.values(), power_map.keys())
                                                               
def main():
    parser = ArgumentParser(description='rank page')
    parser.add_argument('--influx-host', metavar='influx-host', type=str,
                        help='string corresponding to the host address of the influx database')
    parser.add_argument('--influx-port', metavar='influx-port', type=int,
                        help='int corresponding to the port of the influx database')
   
    args = parser.parse_args()
    kube = Kubernetes()
    metrics_storage = InfluxDB(args)
    
    finished_pods = kube.list_finished_pods()
    for pod in finished_pods:
        started = int(kube.get_stated_at(pod))*1000000000
        finished = int(kube.get_finished_at(pod))*1000000000
        host = kube.get_host_node(pod)
        print(metrics_storage.get_power_node(str(node), started, finished))


if __name__ == '__main__':
    main()


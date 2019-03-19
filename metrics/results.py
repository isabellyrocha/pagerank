from influxdb import InfluxDBClient
from datetime import datetime
from datetime import timedelta
import numpy as np
from argparse import ArgumentParser
from kubernetes import client,config
from kubernetes.client import V1PodStatus, V1ObjectReference, V1Event, V1EventSource, V1Pod, V1PodSpec, V1Node, V1Binding, V1Container, V1DeleteOptions, V1ObjectMeta, V1ResourceRequirements
from kubernetes.client.rest import ApiException

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
    parser.add_argument('--started', nargs='?', const='started', metavar='number-of-pages', type=int,
                        help='integer corresponding to the number of pages in the input')
    parser.add_argument('--finished', nargs='?', const='finished', metavar='number-of-pages', type=int,
                        help='integer corresponding to the number of pages in the input')
    influx_client = InfluxDBClient("10.96.21.32", "8086", "root", "root", "k8s")    
    
    parser.add_argument('--node-name', nargs='?', const='node-name', metavar='number-of-pages', type=str,
                        help='integer corresponding to the number of pages in the input')
    args = parser.parse_args()
    started = int(args.started)*1000000000
    finished = int(args.finished)*1000000000
    power = query_last('SELECT max(value) FROM k8s."default"."power/node_utilization" WHERE "nodename" = \'%s\' and '
                                       'time >= %s and time <= %s group by time(1s) fill(linear)' % (args.node_name,started,finished), influx_client)
    total_energy = energy(power)
    print("duration:{}\n".format(len(power)))
    print("energy:{}\n".format(total_energy))
    
    config.load_kube_config()
    api_k8s = client.CoreV1Api()
    pods = api_k8s.list_pod_for_all_namespaces(
            field_selector=("metadata.name=pagerank-1-mp5bg")).items
    print(pods[0].status.container_statuses[0].state.terminated)
    print(pods[0].status.container_statuses[0].state.terminated.started_at)
    print(pods[0].status.container_statuses[0].state.terminated.finished_at.strftime("%s"))
    time=pods[0].status.container_statuses[0].state.terminated.finished_at
    #timestamp = datetime.timestamp(time)
    print("timestamp =", timedelta(days=365))
    #print("Found %d scheduled pods" % len(pods))

if __name__ == '__main__':
    main()


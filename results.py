from influxdb import InfluxDBClient
from datetime import datetime
from datetime import timedelta
import numpy as np
from argparse import ArgumentParser
from metrics.k8s import Kubernetes 

def create_pod(pod_name, host_node):
    return V1Pod(
            api_version="v1",
            kind="Pod",
            metadata=V1ObjectMeta(
                name=pode_name,
            ),
            spec=V1PodSpec(
                containers=[V1Container(
                    name=pod_name,
                    image_pull_policy="IfNotPresent",
                    image="isabellyrocha/pagerank:raspberry-pi",
                    command=["python3",
                            "/pagerank/pagerank.py",
                            " --pages-file-name=/pagerank/input/web-Stanford-Subet.txt"
                            "--iterations=3",
                            "--number-of-nodes=1",
                            "--node-id=0",
                            "--influx-host=10.96.21.32",
                            "--influx-port=8086",
                            "--influx-database=pagerank"],
                ),
                node_selector= {'kubernetes.io/hostname': hostname}],
                restart_policy="OnFailure"
            )
        ) 

def energy(power_values):
    return np.trapz(power_values)
                                                               
def main():
    parser = ArgumentParser(description='rank page')
    parser.add_argument('--influx-user', nargs='?', const='root', metavar='influx-user', type=str,
                        help='string corresponding to the user name of the influx database')
    parser.add_argument('--influx-pass', nargs='?', const='root', metavar='influx-pass', type=str,
                        help='string corresponding to the password of the influx database')
    parser.add_argument('--influx-host', metavar='influx-host', type=str,
                        help='string corresponding to the host address of the influx database')
    parser.add_argument('--influx-port', metavar='influx-port', type=int,
                        help='int corresponding to the port of the influx database')
    parser.add_argument('--influx-database', nargs='?', const='k8s', metavar='influx-database', type=str,
                        help='string corresponding to the name of the influx database')   
    args = parser.parse_args()
    kube = Kubernetes()
    metrics_storage = InfluxDB(args)
    
    pod = create_pod('pagerank-api','vully-1')
    self.api_k8s.create_namespaced_pod("default", pod)
    
    finished_pods = kube.list_finished_pods()
    for pod in finished_pods:
        started = int(kube.get_started_at(pod))*1000000000
        finished = int(kube.get_finished_at(pod))*1000000000
        host = kube.get_host_node(pod)
        pod_name = kube.get_name(pod)
        power_values = metrics_storage.get_power_node(host, started, finished)
        pod_energy = energy(power_values)
        pod_duration = (finished - started)/1000000000
        print(pod_name + "," + str(pod_energy) + "," + str(pod_duration))
pagerank.py
if __name__ == '__main__':
    main()


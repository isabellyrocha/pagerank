from metrics.influxdb import InfluxDB
from datetime import datetime
from datetime import timedelta
import time
import numpy as np
from argparse import ArgumentParser
from metrics.kubernetes import Kubernetes  
from argparse import ArgumentParser
    

def main():
    parser = ArgumentParser(description='deploy rank page')
    parser.add_argument('--influx-user', nargs='?', const='root', metavar='influx-user', type=str,
                        help='string corresponding to the user name of the influx database')
    parser.add_argument('--influx-pass', nargs='?', const='root', metavar='influx-pass', type=str,
                        help='string corresponding to the password of the influx database')
    parser.add_argument('--influx-host', metavar='10.96.21.32', type=str,
                        help='string corresponding to the host address of the influx database')
    parser.add_argument('--influx-port', metavar=8086, type=int,
                        help='int corresponding to the port of the influx database')
    parser.add_argument('--influx-database', nargs='?', const='k8s', metavar='influx-database', type=str,
                        help='string corresponding to the name of the influx database')
    parser.add_argument('-D', nargs='?', const='DEBUG', metavar='DEBUG', type=str,
                        help='Flag to decide if we want the debug mode or not')
    args = parser.parse_args()
    metrics_storage = InfluxDB(args)
    k8s = Kubernetes() 
    number_of_pods = 10
    '''
    for pod_id in range(number_of_pods):
        pod_name = 'pagerank-seq-%d' % (pod_id)
        k8s.deploy_pod(k8s.create_pagerank_pod(pod_name, 'vully-1'))
        time.sleep(30)
        pod = k8s.get_pod(pod_name)
        while (not k8s.is_finished(pod)):
            time.sleep(30)
            pod = k8s.get_pod(pod_name)
        metrics_storage.drop_database()
    '''
    for pod_id in range(number_of_pods):
        #metrics_storage.drop_database()        
        pod_name_1 = 'pagerank-dist3-%d-0' % (pod_id)
        pod_name_2 = 'pagerank-dist3-%d-1' % (pod_id)
        pod_name_3 = 'pagerank-dist3-%d-2' % (pod_id)
        k8s.deploy_pod(k8s.create_pagerank_pod(pod_name_1, 'vully-1', 3, 0))
        k8s.deploy_pod(k8s.create_pagerank_pod(pod_name_2, 'vully-2', 3, 1))
        k8s.deploy_pod(k8s.create_pagerank_pod(pod_name_3, 'vully-3', 3, 2))
        time.sleep(30)
        pod_1 = k8s.get_pod(pod_name_1)
        pod_2 = k8s.get_pod(pod_name_2)
        pod_3 = k8s.get_pod(pod_name_3)
        while (not (k8s.is_finished(pod_1) and k8s.is_finished(pod_2) and k8s.is_finished(pod_3))):
            time.sleep(30)
            pod_1 = k8s.get_pod(pod_name_1)
            pod_2 = k8s.get_pod(pod_name_2)
            pod_3 = k8s.get_pod(pod_name_3)
        metrics_storage.drop_database()

if __name__ == '__main__':
    main()


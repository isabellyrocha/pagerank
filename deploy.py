from metrics.influxdb import InfluxDB
from datetime import datetime
from datetime import timedelta
import time
import numpy as np
from argparse import ArgumentParser
from metrics.kubernetes import Kubernetes  

    

def main():
    k8s = Kubernetes() 
    number_of_pods = 10
    for pod_id in range(number_of_pods):
        pod_name = 'pagerank-seq-%d' % (pod_id)
        k8s.deploy_pod(k8s.create_pagerank_pod(pod_name, 'vully-1'))
        time.sleep(30)
        pod = k8s.get_pod(pod_name)
        while (not k8s.is_finished(pod)):
            time.sleep(30)
            pod = k8s.get_pod(pod_name)
            
    for pod_id in range(number_of_pods):
        pod_name_1 = 'pagerank-dist-1-%d' % (pod_id)
        pod_name_2 = 'pagerank-dist-2-%d' % (pod_id)
        k8s.deploy_pod(k8s.create_pagerank_pod(pod_name_1, 'vully-1'))
        k8s.deploy_pod(k8s.create_pagerank_pod(pod_name_2, 'vully-2'))
        time.sleep(30)
        pod_1 = k8s.get_pod(pod_name_1)
        pod_2 = k8s.get_pod(pod_name_2)
        while (not (k8s.is_finished(pod_1) and k8s.is_finished(pod_2))):
            time.sleep(30)
            pod_1 = k8s.get_pod(pod_name_1)
            pod_2 = k8s.get_pod(pod_name_1)

if __name__ == '__main__':
    main()


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
    for pod_id in range(number_of_pods+1,number_of_pods+2):
        pod_name = 'pagerank-seq-%d' % (pod_id)
        k8s.deploy_pod(k8s.create_pagerank_pod(pod_name, 'vully-1'))
        time.sleep(30)
        pod = k8s.get_pod(pod_name)
        while (not k8s.is_finished(pod)):
            time.sleep(30)
            pod = k8s.get_pod(pod_name)

if __name__ == '__main__':
    main()


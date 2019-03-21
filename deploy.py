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
        pod = k8s.create_pagerank_pod('pagerank-seq-%d' % (pod_id), 'vully-1')
        k8s.deploy_pod(pod)
        time.sleep(30)
        while (not k8s.is_finished(pod)):
            time.sleep(30)

if __name__ == '__main__':
    main()


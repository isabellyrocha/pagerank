from metrics.influxdb import InfluxDB
from datetime import datetime
from datetime import timedelta
import time
import numpy as np
from argparse import ArgumentParser
from metrics.kubernetes import Kubernetes  

    

def main():
    k8s = Kubernetes() 
    
    for pod_id in range(number_of_pod):
        pod = k8s.create_pagerank_pod('pagerank-seq-'+pod_id, 'vully-1')
        k8s.deploy_pod(pod)
        while (not k8s.is_finished()):
            time.sleep(30)

if __name__ == '__main__':
    main()


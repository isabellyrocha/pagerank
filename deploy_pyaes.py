from metrics.kubernetes import Kubernetes
import time

def main():
    k8s = Kubernetes()
    for i in range(5, 10):
        pod_name = 'pyaes-seq-%d' % (i)
        pod = k8s.create_pyaes_pod(pod_name, 'vully-1', 1)
        k8s.deploy_pod(pod)
        time.sleep(60)
        pod = k8s.get_pod(pod_name)
        while (not k8s.is_finished(pod)):
            time.sleep(60)
            pod = k8s.get_pod(pod_name)
    for i in range(5,10):
        pod_name_1 = 'pyaes-dist2n-%d-0' % (i)
        pod_name_2 = 'pyaes-dist2n-%d-1' % (i)
        k8s.deploy_pod(k8s.create_pyaes_pod(pod_name_1, 'vully-1', 2))
        k8s.deploy_pod(k8s.create_pyaes_pod(pod_name_2, 'vully-2', 2))
        pod_1 = k8s.get_pod(pod_name_1)
        pod_2 = k8s.get_pod(pod_name_2)
        while (not (k8s.is_finished(pod_1) and k8s.is_finished(pod_2))):
            time.sleep(60)
            pod_1 = k8s.get_pod(pod_name_1)
            pod_2 = k8s.get_pod(pod_name_2)
    for i in range(5,10):
        pod_name_1 = 'pyaes-dist3n-%d-0' % (i)
        pod_name_2 = 'pyaes-dist3n-%d-1' % (i)
        pod_name_3 = 'pyaes-dist3n-%d-2' % (i)
        k8s.deploy_pod(k8s.create_pyaes_pod(pod_name_1, 'vully-1', 3))
        k8s.deploy_pod(k8s.create_pyaes_pod(pod_name_2, 'vully-2', 3))
        k8s.deploy_pod(k8s.create_pyaes_pod(pod_name_3, 'vully-3', 3))
        pod_1 = k8s.get_pod(pod_name_1)
        pod_2 = k8s.get_pod(pod_name_2)
        pod_3 = k8s.get_pod(pod_name_3)
        while (not (k8s.is_finished(pod_1) and k8s.is_finished(pod_2) and k8s.is_finished(pod_3))):
            time.sleep(60)
            pod_1 = k8s.get_pod(pod_name_1)
            pod_2 = k8s.get_pod(pod_name_2)
            pod_3 = k8s.get_pod(pod_name_3)
if __name__ == '__main__':
    main()

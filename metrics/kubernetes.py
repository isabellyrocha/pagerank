from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.client import V1Pod, V1ObjectMeta, V1PodSpec, V1Container

class Kubernetes:
    def __init__(self):
        config.load_kube_config()
        self.api_k8s = client.CoreV1Api()

    def create_pyaes_pod(self, pod_name, host_name, number_of_nodes=1):
        iterations = int(243/number_of_nodes)
        return V1Pod(
            api_version = 'v1',
            kind = 'Pod',
            metadata = V1ObjectMeta(
                name = pod_name
            ),
            spec = V1PodSpec(
                containers = [
                    V1Container(
                        name = pod_name,
                        image_pull_policy = "IfNotPresent",
                        image = "isabellyrocha/pyaes:raspberry-pi",
                        command = [
                            'python',
                            '/pyaes/crypto_pyaes.py',
                            '--iterations=%d' % (iterations)
                        ]
                    )
                ],
                node_selector = {
                    'kubernetes.io/hostname': host_name
                },
                restart_policy = 'OnFailure'
            )
        )
    
    def create_pagerank_pod(self, pod_name, host_name, number_of_nodes=1, node_id=0):
        return V1Pod(
            api_version = 'v1',
            kind = 'Pod',
            metadata = V1ObjectMeta(
                name = pod_name
            ),
            spec = V1PodSpec(
                containers = [
                    V1Container(
                        name = pod_name,
                        image_pull_policy = "IfNotPresent",
                        image = "isabellyrocha/pagerank:raspberry-pi",
                        command = [
                            'python3',
                            '/pagerank/pagerank.py',
                            '--pages-file-name=/pagerank/input/web-Google.txt',
                            '--iterations=10',
                            '--number-of-nodes=%d' % (number_of_nodes),
                            '--node-id=%d' % (node_id),
                            '--influx-host=10.96.21.32',
                            '--influx-port=8086',
                            '--influx-database=pagerank'
                        ]
                    )
                ],
                node_selector = {
                    'kubernetes.io/hostname': host_name
                },
                restart_policy = 'OnFailure'
            )
        )
    
    def deploy_pod(self, pod):
        self.api_k8s.create_namespaced_pod("default", pod)
        
    def get_started_time(self, pod_name):
        pod = self.get_pod(pod_name)
        return get_started_at(pod)

    def get_finished_time(self, pod_name):
        pod = self.get_pod(pod_name)
        return get_finished_at(pod)

    def list_finished_pods(self):
        pods = self.api_k8s.list_pod_for_all_namespaces(
            field_selector=("status.phase=Succeeded")).items
        return pods
    
    def get_pod(self, pod_name):
        return self.api_k8s.list_pod_for_all_namespaces(
            field_selector=("metadata.name=%s" % (pod_name))).items[0]
        
    def get_name(self, pod):
        return pod.metadata.name #.labels['job-name']

    def get_started_at(self, pod):
        started_at = pod.status.container_statuses[0].state.terminated.started_at
        return started_at.strftime("%s")

    def get_finished_at(self, pod):
        finished_at = pod.status.container_statuses[0].state.terminated.finished_at
        return finished_at.strftime("%s")

    def get_host_node(self, pod):
        return pod.spec.node_name
        
    def is_finished(self, pod):
        print(pod)
        print(pod.status)
        return pod.status.phase == 'Succeeded'

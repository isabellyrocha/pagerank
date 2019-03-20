from kubernetes import client,config
from kubernetes.client import V1PodStatus, V1ObjectReference, V1Event, V1EventSource, V1Pod, V1PodSpec, V1Node, V1Binding, V1Container, V1DeleteOptions, V1ObjectMeta, V1ResourceRequirements
from kubernetes.client.rest import ApiException

class Kubernetes:
    def __init__(self):
        config.load_kube_config()
        self.api_k8s = client.CoreV1Api()

    def create_pod(pod_name, hostname):
        return V1Pod(
            api_version="v1",
            kind="Pod",
            metadata=V1ObjectMeta(
                name=pod_name,
            ),
            spec=V1PodSpec(
                containers=[V1Container(
                    name=pod_name,
                    image_pull_policy="IfNotPresent",
                    image="isabellyrocha/pagerank:raspberry-pi",
                    command=["python3",
                            "/pagerank/pagerank.py",
                            "--pages-file-name=/pagerank/input/web-Stanford-Subet.txt",
                            "--iterations=3",
                            "--number-of-nodes=1",
                            "--node-id=0",
                            "--influx-host=10.96.21.32",
                            "--influx-port=8086",
                            "--influx-database=pagerank"],
                )],
                node_selector={'kubernetes.io/hostname':hostname},
                restart_policy="OnFailure"
            )
        )

    def get_start_time(self, pod_name):
        pod = self.api_k8s.list_pod_for_all_namespaces(field_selector=("metadata.name=%s" % (pod_name))).items[0]
        return pod.status.container_statuses[0].state.terminated.started_at.strftime("%s")

    def get_finished_time(self, pod_name):
        pod = self.api_k8s.list_pod_for_all_namespaces(
            field_selector=("metadata.name=%s", pod_name)).items[0]
        return pod.status.container_statuses[0].state.terminated.finished_at.strftime("%s")

    def list_finished_pods(self):
        pods = self.api_k8s.list_pod_for_all_namespaces(
            field_selector=("status.phase=Succeeded")).items
        #print(pods)
        #print("Found %d active pods scheduled in node %s" % (len(pods), node))
        return pods
    
    def get_name(self,pod):
        return pod.metadata.labels['job-name']

    def get_started_at(self, pod):
        return pod.status.container_statuses[0].state.terminated.started_at.strftime("%s")

    def get_finished_at(self, pod):
        return pod.status.container_statuses[0].state.terminated.finished_at.strftime("%s")

    def get_host_node(self, pod):
        return pod.spec.node_name

from kubernetes import client,config
from kubernetes.client import V1PodStatus, V1ObjectReference, V1Event, V1EventSource, V1Pod, V1PodSpec, V1Node, V1Binding, V1Container, V1DeleteOptions, V1ObjectMeta, V1ResourceRequirements
from kubernetes.client.rest import ApiException

class Kubernetes:
    def __init__(self, args):
        config.load_kube_config()
        self.api_k8s = client.CoreV1Api()


    def get_start_time(self, pod_name):
        pod = api_k8s.list_pod_for_all_namespaces(
            field_selector=("metadata.name=%s", pod_name)).items[0]
        return pod.status.container_statuses[0].state.terminated.started_at.strftime("%s")

    def get_finished_time(self, pod_name):
        pod = api_k8s.list_pod_for_all_namespaces(
            field_selector=("metadata.name=%s", pod_name)).items[0]
        return pod.status.container_statuses[0].state.terminated.finished_at.strftime("%s")


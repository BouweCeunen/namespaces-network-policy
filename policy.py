import os
from kubernetes import client, config, utils, watch

config.load_incluster_config()
kubernetesv1 = client.CoreV1Api()
kubernetesbetav1 = client.ExtensionsV1beta1Api()

filename_last_resource = '/etc/last_resource_version'
filename_excluded_namespaces = '/etc/excluded_namespaces'

def update_last_resource_version(resource_version):
    if resource_version != None:
        f = open(filename_last_resource, "w")
        f.write(resource_version)
        f.close()

def get_excluded_namespaces():
    if not os.path.isfile(filename_excluded_namespaces):
        return ['kube-system']
    return open(filename_excluded_namespaces, "r").read().split()

def get_last_resource_version():
    if not os.path.isfile(filename_last_resource):
        update_last_resource_version('0')
    return open(filename_last_resource, "r").read()

def patch_labels(event_name):
    labels = {
        "metadata": {
            "labels": {
                "name": event_name
            }
        }
    }

    try:
        kubernetesv1.patch_namespace(event_name, labels)
    except Exception:
        print('Failed patching labels in namespace %s' % event_name)

def whitelist(policy_name, event_name):
    policy = {
        'metadata': {
            'name': policy_name
        },
        'spec': {
            'pod_selector': {
                'match_labels': {}
            },
            'ingress': [
                client.V1beta1NetworkPolicyIngressRule(
                    _from=[
                        client.V1beta1NetworkPolicyPeer(
                            namespace_selector=client.V1LabelSelector(
                                match_labels={
                                    'name': 'kube-system'
                                }
                            )
                        ),
                        client.V1beta1NetworkPolicyPeer(
                            pod_selector=client.V1LabelSelector(
                                match_labels={}
                            )
                        )
                    ]
                )
            ]
        }
    }

    try:
        kubernetesbetav1.read_namespaced_network_policy(policy_name, event_name)
    except Exception:
        try:
            kubernetesbetav1.create_namespaced_network_policy(event_name, policy)
        except Exception:
            print('Failed creating network policy in namespace %s' % event_name)

excluded_namespaces = get_excluded_namespaces()
print('Excluded namespaces: %s' % excluded_namespaces)

w = watch.Watch()
for event in w.stream(kubernetesv1.list_namespace, _request_timeout=0, resource_version=get_last_resource_version()):
    event_type = event['type']
    event_name = event['object'].metadata.name
    resource_version = event['object'].metadata.resource_version
    print("==> Event %s: %s: %s" % (event_type,event_name,resource_version))

    if event_type != None:
        if event_type != 'ERROR':
            if event_type == 'ADDED':
                patch_labels(event_name)
                if event_name not in excluded_namespaces:
                    whitelist('allow-intra-namespace', event_name)
        else:
            if event['raw_object']['reason'] == 'Gone':
                message = event['raw_object']['message']
                resource_version = message[message.find("(")+1:message.find(")")]

    update_last_resource_version(resource_version)
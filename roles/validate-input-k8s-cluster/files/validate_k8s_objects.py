#!/usr/bin/env python3

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import os
import sys
import base64
import requests

from oauth2client.client import GoogleCredentials
from kubernetes import client, config
from kubernetes.client.rest import ApiException

KUBECONFIG_FILE = os.getenv('KUBECONFIG')
try:
    config.load_kube_config(config_file=KUBECONFIG_FILE)
except Exception as e:
    print(f"Unable to load kubeconfig : {KUBECONFIG_FILE}")
    print(f"Error: {e}")
    sys.exit(1)

api_instance = client.CoreV1Api()
apps_api = client.AppsV1Api()


DEFAULT_CASSANDRA_STATEFULSET = "apigee-cassandra-default"
DEFAULT_APIGEE_NAMESPACE = "apigee"

def check_api_server():
    timeout = 2
    try:
        api_instance.list_namespace(_request_timeout=timeout)
        return True
    except Exception as e:
        print("Kubernetes API server is not reachable")
        print(f"Error: {str(e)}")
        return False


def check_nodes(label_selector):
    node_list = api_instance.list_node(label_selector=label_selector)
    if len(node_list.items) > 0:
        return True
    else:
        return False

def can_deploy_statefulset(storage_class_name):
    namespace = DEFAULT_APIGEE_NAMESPACE
    try:
        api_instance.read_namespace(name=namespace)
        statefulset = apps_api.read_namespaced_stateful_set(name=DEFAULT_CASSANDRA_STATEFULSET, namespace=namespace)
    except ApiException as e:
        print(f"not found: {e}")
        if e.status == 404:
            return True

    storage_classes = set()
    claims = statefulset.spec.volume_claim_templates
    if len(claims) > 1:
        raise Exception("statefulset contains more than one volume claim")
    volume_claim_template = claims[0]
    if not volume_claim_template.metadata.annotations:
        return False
    if "volume.beta.kubernetes.io/storage-class" not in volume_claim_template.metadata.annotations:
        return False
    storage_class = volume_claim_template.metadata.annotations["volume.beta.kubernetes.io/storage-class"]
    if storage_class_name != storage_class:
        return False
    return True


def list_namespace_secrets(namespace):
    secret_list = api_instance.list_namespaced_secret(namespace)
    return [each_secret.metadata.name for each_secret in secret_list.items]


def _finditem(obj, key, result=[]):
    if key in obj:
        result.append(obj[key])
    for k, v in obj.items():
        if isinstance(v, dict):
            item = _finditem(v, key, result)
            if item is not None:
                return item


def get_roles(project_id):
    credentials = GoogleCredentials.get_application_default()
    access_token = credentials.get_access_token().access_token

    headers = {}
    headers['Authorization'] = f'Bearer {access_token}'
    uri = f"https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}:getIamPolicy?alt=json"  # noqa

    response = requests.post(uri, headers=headers)
    if response.status_code == 200:
        return True, response
    else:
        return False, {"error": json.loads(response.text).get('error', {}).get('message','')}  # noqa


def get_sa_role(secret_name, namespace, bindings):
    secret = api_instance.read_namespaced_secret(secret_name, namespace)
    print(secret.data)
    try:
        if secret.data is not None:
            decoded_data = base64.b64decode(secret.data['client_secret.json'])
            client_secret_data = json.loads(decoded_data)
        else:
            return False, {"error": f"{secret_name}'s secret.data is None"}  # noqa
    except KeyError:
        return False, {"error": f"File 'client_secret.json' not found in {secret_name}'s secret.data"}  # noqa
    except json.decoder.JSONDecodeError:
        return False, {"error": f"client_secret file is not of type json in {secret_name}'s secret.data"}  # noqa

    if not client_secret_data.get('client_email', False):
        return False, {"error": f"Incorrect secret data configuration. 'client_email' not present in {secret_name}'s secret data"}  # noqa

    service_account_email = client_secret_data.get('client_email', '')
    bindings = [binding for binding in bindings if service_account_email in [member.split(':')[-1] for member in binding['members'] if member.startswith('serviceAccount:')]]  # noqa
    existing_roles = [binding['role'] for binding in bindings]
    return True, existing_roles


def main():
    parser = argparse.ArgumentParser(description='Validates Apigee Objects')
    parser.add_argument('--input_data', help='Apigee Input data', required=True)  # noqa
    parser.add_argument('--generate_certificates', help='SSL Certs need to be generated', default='True')  # noqa
    parser.add_argument('--create_service_account', help='Service Account Secrets need to be created', default='True')  # noqa
    parser.add_argument('--cassandra_storage_class', help='In case a custom storage class is used for cassandra, this argument validates if the deployment can proceed with the existing storage class', required=False, default='')
    args = parser.parse_args()
    input_data = json.loads(args.input_data)
    apigee_vhosts = input_data.get('virtualhosts', [])
    apigee_node_selector = input_data.get('nodeSelector', {}).get(
        'requiredForScheduling', False)
    apigee_namespace = 'apigee'
    validations = []
    api_server_reachable = check_api_server()
    if not api_server_reachable:
        sys.exit(1)

    if apigee_node_selector:
        apigee_rt_node_selector_key = input_data.get('nodeSelector', {}).get(  # noqa
            'apigeeRuntime', {}).get('key','cloud.google.com/gke-nodepool')  # noqa
        apigee_rt_node_selector_value = input_data.get('nodeSelector', {}).get(  # noqa
            'apigeeRuntime', {}).get('value', 'apigee-runtime')  # noqa
        apigee_data_node_selector_key = input_data.get('nodeSelector', {}).get(  # noqa
            'apigeeData', {}).get('key', 'cloud.google.com/gke-nodepool')  # noqa
        apigee_data_node_selector_value = input_data.get('nodeSelector', {}).get(  # noqa
            'apigeeData', {}).get('value', 'apigee-data')

        if not check_nodes(f"{apigee_rt_node_selector_key}={apigee_rt_node_selector_value}"):  # noqa
            validations.append(f"Number of nodes with selectors {apigee_rt_node_selector_key}={apigee_rt_node_selector_value} are Zero[0]")  # noqa
        if not check_nodes(f"{apigee_data_node_selector_key}={apigee_data_node_selector_value}"):  # noqa
            validations.append(f"Number of nodes with selectors {apigee_data_node_selector_key}={apigee_data_node_selector_value} are Zero[0]")  # noqa

    apigee_secrets = list_namespace_secrets(apigee_namespace)
    _key_ref = 'sslSecret'
    if args.generate_certificates == 'False':
        for apigee_vhost in apigee_vhosts:
            if apigee_vhost[_key_ref] not in apigee_secrets:
                validations.append(f"SSL Secret: {apigee_vhost[_key_ref]} Not found in {apigee_namespace} namespace")  # noqa

    if args.create_service_account == 'False':
        input_service_accounts = []
        _finditem(input_data, 'serviceAccountRef', input_service_accounts)

        for each_sa in input_service_accounts:
            if each_sa not in apigee_secrets:
                validations.append(f"Service Account Secret: {each_sa} Not found in {apigee_namespace} namespace")  # noqa

        apigee_components = ["mart", "runtime", "udca", "logger", "metrics", "watcher", "cassandra"]  # noqa
        project_id = input_data.get('gcp', '').get('projectID', '')
        success, roles_response = get_roles(project_id)

        if success:
            roles_map_file_path = 'roles/validate-input-k8s-cluster/files/roles_map.json'  # noqa
            roles_map = {}
            try:
                with open(roles_map_file_path, 'r') as file:
                    roles_map = json.load(file)
            except FileNotFoundError:
                validations.append(f"ERROR: Couldn't perform kubernetes validations. Reason: File '{roles_map_file_path}' not found.")  # noqa

            bindings = roles_response.json()['bindings']
            for component in apigee_components:
                if component == "cassandra":
                    if input_data.get(component, {}).get('backup', '').get('enabled'):  # noqa
                        component_sa = input_data.get(component, {}).get('backup', '').get('serviceAccountRef', '')  # noqa
                    elif input_data.get(component, {}).get('restore', '').get('enabled'):  # noqa
                        component_sa = input_data.get(component, {}).get('restore', '').get('serviceAccountRef', '')  # noqa
                    else:
                        continue
                else:
                    component_sa = input_data.get(component, {}).get('serviceAccountRef', '')  # noqa

                success_bool, existing_roles = get_sa_role(component_sa, apigee_namespace, bindings)  # noqa
                if success_bool:
                    req_roles = roles_map.get(f"apigee-{component}", '')
                    for role in req_roles:
                        if role not in existing_roles:
                            validations.append(f"ERROR: Service Account Secret {component_sa} doesn't have required role({role})")  # noqa
                else:
                    error_msg = existing_roles.get("error")
                    validations.append(f"ERROR: {error_msg}")

        else:
            print("hii")
            error_msg = roles_response.get("error")
            validations.append(f"ERROR: Couldn't retrieve the roles associated with service accounts. Reason : {error_msg}")  # noqa

    try:
        storage_class_name = args.cassandra_storage_class
        if storage_class_name != "":
            if not can_deploy_statefulset(storage_class_name):
                validations.append(f"ERROR: You cannot change the storage class of an existing statefulset, current storage class: {storage_class_name}") 
    except Exception as e:
        validations.append(f"ERROR: There was an error validating statefulsets. Reason: {e}") 

    if len(validations) > 0:
        print('Kubernetes validation Errors found !')
        print("\n".join(validations))
        sys.exit(1)
    print('Kubernetes validations successfull')


if __name__ == '__main__':
    main()

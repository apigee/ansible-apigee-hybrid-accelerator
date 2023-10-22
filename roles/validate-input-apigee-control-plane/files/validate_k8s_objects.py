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

import os
import sys
import json
import argparse
from kubernetes import client, config

config.load_kube_config(config_file=os.getenv('KUBECONFIG'))
api_instance = client.CoreV1Api()

def check_nodes(label_selector):
    node_list = api_instance.list_node(label_selector=label_selector)
    if len(node_list.items) > 0:
        return True
    else:
        return False

def list_namespace_secrets(namespace):
    secret_list = api_instance.list_namespaced_secret(namespace)
    return [ each_secret.metadata.name for each_secret in secret_list.items ]

def _finditem(obj, key, result=[]):
    if key in obj: result.append(obj[key])
    for k, v in obj.items():
        if isinstance(v,dict):
            item = _finditem(v, key, result)
            if item is not None:
                return item

def main():
    parser = argparse.ArgumentParser(description='Validates Apigee Objects')
    parser.add_argument('--input_data', help='Apigee Input data')
    args = parser.parse_args()
    input_data = json.loads(args.input_data)
    apigee_vhosts = input_data.get('virtualhosts',[])
    apigee_node_selector = input_data.get('nodeSelector',{}).get(
        'requiredForScheduling',False)
    secret_namespace = 'apigee'
    validations = []

    if apigee_node_selector:
        apigee_rt_node_selector_key = input_data.get('nodeSelector',{}).get(
            'apigeeRuntime',{}).get('key','cloud.google.com/gke-nodepool')
        apigee_rt_node_selector_value = input_data.get('nodeSelector',{}).get(
            'apigeeRuntime',{}).get('value','apigee-runtime')
        apigee_data_node_selector_key = input_data.get('nodeSelector',{}).get(
            'apigeeData',{}).get('key','cloud.google.com/gke-nodepool')
        apigee_data_node_selector_key = input_data.get('nodeSelector',{}).get(
            'apigeeData',{}).get('value','apigee-data')

        if not check_nodes(f"{apigee_rt_node_selector_key}={apigee_rt_node_selector_value}"):
            validations.append(f"Number of nodes with selectors {apigee_rt_node_selector_key}={apigee_rt_node_selector_value} are Zero[0]")
        if not check_nodes(f"{apigee_data_node_selector_key}={apigee_data_node_selector_key}"):
            validations.append(f"Number of nodes with selectors {apigee_data_node_selector_key}={apigee_data_node_selector_key} are Zero[0]")

    apigee_secrets = list_namespace_secrets(secret_namespace)
    
    for apigee_vhost in apigee_vhosts:
        if apigee_vhost['sslSecret'] not in apigee_secrets:
            validations.append(f"SSL Secret: {apigee_vhost['sslSecret']} Not found in {secret_namespace} namespace")

    input_service_account_secrets = []
    _finditem(input_data,'serviceAccountRef',input_service_account_secrets)

    for each_sa_secret in input_service_account_secrets:
        if each_sa_secret not in apigee_secrets:
            validations.append(f"Service Account Secret: {each_sa_secret} Not found in {secret_namespace} namespace")

    if len(validations) > 0:
        print('Kubernetes validation Errors found !')
        print("\n".join(validations))
        sys.exit(1)
    print('Kubernetes validations successfull')

if __name__ == '__main__':
    main()